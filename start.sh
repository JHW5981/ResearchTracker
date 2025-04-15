#!/bin/bash

# 进入前端目录构建静态文件
cd frontend
echo "Building frontend..."
npm run build

# 返回项目根目录
cd ..

# 启动后端服务（会同时服务前端静态文件）
echo "Starting server..."
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 