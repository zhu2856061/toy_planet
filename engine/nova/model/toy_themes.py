# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging

from mysql.connector import Error

from nova import mysql_client

logger = logging.getLogger(__name__)

TABLE_NAME = "TOY_THEMES"


def create_toy_themes_table():
    """仅在表不存在时创建表"""
    try:
        cursor = mysql_client.cursor(dictionary=True)
        # 检查表是否存在
        cursor.execute(f"SHOW TABLES LIKE '{TABLE_NAME}'")
        if cursor.fetchone():
            logger.info(f"表 {TABLE_NAME} 已存在，不重复创建")
            return

        # 创建表
        create_table_sql = f"""
        CREATE TABLE {TABLE_NAME} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            parent_theme_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """
        cursor.execute(create_table_sql)
        mysql_client.commit()
        logger.info(f"表 {TABLE_NAME} 创建成功")
    except Error as e:
        logger.error(f"创建表 {TABLE_NAME} 失败: {e}")
        raise
    finally:
        cursor.close()
