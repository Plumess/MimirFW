#!/bin/bash

# 获取当前工作目录
CURRENT_DIR=$(pwd)

# 切换到 install.sh 所在的目录
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" || { echo "无法进入脚本目录，脚本退出。"; exit 1; }

echo "当前目录切换到 $(pwd)"

# 安装 Docker 和 Docker Compose
./install_docker.sh

# 安装 Helm 和 Helmfile
./install_helm.sh

# 安装 Kubernetes 工具
./install_k8s.sh

# 切换回到原始工作目录
cd "$CURRENT_DIR" || { echo "无法返回原始目录，脚本退出。"; exit 1; }

echo "所有安装脚本运行完成！"
