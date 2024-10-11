#!/bin/bash

# 检查是否已经安装 Docker
if command -v docker &> /dev/null
then
    echo "Docker 已经安装，跳过安装步骤。"
else
    echo "开始安装 Docker..."

    # 检查操作系统类型
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    else
        echo "无法检测操作系统类型，脚本退出。"
        exit 1
    fi

    # 安装 Docker
    if [[ "$OS" == "ubuntu" ]]; then
        sudo apt-get update -y
        sudo apt-get install -y ca-certificates wget gnupg lsb-release
        wget -qO- https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update -y
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    elif [[ "$OS" == "almalinux" || "$OS" == "centos" || "$OS" == "rhel" || "$OS" == "fedora" ]]; then
        sudo dnf remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
        sudo dnf install -y dnf-plugins-core
        sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo dnf install -y docker-ce docker-ce-cli containerd.io
    else
        echo "暂不支持的操作系统：$OS"
        exit 1
    fi

    sudo systemctl start docker
    sudo systemctl enable docker
fi

# 检查是否已经安装 Docker Compose
if command -v docker-compose &> /dev/null
then
    echo "Docker Compose 已经安装，跳过安装步骤。"
else
    echo "开始安装 Docker Compose..."

    # 安装最新版本的 Docker Compose
    LATEST_COMPOSE_VERSION=$(wget -qO- https://github.com/docker/compose/releases/latest | grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+')
    sudo wget -O /usr/local/bin/docker-compose "https://github.com/docker/compose/releases/download/${LATEST_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)"
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 检查用户是否在 docker 组中
if groups $USER | grep &>/dev/null '\bdocker\b'; then
    echo "用户 $USER 已经在 docker 组中，跳过用户组配置。"
else
    echo "将用户 $USER 添加到 docker 组中..."
    sudo usermod -aG docker $USER
    echo "请重新登录当前 shell 会话，或者运行 'newgrp docker' 以使更改生效。"
fi

# 输出版本信息
docker --version
docker-compose --version

echo
echo
