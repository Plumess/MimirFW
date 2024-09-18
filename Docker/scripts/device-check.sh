#!/bin/bash

# 默认设备类型
DEVICE="cpu"
USE_CUDA="false"
CUDA_DEVICES=""
BUILD_STAGE="cpu"

# 检查是否有 NVIDIA GPU
if command -v nvidia-smi &> /dev/null
then
    DEVICE="cuda"
    USE_CUDA="true"
    BUILD_STAGE="nvidia"
    # 获取所有可用的 GPU ID
    CUDA_DEVICES=$(nvidia-smi --query-gpu=index --format=csv,noheader | tr '\n' ',')
    # 移除最后一个逗号
    CUDA_DEVICES="${CUDA_DEVICES%,}"
else
    # 检查是否是 Apple M1/M2 芯片（用于 MPS）
    if [[ "$(uname -s)" == "Darwin" ]] && [[ "$(sysctl -n machdep.cpu.brand_string)" == *"Apple"* ]]
    then
        DEVICE="mps"
        BUILD_STAGE="mac"
    fi
fi

# 生成 device.env 文件
echo "DEVICE=$DEVICE" > device.env
echo "USE_CUDA=$USE_CUDA" >> device.env
echo "BUILD_STAGE=$BUILD_STAGE" >> device.env

# 仅当 CUDA 可用时才写入 CUDA_DEVICES
if [ "$USE_CUDA" = "true" ]; then
    echo "CUDA_DEVICES=$CUDA_DEVICES" >> device.env
fi
