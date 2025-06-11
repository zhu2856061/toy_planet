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

keyword_history_cache = TTLCache(maxsize=10000, ttl=86400)


# 获取热品
def get_hot_by_keyword(trace_id, keyword, topk):
    try:
        res = keyword_history_cache.get(keyword, None)
        if res is not None and len(res) >= topk:
            return {"code": 0, "msg": "ok", "data": {"tok_result": res[:topk]}}

        cursor = mysql_client.cursor(dictionary=True)
        query_sql = f"""
        SELECT set_code
        FROM {TABLE_NAME}
        WHERE name LIKE %s OR description LIKE %s
        ORDER BY hot DESC
        LIMIT {topk}
        """
        cursor.execute(query_sql, (f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()

        # 写入cacahe
        keyword_history_cache[keyword] = [result["set_code"] for result in results]  # type: ignore
        results = keyword_history_cache[keyword]

        logger.info(f"trace_id: {trace_id}, 写入关键词缓存 {len(results)} 条数据")
        return {"code": 0, "msg": "ok", "data": {"tok_result": results}}

    except Error as e:
        logger.error(f"trace_id: {trace_id}, 写入关键词缓存数据失败: {e}")
        return {
            "code": 1,
            "msg": f"trace_id: {trace_id}, Error in get_hot_by_keyword: {e}",
        }
    finally:
        cursor.close()
