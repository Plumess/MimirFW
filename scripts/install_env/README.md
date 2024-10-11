# 环境安装说明

本安装脚本支持在常见的服务器Linux发行版上安装必要的开发和部署环境，主要包括：

- Docker
- Docker Compose
- Helm
- Helmfile
- Kubernetes

## 支持的系统

- Ubuntu (Debian) 18.04, 20.04, 22.04 & New
- AlmaLinux (Red Hat/RHEL) 8.x, 9.x

## 安装步骤

1. 赋予安装脚本可执行权限：
   ```bash
   chmod +x install.sh
   ```

2. 执行一键安装脚本：
   ```bash
   ./install.sh
   ```

4. 安装完成后，Docker、Compose、Helm、Helmfile、Kubernetes 即可以使用，且不需要sudo。

## 脚本内容概述

- `install_docker.sh`：**未测试！** 安装 Docker 和 Docker Compose，并配置用户权限避免使用 sudo。

- `install_helm.sh`：**未测试 RHEL！** 安装 Helm 及 Helmfile。

- `install_k8s.sh`：**未测试 RHEL！** 

   - 针对不同的系统类型安装 Kubernetes 集群组件：

      - Debian/Ubuntu 系：通过 apt-get 安装 kubelet、kubeadm、kubectl。

      - Red Hat 系：通过 yum 安装相同的组件。

   - 安装 cri-dockerd： 安装并配置 Docker 作为 Kubernetes 的容器运行时。

   - 安装 Flannel 网络插件： 安装 Flannel 作为 Kubernetes 集群的 CNI 插件，提供 Pod 网络通信功能。
   
   - 集群初始化： 使用 kubeadm init 初始化 Kubernetes 集群，并配置 kubectl 管理集群。

- `install.sh`：一键执行上述所有安装脚本。
