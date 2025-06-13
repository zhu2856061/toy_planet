# -*- coding: utf-8 -*-
# @Time   : 2025/05/12 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nova.service import mysql_router, rec_router, search_router

# --- Logging Configuration ---
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
# Define constants for better readability and easier modification


@asynccontextmanager
async def lifespan(app: FastAPI):
    """定义 FastAPI 生命周期事件"""
    # 启动时加载分词器和模型
    yield
    # 关闭时清理资源
    logger.info("清理资源")


app = FastAPI(
    title="Engine Service",
    description="一个通用的引擎服务",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# init
# Include the FAQ router
app.include_router(mysql_router, prefix="/mysql")
app.include_router(rec_router, prefix="/rec")
app.include_router(search_router, prefix="/search")

if __name__ == "__main__":
    logger.info("Starting nova API server")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
