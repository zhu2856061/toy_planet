# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging
from typing import Dict, Optional

from fastapi import APIRouter
from mysql.connector import Error
from pydantic import BaseModel, Field

from nova.model import (
    TOY_BRANDS_TABLE_NAME,
    TOY_KIT_TABLE_NAME,
    TOY_THEMES_TABLE_NAME,
    delete,
    insert,
    query_by_page,
    select,
    update,
)

logger = logging.getLogger(__name__)

# Define the router
mysql_router = APIRouter(
    tags=["mysql"],
    responses={404: {"description": "Not found"}},
)


# 🌟
class MYSQLRequest(BaseModel):
    trace_id: Optional[str] = None
    kit_table: Optional[Dict] = None
    themes_table: Optional[Dict] = None
    brands_table: Optional[Dict] = None


class MYSQLResponse(BaseModel):
    code: int = Field(..., description="HTTP 状态码")
    msg: str = Field(..., description="HTTP 状态码描述")
    data: Optional[Dict] = Field(None, description="返回核心数据")


# 🌟
@mysql_router.post("/insert", response_model=MYSQLResponse)
async def insert_server(mysqlRequest: MYSQLRequest):
    """插入数据"""
    try:
        trace_id = mysqlRequest.trace_id
        kit_table = mysqlRequest.kit_table
        themes_table = mysqlRequest.themes_table
        brands_table = mysqlRequest.brands_table

        data = None
        if kit_table:
            data = insert(TOY_KIT_TABLE_NAME, kit_table)
        if themes_table:
            data = insert(TOY_THEMES_TABLE_NAME, themes_table)
        if brands_table:
            data = insert(TOY_BRANDS_TABLE_NAME, brands_table)

        if data is None:
            logger.error(f"trace_id={trace_id}, 插入数据失败, 无数据")
            return MYSQLResponse(code=1, msg="插入数据失败, 无数据", data={})

        logger.info(f"插入数据成功: tace_id: {trace_id}")
        return MYSQLResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"插入数据失败: {e}")
        return MYSQLResponse(code=1, msg=f"插入数据失败: {e}", data={})


# 🌟
@mysql_router.post("/select", response_model=MYSQLResponse)
def select_server(mysqlRequest: MYSQLRequest):
    """查询数据"""
    try:
        trace_id = mysqlRequest.trace_id
        kit_table = mysqlRequest.kit_table
        themes_table = mysqlRequest.themes_table
        brands_table = mysqlRequest.brands_table

        data = None
        if kit_table:
            data = select(TOY_KIT_TABLE_NAME, kit_table)
        if themes_table:
            data = select(TOY_THEMES_TABLE_NAME, themes_table)
        if brands_table:
            data = select(TOY_BRANDS_TABLE_NAME, brands_table)

        if data is None:
            logger.error(f"trace_id={trace_id}, 查询数据失败, 无数据")
            return MYSQLResponse(code=1, msg="查询数据失败, 无数据", data={})

        logger.info(f"查询数据成功: tace_id: {trace_id}")
        return MYSQLResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"查询数据失败: {e}")
        return MYSQLResponse(code=1, msg=f"查询数据失败: {e}", data={})


# 🌟
@mysql_router.post("/update", response_model=MYSQLResponse)
def update_server(mysqlRequest: MYSQLRequest):
    """查询数据"""
    try:
        trace_id = mysqlRequest.trace_id
        kit_table = mysqlRequest.kit_table
        themes_table = mysqlRequest.themes_table
        brands_table = mysqlRequest.brands_table

        data = None
        if kit_table:
            data = update(TOY_KIT_TABLE_NAME, kit_table)
        if themes_table:
            data = update(TOY_THEMES_TABLE_NAME, themes_table)
        if brands_table:
            data = update(TOY_BRANDS_TABLE_NAME, brands_table)

        if data is None:
            logger.error(f"trace_id={trace_id}, 更新数据失败, 无数据")
            return MYSQLResponse(code=1, msg="更新数据失败, 无数据", data={})

        logger.info(f"更新数据成功: tace_id: {trace_id}")
        return MYSQLResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"更新数据失败: {e}")
        return MYSQLResponse(code=1, msg=f"更新数据失败: {e}", data={})


# 🌟
@mysql_router.post("/delete", response_model=MYSQLResponse)
def delete_server(mysqlRequest: MYSQLRequest):
    """查询数据"""
    try:
        trace_id = mysqlRequest.trace_id
        kit_table = mysqlRequest.kit_table
        themes_table = mysqlRequest.themes_table
        brands_table = mysqlRequest.brands_table

        data = None
        if kit_table:
            data = delete(TOY_KIT_TABLE_NAME, kit_table)
        if themes_table:
            data = delete(TOY_THEMES_TABLE_NAME, themes_table)
        if brands_table:
            data = delete(TOY_BRANDS_TABLE_NAME, brands_table)

        if data is None:
            logger.error(f"trace_id={trace_id}, 删除数据失败, 无数据")
            return MYSQLResponse(code=1, msg="删除数据失败, 无数据", data={})

        logger.info(f"删除数据成功: tace_id: {trace_id}")
        return MYSQLResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"删除数据失败: {e}")
        return MYSQLResponse(code=1, msg=f"删除数据失败: {e}", data={})


# 🌟
@mysql_router.post("/query_by_page", response_model=MYSQLResponse)
def query_by_page_server(mysqlRequest: MYSQLRequest):
    """查询数据"""
    try:
        trace_id = mysqlRequest.trace_id
        kit_table = mysqlRequest.kit_table
        themes_table = mysqlRequest.themes_table
        brands_table = mysqlRequest.brands_table

        data = None

        if kit_table:
            data = query_by_page(
                TOY_KIT_TABLE_NAME,
                kit_table.get("page", 0),
                kit_table.get("page_size", 0),
            )
        if themes_table:
            data = query_by_page(
                TOY_THEMES_TABLE_NAME,
                themes_table.get("page", 0),
                themes_table.get("page_size", 0),
            )
        if brands_table:
            data = query_by_page(
                TOY_BRANDS_TABLE_NAME,
                brands_table.get("page", 0),
                brands_table.get("page_size", 0),
            )

        if data is None:
            logger.error(f"trace_id={trace_id}, 分页查询数据失败, 无数据")
            return MYSQLResponse(code=1, msg="分页查询数据失败, 无数据", data={})

        logger.info(f"分页查询数据成功: tace_id: {trace_id}")
        return MYSQLResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"分页查询数据失败: {e}")
        return MYSQLResponse(code=1, msg=f"分页查询数据失败: {e}", data={})
