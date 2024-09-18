#!/bin/bash

# 定义路径
SCRIPT_DIR="./scripts"
ROOT_DIR="./"
LLMCORE_DIR="./LLMCore"

# 检测设备以区分构建
export DEVICE="cpu"
export USE_CUDA="false"
export CUDA_DEVICES=""
export BUILD_STAGE="cpu"

# 检查是否有 NVIDIA GPU
if command -v nvidia-smi &> /dev/null
then
    export DEVICE="cuda"
    export USE_CUDA="true"
    export BUILD_STAGE="nvidia"
    # 获取所有可用的 GPU ID
    export CUDA_DEVICES=$(nvidia-smi --query-gpu=index --format=csv,noheader | tr '\n' ',')
    # 移除最后一个逗号
    export CUDA_DEVICES="${CUDA_DEVICES%,}"
else
    # 检查是否是 Apple M1/M2 芯片（用于 MPS）
    if [[ "$(uname -s)" == "Darwin" ]] && [[ "$(sysctl -n machdep.cpu.brand_string)" == *"Apple"* ]]
    then
        export DEVICE="mps"
        export BUILD_STAGE="mac"
    fi
fi

# 动态设置镜像标签
export IMAGE_TAG="llmcore:${BUILD_STAGE,,}"  # 使用 BUILD_STAGE 并转换为小写

# # 生成 device.env 文件
# echo "DEVICE=$DEVICE" >> device.env
# echo "USE_CUDA=$USE_CUDA" >> device.env
# echo "BUILD_STAGE=$BUILD_STAGE" >> device.env

# # 仅当 CUDA 可用时才写入 CUDA_DEVICES
# if [ "$USE_CUDA" = "true" ]; then
#     echo "CUDA_DEVICES=$CUDA_DEVICES" >> device.env
# fi

# 使用 docker-compose 构建和启动服务
docker-compose up -d --build && docker image prune -f
