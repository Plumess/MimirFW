#!/bin/bash 

WGET_CMD=$(which wget)

# 检查是否已经安装 Helm
if command -v helm &> /dev/null
then
    echo "Helm 已经安装，跳过安装步骤。"
else
    echo "开始安装 Helm..."

    # 使用 wget 下载并安装 Helm
    $WGET_CMD https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 -O - | bash

    # 验证 Helm 是否成功安装
    if ! command -v helm &> /dev/null
    then
        echo "Helm 安装失败，请检查网络或安装脚本。"
        exit 1
    fi
fi

# 检查是否已经安装 Helmfile
if command -v helmfile &> /dev/null
then
    echo "Helmfile 已经安装，跳过安装步骤。"
else
    echo "开始安装 Helmfile..."

    # 使用 wget 获取 GitHub API 的最新版本号
    LATEST_HELMFILE_VERSION=$(wget -qO- https://api.github.com/repos/helmfile/helmfile/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')

    if [ -z "$LATEST_HELMFILE_VERSION" ]; then
        echo "无法获取 Helmfile 最新版本，请检查网络连接。"
        exit 1
    fi

    echo "最新的 Helmfile 版本为: $LATEST_HELMFILE_VERSION"

    # 使用 wget 下载最新的 Helmfile .tar.gz 文件
    DOWNLOAD_URL="https://github.com/helmfile/helmfile/releases/download/$LATEST_HELMFILE_VERSION/helmfile_${LATEST_HELMFILE_VERSION}_linux_amd64.tar.gz"
    $WGET_CMD $DOWNLOAD_URL -O /tmp/helmfile_linux_amd64.tar.gz

    # 检查下载是否成功
    if [ $? -ne 0 ]; then
        echo "Helmfile 下载失败，请检查网络连接或 URL。"
        exit 1
    fi

    # 解压 Helmfile 文件
    tar -zxvf /tmp/helmfile_linux_amd64.tar.gz -C /tmp

    # 将 Helmfile 移动到 /usr/local/bin 并设置执行权限
    sudo mv /tmp/helmfile /usr/local/bin/helmfile
    sudo chmod +x /usr/local/bin/helmfile

    # 验证 Helmfile 是否成功安装
    if ! command -v helmfile &> /dev/null
    then
        echo "Helmfile 安装失败，请检查文件权限或安装脚本。"
        exit 1
    fi
fi

# 验证安装
echo "Helm 和 Helmfile 安装完成，版本信息如下："
helm version
helmfile --version

echo
echo