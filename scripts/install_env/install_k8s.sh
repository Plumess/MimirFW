#!/bin/bash

# 设置临时目录
TMP_DIR="/tmp/k8s_install"
mkdir -p "$TMP_DIR"

# 检查组件是否已经安装
check_installation() {
    if command -v "$1" &> /dev/null
    then
        echo "$1 已经安装，跳过安装。"
        return 0
    else
        return 1
    fi
}

# 自动检测操作系统类型
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS_FAMILY=$ID
        OS_VERSION=$VERSION_ID

        if [[ "$OS_FAMILY" == "ubuntu" || "$OS_FAMILY" == "debian" ]]; then
            OS_TYPE="debian"
        elif [[ "$OS_FAMILY" == "almalinux" || "$OS_FAMILY" == "centos" || "$OS_FAMILY" == "rhel" || "$OS_FAMILY" == "fedora" ]]; then
            OS_TYPE="redhat"
        else
            echo "不支持的操作系统：$OS_FAMILY"
            exit 1
        fi
    else
        echo "无法检测操作系统类型，退出。"
        exit 1
    fi
}

# 获取最新的 Kubernetes 次要版本号，例如 1.31
get_latest_k8s_minor_version() {
    echo "获取最新的 Kubernetes 版本..."
    LATEST_K8S_VERSION=$(wget -qO- https://dl.k8s.io/release/stable.txt)
    if [ -z "$LATEST_K8S_VERSION" ]; then
        echo "无法获取最新的 Kubernetes 版本，退出。"
        exit 1
    fi
    echo "最新的 Kubernetes 版本是 $LATEST_K8S_VERSION"
    # 提取次要版本号，例如 v1.31.2 -> 1.31
    K8S_VERSION_MINOR=$(echo "$LATEST_K8S_VERSION" | cut -d '.' -f1,2 | sed 's/v//')
    echo "使用的 Kubernetes 次要版本是 $K8S_VERSION_MINOR"
}

# 安装 kubelet、kubeadm 和 kubectl
install_kubernetes_components() {
    check_installation "kubectl"
    check_installation "kubeadm"
    check_installation "kubelet"
    if [ $? -eq 0 ]; then
        echo "Kubernetes 组件已经安装，跳过安装。"
        return 0
    fi

    echo "开始安装 Kubernetes 组件（kubelet、kubeadm、kubectl）..."

    detect_os
    get_latest_k8s_minor_version

    if [[ "$OS_FAMILY" == "ubuntu" || "$OS_FAMILY" == "debian" ]]; then
        echo "检测到基于 Debian 的发行版 ($OS_FAMILY)..."

        # 更新 apt 包索引，并安装所需的包
        sudo apt-get update
        sudo apt-get install -y apt-transport-https ca-certificates gnupg lsb-release wget

        # 添加 Kubernetes 的 GPG 密钥（覆盖已存在的文件）
        sudo mkdir -p -m 755 /etc/apt/keyrings
        wget -qO- https://pkgs.k8s.io/core:/stable:/v${K8S_VERSION_MINOR}/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

        # 添加 Kubernetes apt 仓库
        echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v${K8S_VERSION_MINOR}/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
        sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list

        # 更新 apt 包索引
        sudo apt-get update

        # 安装最新版本的 kubelet、kubeadm、kubectl
        sudo apt-get install -y kubelet kubeadm kubectl

        # 锁定版本，防止意外升级
        sudo apt-mark hold kubelet kubeadm kubectl

    elif [[ "$OS_FAMILY" == "almalinux" || "$OS_FAMILY" == "centos" || "$OS_FAMILY" == "rhel" || "$OS_FAMILY" == "fedora" ]]; then
        echo "检测到基于 Red Hat 的发行版 ($OS_FAMILY)..."

        # 安装所需的包
        sudo yum install -y yum-utils

        # 添加 Kubernetes 的 yum 仓库
        sudo tee /etc/yum.repos.d/kubernetes.repo <<EOF >/dev/null
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v${K8S_VERSION_MINOR}/rpm/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v${K8S_VERSION_MINOR}/rpm/repodata/repomd.xml.key
EOF

        # 清理并更新 yum 缓存
        sudo yum clean all
        sudo yum makecache

        # 安装最新版本的 kubelet、kubeadm、kubectl
        sudo yum install -y kubelet kubeadm kubectl

        # 启用 kubelet 服务
        sudo systemctl enable kubelet

    else
        echo "不支持的操作系统：$OS_FAMILY"
        exit 1
    fi

    echo "Kubernetes 组件安装完成。"
}

# 安装 cri-dockerd（Docker 运行时接口）
install_cri_dockerd() {
    # 检查 cri-dockerd 是否已经安装
    check_installation "cri-dockerd"
    if [ $? -eq 0 ]; then
        return 0
    fi

    echo "开始安装 cri-dockerd..."

    # 获取 cri-dockerd 最新版本号
    CRI_DOCKERD_VERSION=$(wget -qO- https://api.github.com/repos/Mirantis/cri-dockerd/releases/latest | grep -Po '"tag_name": "\K[^\"]+')
    if [ -z "$CRI_DOCKERD_VERSION" ]; then
        echo "无法获取 cri-dockerd 版本号，退出。"
        exit 1
    fi
    # 移除版本中的"v"前缀用于下载链接
    CRI_DOCKERD_VERSION_NO_V=$(echo $CRI_DOCKERD_VERSION | sed 's/v//')

    # 下载并安装 cri-dockerd
    wget -O "$TMP_DIR/cri-dockerd.tgz" "https://github.com/Mirantis/cri-dockerd/releases/download/$CRI_DOCKERD_VERSION/cri-dockerd-$CRI_DOCKERD_VERSION_NO_V.amd64.tgz"

    if [ $? -ne 0 ]; then
        echo "cri-dockerd 下载失败，请检查版本号或网络连接。"
        exit 1
    fi

    # 解压并安装
    sudo tar zxvf "$TMP_DIR/cri-dockerd.tgz" -C /usr/local/bin
    echo "cri-dockerd 安装完成"

    # 下载并配置 cri-dockerd 的 systemd 服务
    wget -O /etc/systemd/system/cri-docker.service https://raw.githubusercontent.com/Mirantis/cri-dockerd/master/packaging/systemd/cri-docker.service
    wget -O /etc/systemd/system/cri-docker.socket https://raw.githubusercontent.com/Mirantis/cri-dockerd/master/packaging/systemd/cri-docker.socket

    # 重新加载 systemd，并启用 cri-dockerd 服务
    sudo systemctl daemon-reload
    sudo systemctl enable cri-docker.service
    sudo systemctl start cri-docker.service

    echo "cri-dockerd 安装完成并已启动"
}

# 安装最新的 crictl 工具
install_crictl() {
    # 检查 crictl 是否已经安装
    check_installation "crictl"
    if [ $? -eq 0 ]; then
        return 0
    fi

    # 获取最新的 crictl 版本号
    echo "获取最新的 crictl 版本..."
    CRICTL_VERSION=$(wget -qO- https://api.github.com/repos/kubernetes-sigs/cri-tools/releases/latest | grep -Po '"tag_name": "\K[^\"]+')

    if [ -z "$CRICTL_VERSION" ]; then
        echo "无法获取 crictl 版本，请检查网络连接。"
        exit 1
    fi

    echo "最新的 crictl 版本是 $CRICTL_VERSION"

    # 下载并安装最新版本的 crictl
    echo "开始安装 crictl ..."
    wget -O "$TMP_DIR/crictl.tar.gz" "https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-amd64.tar.gz"

    if [ $? -ne 0 ]; then
        echo "crictl 下载失败，请检查版本号或网络连接。"
        exit 1
    fi

    sudo tar zxvf "$TMP_DIR/crictl.tar.gz" -C /usr/local/bin
    echo "crictl 安装完成"
}

# 禁用 Swap
disable_swap() {
    sudo swapoff -a
    sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
}

# 为 kubelet 创建临时配置（在 kubeadm init 之前）
configure_kubelet_before_init() { 
    echo "为 kubelet 创建临时配置..."

    # 获取 Docker 的 cgroup 驱动程序
    CGROUP_DRIVER=$(docker info | grep -i 'Cgroup Driver' | awk '{print $3}')
    echo "Docker 使用的 cgroup 驱动程序是 $CGROUP_DRIVER"

    # 创建 kubelet 配置目录
    sudo mkdir -p /var/lib/kubelet

    # 创建 kubelet 配置文件
    sudo tee /var/lib/kubelet/config.yaml <<EOF
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
cgroupDriver: "$CGROUP_DRIVER"
containerRuntimeEndpoint: "unix:///var/run/cri-dockerd.sock"
kubeconfig: "/etc/kubernetes/kubelet.conf"
authentication:
  x509:
    clientCAFile: "/etc/kubernetes/pki/ca.crt"
authorization:
  mode: Webhook
EOF

    # 配置 kubelet 使用 cri-dockerd 并通过配置文件加载参数
    sudo mkdir -p /etc/systemd/system/kubelet.service.d

    # 删除可能存在的旧配置文件
    sudo rm -f /etc/systemd/system/kubelet.service.d/10-cri-dockerd.conf

    # 设置 kubelet 的环境变量，使用 --config 加载配置文件
    sudo tee /etc/systemd/system/kubelet.service.d/10-kubeadm.conf <<EOF
[Service]
Environment="KUBELET_KUBEADM_ARGS=--container-runtime-endpoint=unix:///var/run/cri-dockerd.sock --config=/var/lib/kubelet/config.yaml --kubeconfig=/etc/kubernetes/kubelet.conf"
EOF

    # 确保 Kubelet 使用正确的 kubeconfig 文件来和 API server 通信
    if [ -f /lib/systemd/system/kubelet.service ]; then
        sudo sed -i '/ExecStart=/c ExecStart=/usr/bin/kubelet $KUBELET_KUBEADM_ARGS' /lib/systemd/system/kubelet.service
        sudo sed -i '/EnvironmentFile=/c EnvironmentFile=-/etc/systemd/system/kubelet.service.d/10-kubeadm.conf' /lib/systemd/system/kubelet.service
    fi

    # 重新加载 systemd 并重启 kubelet
    sudo systemctl daemon-reload
    sudo systemctl restart kubelet
}

# 初始化 Kubernetes 集群
init_k8s_cluster() {
    echo "停止 kubelet 服务..."
    sudo systemctl stop kubelet || true

    echo "禁用 Swap..."
    disable_swap

    echo "重置 Kubernetes 集群..."
    sudo kubeadm reset -f --cri-socket unix:///var/run/cri-dockerd.sock

    echo "清理残留的配置和数据..."
    sudo rm -rf /etc/cni/net.d
    sudo iptables -F
    sudo ipvsadm --clear || true
    sudo rm -rf $HOME/.kube/config
    sudo rm -rf /etc/kubernetes/pki

    # 预拉取 Kubernetes 所需镜像
    echo "预先拉取 kubeadm 所需的镜像..."
    sudo kubeadm config images pull --cri-socket unix:///var/run/cri-dockerd.sock

    echo "开始初始化 Kubernetes 集群..."
    sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --cri-socket unix:///var/run/cri-dockerd.sock

    if [ $? -ne 0 ]; then
        echo "Kubernetes 集群初始化失败。请检查日志并手动解决问题。"
        exit 1
    fi

    echo "Kubernetes 集群初始化完成。"
}

# 配置 kubectl 来管理集群
configure_kubectl() {
    if [ ! -f /etc/kubernetes/admin.conf ]; then
        echo "/etc/kubernetes/admin.conf 文件不存在，可能是集群初始化失败。"
        exit 1
    fi

    mkdir -p $HOME/.kube
    sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    # 确保 /usr/bin 在 PATH 中优先于 /usr/local/bin
    if ! grep -q 'export PATH=/usr/bin:$PATH' $HOME/.bashrc; then
        echo 'export PATH=/usr/bin:$PATH' >> $HOME/.bashrc
    fi

    # 使更改立即生效
    export PATH=/usr/bin:$PATH
}

# 安装 Flannel 网络插件
install_flannel() {
    echo "开始配置 Flannel 网络插件..."
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
}

# 删除临时文件
cleanup() {
    echo "清理临时文件..."
    rm -rf "$TMP_DIR"
}

# 主执行流程
install_kubernetes_components
install_cri_dockerd
install_crictl
disable_swap

configure_kubelet_before_init

init_k8s_cluster

configure_kubectl
install_flannel

cleanup

echo "所有安装脚本运行完成！"

kubectl version --client
kubectl get nodes
kubectl get pods -A
