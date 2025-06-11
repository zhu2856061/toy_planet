import logging
import time
from functools import wraps

import mysql.connector
from mysql.connector import Error

logger = logging.getLogger(__name__)


class Timer:
    """
    使用方式： 在指定的需要计算耗时的代码块前加上 with Timer()

    with Timer():
        # 这里是你要计时的代码块
    """

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        logger.info(f"代码块耗时 (Timer): {self.elapsed_time:.4f} 秒")


# 定义计时装饰器
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 使用高精度计时
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.perf_counter()
        logger.info(f"函数 {func.__name__} 耗时: {end_time - start_time:.4f} 秒")
        return result

    return wrapper


def connect_mysql_database(
    host: str, port: str, user: str, password: str, database: str
):
    """
    连接到 MySQL 数据库，若数据库不存在则创建。

    Args:
        host (str): MySQL 服务器地址
        port (str): MySQL 端口号
        user (str): MySQL 用户名
        password (str): MySQL 密码
        database (str): 要连接的数据库名称

    Returns:
        mysql.connector.connection.MySQLConnection: 数据库连接对象

    Raises:
        mysql.connector.Error: 如果连接或创建数据库失败
    """
    connection = None
    try:
        # 先尝试连接到 MySQL 服务器（不指定数据库）
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="utf8mb4",  # 指定字符集为 utf8mb4
            collation="utf8mb4_unicode_ci",  # 指定排序规则
        )
        cursor = connection.cursor()

        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{database}'")
        if cursor.fetchone():
            logger.info(f"数据库 {database} 已存在，直接连接")
            connection.database = database  # type: ignore
        else:
            # 创建数据库
            cursor.execute(
                f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            connection.commit()
            connection.database = database  # type: ignore
            logger.info(f"数据库 {database} 创建成功并已连接")

        cursor.close()
        return connection

    except Error as e:
        logger.error(f"连接或创建数据库失败: {e}")
        if connection and connection.is_connected():
            connection.close()
        raise

    except Exception as e:
        logger.error(f"意外错误: {e}")
        if connection and connection.is_connected():
            connection.close()
        raise
