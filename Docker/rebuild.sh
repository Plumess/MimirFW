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
else
    # 检查是否是 Apple M1/M2 芯片（用于 MPS）
    if [[ "$(uname -s)" == "Darwin" ]] && [[ "$(sysctl -n machdep.cpu.brand_string)" == *"Apple"* ]]
    then
        export DEVICE="mps"
    fi
fi

# 根据设备类型确定使用的 Dockerfile
if [[ "$DEVICE" == "cuda" ]]; then
    export DOCKERFILE_DEVICE="Dockerfile"
else
    export DOCKERFILE_DEVICE="Dockerfile.$DEVICE"
fi

# 构建 llmcore 和 weaviate 服务，跳过 vllm 服务(重构需要重新编译，不建议)
docker-compose build llmcore weaviate

# 根据设备类型启动服务，但不重构 vllm
if [[ "$DEVICE" == "cuda" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.cuda.yml up -d llmcore weaviate && docker image prune -f
elif [[ "$DEVICE" == "cpu" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.cpu.yml up -d llmcore weaviate && docker image prune -f
elif [[ "$DEVICE" == "mps" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.mps.yml up -d llmcore weaviate && docker image prune -f
else
    docker-compose up -d llmcore weaviate && docker image prune -f
fi
