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

from nova.model import (
    TOY_KIT_TABLE_NAME,
    get_hot_by_uid,
    get_new_by_uid,
    insert_uid_history,
    select_by_set_codes,
)

logger = logging.getLogger(__name__)

# Define the router
rec_router = APIRouter(
    tags=["rec"],
    responses={404: {"description": "Not found"}},
)


# 🌟
class RECRequest(BaseModel):
    trace_id: Optional[str] = None
    rec_data: Dict = Field(..., description="推荐对象信息")


class RECResponse(BaseModel):
    code: int = Field(..., description="HTTP 状态码")
    msg: str = Field(..., description="HTTP 状态码描述")
    data: Optional[Dict] = Field(None, description="返回核心数据")


# 🌟
@rec_router.post("/hot", response_model=RECResponse)
async def rec_hot_server(recRequest: RECRequest):
    """获取热门数据"""
    try:
        trace_id = recRequest.trace_id
        rec_data = recRequest.rec_data
        uid = rec_data.get("uid", None)
        topk = rec_data.get("topk", 10)
        if uid is None:
            logger.error(f"trace_id={trace_id}, 数据中缺少uid字段")
            return RECResponse(code=HTTPStatus.BAD_REQUEST, msg="插入数据失败, 数据中缺少uid字段", data={})

        # 获得 热门数据 set_code
        data = get_hot_by_uid(trace_id, uid, topk)
        if data["code"] != HTTPStatus.OK:
            logger.error(
                f"trace_id={trace_id}, 获得热门推荐失败， error: {data['msg']}"
            )
            return RECResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg="获得热门推荐失败", data={})
        hot_item = data["data"]["tok_result"]

        # 基于这个结果，从库中获取到 热门set_code 的详情数据
        data = select_by_set_codes(TOY_KIT_TABLE_NAME, hot_item)
        if data["code"] == HTTPStatus.OK:
            logger.info(f"获得热门推荐: tace_id: {trace_id}")
            insert_uid_history(trace_id, uid, hot_item)

        return RECResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"获得热门推荐失败: {e}")
        return RECResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg=f"获得热门推荐失败: {e}", data={})


# 🌟
@rec_router.post("/new", response_model=RECResponse)
async def rec_new_server(recRequest: RECRequest):
    """获取新品数据"""
    try:
        trace_id = recRequest.trace_id
        rec_data = recRequest.rec_data
        uid = rec_data.get("uid", None)
        topk = rec_data.get("topk", 10)
        if uid is None:
            logger.error(f"trace_id={trace_id}, 数据中缺少uid字段")
            return RECResponse(code=HTTPStatus.BAD_REQUEST, msg="插入数据失败, 数据中缺少uid字段", data={})

        # 获得 新品数据 set_code
        data = get_new_by_uid(trace_id, uid, topk)
        if data["code"] != HTTPStatus.OK:
            logger.error(f"trace_id={trace_id}, 获得新品推荐失败")
            return RECResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg="获得新品推荐失败", data={})
        hot_item = data["data"]["tok_result"]

        # 基于这个结果，从库中获取到 新品set_code 的详情数据
        data = select_by_set_codes(TOY_KIT_TABLE_NAME, hot_item)
        if data["code"] == HTTPStatus.OK:
            logger.info(f"获得新品推荐: tace_id: {trace_id}")
            insert_uid_history(trace_id, uid, hot_item)

        return RECResponse(
            code=data["code"], msg=data["msg"], data=data.get("data", {})
        )
    except Error as e:
        logger.error(f"获得新品推荐失败: {e}")
        return RECResponse(code=HTTPStatus.INTERNAL_SERVER_ERROR, msg=f"获得新品推荐失败: {e}", data={})
