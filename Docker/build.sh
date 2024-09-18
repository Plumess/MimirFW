#!/bin/bash

# 定义路径
SCRIPT_DIR="./scripts"
ROOT_DIR="./"
LLMCORE_DIR="./LLMCore"

# 调用 device-check.sh 脚本来检测设备并生成 device.env 文件
$SCRIPT_DIR/device-check.sh

# 导出检查到的环境变量到会话，用于构建
export $(grep -v '^#' $ROOT_DIR/device.env | xargs)

# 动态设置镜像标签
IMAGE_TAG="llmcore:${BUILD_STAGE,,}"  # 使用 BUILD_STAGE 并转换为小写

# 使用 docker-compose 构建和启动服务
docker-compose up -d --build && docker image prune -f
