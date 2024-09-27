#!/bin/bash

# 原始工作路径
ORIGINAL_DIR=$(pwd)

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

# 如果没有vLLM项目，git clone 一份，由.env 控制的版本号
TARGET_DIR="./vLLM"
export $(grep -v '^#' .env | xargs)
# 检查目标目录下是否有 .git 文件夹
if [ -d "$TARGET_DIR/.git" ]; then
    echo "Git repository already exists in $TARGET_DIR."
    # 检查是否是完整克隆且没有损坏
    cd $TARGET_DIR
    git fetch --dry-run > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Repository in $TARGET_DIR is fully cloned and healthy."
    else
        echo "Repository exists but might be corrupted or incomplete. Re-cloning..."
        cd ..
        rm -rf $TARGET_DIR
        git clone -b $VLLM_VERSION https://github.com/vllm-project/vllm.git $TARGET_DIR
    fi
else
    echo "Cloning the repository..."
    git clone -b $VLLM_VERSION https://github.com/vllm-project/vllm.git $TARGET_DIR
fi

# 恢复到原始工作目录
cd $ORIGINAL_DIR

# 根据设备类型确定使用的 Dockerfile
if [[ "$DEVICE" == "cuda" ]]; then
    export DOCKERFILE_DEVICE="Dockerfile"
else
    export DOCKERFILE_DEVICE="Dockerfile.$DEVICE"
fi

# 根据设备类型构建和启动服务
if [[ "$DEVICE" == "cuda" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.cuda.yml up -d --build && docker image prune -f
elif [[ "$DEVICE" == "cpu" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.cpu.yml up -d --build && docker image prune -f
elif [[ "$DEVICE" == "mps" ]]; then
    docker-compose -f docker-compose.yml -f docker-compose.override.mps.yml up -d --build && docker image prune -f
else
    docker-compose up -d --build && docker image prune -f
fi

