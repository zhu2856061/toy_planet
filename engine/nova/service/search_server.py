# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging
from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter
from mysql.connector import Error
from pydantic import BaseModel, Field
import mysql.connector

from nova.model import TOY_KIT_TABLE_NAME, get_hot_by_keyword, select_by_set_codes
from nova.model import get_set_by_query

logger = logging.getLogger(__name__)


# Define the router
search_router = APIRouter(
    tags=["search"],
    responses={404: {"description": "Not found"}},
)


# 🌟
class SEARCHRequest(BaseModel):
    trace_id: Optional[str] = None
    query : Optional[str] = None 


class SEARCHResponse(BaseModel):
    code: int = Field(..., description="HTTP 状态码")
    msg: str = Field(..., description="HTTP 状态码描述")
    data: Optional[Dict] = Field(None, description="返回核心数据")


# 🌟
@search_router.post("/hot", response_model=SEARCHResponse)
async def search_hot_server(recRequest: SEARCHRequest):
    """获取热门数据"""
    try:
        trace_id = recRequest.trace_id
        search_data = recRequest.search_data
        keyword = search_data.get("keyword", None)
        topk = search_data.get("topk", 10)
        if keyword is None:
            logger.error(f"trace_id={trace_id}, 数据中缺少keyword字段")
            return SEARCHResponse(
                code=HTTPStatus.BAD_REQUEST, msg="插入数据失败, 数据中缺少keyword字段", data={}
            )

        # 获得 热门数据 set_code
        data = get_hot_by_keyword(trace_id, keyword, topk)
        if data["code"] != 0:
            logger.error(
                f"trace_id={trace_id}, 获得热门推荐失败， error: {data['msg']}"
            )
            return SEARCHResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg="获得热门推荐失败", data={})
        hot_item = data["data"]["tok_result"]

        # 基于这个结果，从库中获取到 热门set_code 的详情数据
        data = select_by_set_codes(TOY_KIT_TABLE_NAME, hot_item)
        if data["code"] == 0:
            logger.info(f"获得热门推荐: tace_id: {trace_id}")

        return SEARCHResponse(
            code=HTTPStatus.OK, msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"获得热门推荐失败: {e}")
        return SEARCHResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg=f"获得热门推荐失败: {e}", data={})


@search_router.post("/set", response_model=SEARCHResponse)
async def search_set_server(searchRequest: SEARCHRequest):
    """
        1. 套装搜索服务
    """


    try:
        trace_id = searchRequest.trace_id
        query = searchRequest.query
        data = get_set_by_query(query)
        if data["code"] == HTTPStatus.OK:
            logger.info(f"获得套装搜索结果: trace_id: {trace_id}")

        return SEARCHResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"获得套装搜索失败: {e}")
        return SEARCHResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg=f"获得套装搜索失败: {e}", data={})

