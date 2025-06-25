# -*- coding: utf-8 -*-
# @Time   : 2025/06/14 
# @Author : guido
# @Desc   : 搜索相关功能
from http import HTTPStatus
import logging
import random
import threading
import time

import schedule
import mysql
from mysql.connector import Error

from nova import mysql_client


logger = logging.getLogger(__name__)

SET_TABLE_NAME = "set_info"

def get_set_by_query(query):
    """
    根据查询条件获取套装信息
    """

    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123",
        database="toy_planet",
        charset="utf8mb4",  # 指定字符集为 utf8mb4
        collation="utf8mb4_unicode_ci",  # 指定排序规则
    )
    cursor = conn.cursor(dictionary=True)

    sql = f"""
        SELECT * 
        FROM {SET_TABLE_NAME}
        WHERE name LIKE %s
    """
    cursor.execute(sql, (f"%{query}%",))
    lines = cursor.fetchall()

    logger.info(f"查询到 {len(lines)} 条数据从 {SET_TABLE_NAME}")
    cursor.close()
    
    return {"code": HTTPStatus.OK, "msg": "ok", "data": {"lines": lines}}