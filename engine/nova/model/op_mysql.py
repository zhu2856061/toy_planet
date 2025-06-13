# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging
from http import HTTPStatus
from typing import Any, Dict

from mysql.connector import Error

from nova import mysql_client
from nova.utils.common import timer

logger = logging.getLogger(__name__)


@timer
def insert(table_name, data: Dict[str, Any]):
    """插入数据"""
    try:
        cursor = mysql_client.cursor(dictionary=True)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        mysql_client.commit()
        logger.info(f"成功插入数据到 {table_name}")
        return {"code": HTTPStatus.OK, "msg": "ok", "data": {"lastrowid": cursor.lastrowid}}
    except Error as e:
        logger.error(f"插入数据失败: {e}")
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": f"插入数据失败: {e}"}
    finally:
        cursor.close()


@timer
def select(table_name, conditions: Dict[str, Any]):
    """查询数据"""
    try:
        cursor = mysql_client.cursor(dictionary=True)

        sql = f"SELECT * FROM {table_name}"

        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        sql += f" WHERE {where_clause}"
        cursor.execute(sql, list(conditions.values()))

        lines = cursor.fetchall()
        logger.info(f"查询到 {len(lines)} 条数据从 {table_name}")
        return {"code": HTTPStatus.OK, "msg": "ok", "data": {"lines": lines}}
    except Error as e:
        logger.error(f"查询数据失败: {e}")
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": f"查询数据失败: {e}"}
    finally:
        cursor.close()


@timer
def select_by_set_codes(table_name, set_codes: list):
    """根据 set_code 列表查询数据"""
    try:
        cursor = mysql_client.cursor(dictionary=True)
        # 将列表转换为 IN 子句的格式
        placeholders = ",".join(["%s"] * len(set_codes))
        query_sql = f"SELECT * FROM {table_name} WHERE set_code IN ({placeholders})"
        cursor.execute(query_sql, set_codes)
        lines = cursor.fetchall()
        logger.info(f"查询到 {len(lines)} 条数据")
        return {"code": HTTPStatus.OK, "msg": "ok", "data": {"lines": lines}}
    except Error as e:
        logger.error(f"查询数据失败: {e}")
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": f"查询数据失败: {e}"}
    finally:
        cursor.close()


@timer
def update(table_name, data: Dict[str, Any]):
    """更新数据"""
    try:
        cursor = mysql_client.cursor(dictionary=True)
        id = data.get("id", None)
        if id is None:
            return {"code": 1, "msg": "没有提供id"}

        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        where_clause = f" id = {id} "
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(sql, list(data.values()))
        mysql_client.commit()
        logger.info(f"成功更新 {cursor.rowcount} 条数据在 {table_name}")
        return {"code": HTTPStatus.OK, "msg": "ok", "data": {"rowcount": cursor.rowcount}}
    except Error as e:
        logger.error(f"更新数据失败: {e}")
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": f"更新数据失败: {e}"}
    finally:
        cursor.close()


@timer
def delete(table_name, conditions: Dict[str, Any]):
    """删除数据"""
    try:
        cursor = mysql_client.cursor(dictionary=True)

        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        sql = f"DELETE FROM {table_name} WHERE {where_clause}"
        cursor.execute(sql, list(conditions.values()))
        mysql_client.commit()
        logger.info(f"成功删除 {cursor.rowcount} 条数据从 {table_name}")
        return {"code": HTTPStatus.OK, "msg": "ok", "data": {"rowcount": cursor.rowcount}}
    except Error as e:
        logger.error(f"删除数据失败: {e}")
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": f"删除数据失败: {e}"}
    finally:
        cursor.close()


@timer
def query_by_page(table_name, page: int, page_size: int):
    """
    按照页码和每页数量查询 toy_kit 表数据。

    Args:
        connection: MySQL 数据库连接对象
        page (int): 页码（从 1 开始）
        page_size (int): 每页数量

    Returns:
        List[Dict[str, Any]]: 查询结果列表，每个元素为一行数据的字典

    Raises:
        ValueError: 如果页码或每页数量小于 1
        mysql.connector.Error: 如果查询失败
    """
    if page < 1 or page_size < 1:
        return {"code": 1, "msg": "页码和每页数量必须大于 0"}

    try:
        cursor = mysql_client.cursor(dictionary=True)

        # 计算 OFFSET
        offset = (page - 1) * page_size

        # 查询数据
        query_sql = f"""
        SELECT * FROM {table_name}
        ORDER BY id
        LIMIT %s OFFSET %s
        """
        cursor.execute(query_sql, (page_size, offset))
        lines = cursor.fetchall()

        logger.info(f"页码 {page}，每页 {page_size} 条，查询到 {len(lines)} 条数据")
        return {"code": HTTPStatus.OK, "msg": "ok", "data": {"lines": lines}}

    except Error as e:
        logger.error(f"分页查询 toy_kit 表失败: {e}")
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": f"查询数据失败: {e}"}
    finally:
        cursor.close()
