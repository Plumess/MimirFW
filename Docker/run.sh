#!/bin/bash

# 检测设备以区分构建
export DEVICE="cpu"
export USE_CUDA="false"
export CUDA_DEVICES=""

# 检查是否有 NVIDIA GPU
if command -v nvidia-smi &> /dev/null
then
    export DEVICE="cuda"
    export USE_CUDA="true"
    # 获取所有可用的 GPU ID
    export CUDA_DEVICES=$(nvidia-smi --query-gpu=index --format=csv,noheader | tr '\n' ',')
    # 移除最后一个逗号
    export CUDA_DEVICES="${CUDA_DEVICES%,}"
fi

# 根据设备类型确定使用的 Dockerfile
if [[ "$DEVICE" == "cuda" ]]; then
    export DOCKERFILE_DEVICE="Dockerfile"
else
    export DOCKERFILE_DEVICE="Dockerfile.$DEVICE"
fi

# 根据设备类型构建和启动服务
if [[ "$DEVICE" == "cuda" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.cuda.yml up -d --remove-orphans && docker image prune -f
elif [[ "$DEVICE" == "cpu" ]]; then
    docker-compose up -d --remove-orphans && docker image prune -f
fi

