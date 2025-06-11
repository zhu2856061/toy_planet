# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging
import random
import threading
import time

import schedule
from cachetools import LRUCache, TTLCache
from mysql.connector import Error

from nova import mysql_client

from .toy_kit import TABLE_NAME

logger = logging.getLogger(__name__)

# LRU 缓存，最大 1000 项
hot_cache = LRUCache(maxsize=1000)  # {"set_code": hot_value}
new_cache = LRUCache(maxsize=1000)

user_history_cache = TTLCache(maxsize=10000, ttl=86400)

# Lock for thread-safe cache updates
hot_cache_lock = threading.Lock()
new_cache_lock = threading.Lock()


# 从数据库中拉取到最热门的1000个 set_code
def insert_hot_cache():
    try:
        with hot_cache_lock:
            cursor = mysql_client.cursor(dictionary=True)
            query_sql = f"""
            SELECT set_code, hot
            FROM {TABLE_NAME}
            ORDER BY hot DESC
            LIMIT 1000
            """
            cursor.execute(query_sql)
            results = cursor.fetchall()

            # 写入cacahe

            for result in results:
                hot_cache[result["set_code"]] = result["hot"]  # type: ignore

            logger.info(f"写入热门缓存 {len(results)} 条数据")

    except Error as e:
        logger.error(f"写入热门缓存数据失败: {e}")

    finally:
        cursor.close()


def insert_new_cache():
    try:
        with new_cache_lock:
            cursor = mysql_client.cursor(dictionary=True)
            query_sql = f"""
            SELECT set_code, hot
            FROM {TABLE_NAME}
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 3 DAY)
            ORDER BY hot DESC
            LIMIT 1000
            """
            cursor.execute(query_sql)
            results = cursor.fetchall()

            # 写入cacahe
            for result in results:
                new_cache[result["set_code"]] = result["hot"]  # type: ignore

            logger.info(f"写入新品缓存 {len(results)} 条数据")

    except Error as e:
        logger.error(f"写入新品缓存数据失败: {e}")
    finally:
        cursor.close()


def cache_update_process():
    try:
        # 服务启动时立即加载缓存
        insert_hot_cache()
        insert_new_cache()
        # 设置定时任务，每 6 小时执行一次
        schedule.every(6).hours.do(insert_hot_cache)
        schedule.every(6).hours.do(insert_new_cache)

        # 保持进程运行，执行定时任务
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次任务

    except Exception as e:
        logger.error(f"缓存更新进程失败: {e}")


def start_cache_update_thread():
    # Start cache update in a background thread
    cache_thread = threading.Thread(target=cache_update_process, daemon=True)
    cache_thread.start()
    logger.info("Cache update thread started")


# 用户历史记录
def insert_uid_history(trace_id, uid, set_codes):
    try:
        uid_hist = user_history_cache.get(uid, None)
        if uid_hist is None:
            user_history_cache[uid] = set(set_codes)
        else:
            user_history_cache[uid] = uid_hist.union(set(set_codes))
        logger.info(f"trace_id={trace_id}, 插入用户历史记录成功")
    except Exception as e:
        logger.error(f"trace_id={trace_id}, 插入用户历史记录失败, err: {e}")


# 获取热品
def get_hot_by_uid(trace_id, uid, topk):
    try:
        uid_hist = user_history_cache.get(uid, [])

        all_items = list(hot_cache.items())

        if len(all_items) < topk:
            return {"code": 1, "msg": f"trace_id: {trace_id}, 热门 item 不够"}

        all_items = sorted(all_items, key=lambda x: x[1], reverse=True)

        tok_result = []
        for code, _ in all_items:
            if code in uid_hist:
                continue
            tok_result.append(code)
            if len(tok_result) == topk:
                break

        if len(tok_result) < topk:
            # 随机从all_items中抽取不够的数量
            tmp = random.sample(all_items, topk - len(tok_result))
            tok_result.extend([_[0] for _ in tmp])

        return {"code": 0, "msg": "ok", "data": {"tok_result": tok_result}}
    except Exception as e:
        logger.error(f"trace_id: {trace_id}, Error in get_hot_by_uid: {e}")
        return {
            "code": 1,
            "msg": f"trace_id: {trace_id}, Error in get_hot_by_uid: {e}",
        }


# 获取新品
def get_new_by_uid(trace_id, uid, topk):
    try:
        uid_hist = user_history_cache.get(uid, None)

        all_items = list(new_cache.items())
        all_items = sorted(all_items, key=lambda x: x[1], reverse=True)

        tok_result = []
        for code, _ in all_items:
            if code in uid_hist:
                continue
            tok_result.append(code)
            if len(tok_result) == topk:
                break

        if len(tok_result) < topk:
            # 随机从all_items中抽取不够的数量
            tmp = random.sample(all_items, topk - len(tok_result))
            tok_result.extend([_[0] for _ in tmp])

        return {"code": 0, "msg": "ok", "data": {"tok_result": tok_result}}
    except Exception as e:
        logger.error(f"trace_id: {trace_id}, Error in get_new_by_uid: {e}")
        return {
            "code": 1,
            "msg": f"trace_id: {trace_id}, Error in get_new_by_uid: {e}",
        }
