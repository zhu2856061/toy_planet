# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging

from mysql.connector import Error

from nova import mysql_client

logger = logging.getLogger(__name__)

# TABLE_NAME = "TOY_KIT"
TABLE_NAME = "set_info" 


def create_toy_kit_table():
    """仅在表不存在时创建 toy_kit 表"""
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
            set_code VARCHAR(50) NOT NULL,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            brand_id INT,
            theme_id INT,
            num_parts INT,
            price DECIMAL(10, 2),
            currency VARCHAR(10),
            release_year INT,
            main_image_url VARCHAR(512),
            gallery_image_urls JSON,
            is_sale BOOLEAN DEFAULT FALSE,
            hot INT DEFAULT 0,
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


def insert_kit_table():
    datas = [
        {"set_code": "C00002", "name": "迈凯伦 765LT"},
        {"set_code": "Y00001", "name": "太空熊猫"},
    ]
    """插入数据"""
    try:
        for data in datas:
            cursor = mysql_client.cursor(dictionary=True)
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            sql = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            mysql_client.commit()
            logger.info(f"样例数据成功插入到 {TABLE_NAME}")
    except Error as e:
        logger.error(f"插入数据失败: {e}")
    finally:
        cursor.close()
