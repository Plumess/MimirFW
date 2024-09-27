# 项目 Docker 环境搭建说明

本目录用于项目的 Docker 环境搭建，包含了 LLMCore、Weaviate 和 vLLM 等的服务配置。这些服务可以根据设备的不同硬件进行配置。本 README 将介绍如何构建和启动这些服务。

## 功能概述

- **LLMCore**：用于处理模型的推理和管理的自建镜像。
- **Weaviate**：向量数据库，用于存储和检索嵌入向量，直接 Pull 的官方镜像。
- **vLLM**：主流推理后端，目前本项目支持 CUDA 和 CPU 调用，从官方 Git 仓库获取并通过 Docker 构建。

## 使用指南

1. **环境检测与准备**：脚本会自动检测当前设备的硬件配置，以选择合适的 Dockerfile（如 CPU、CUDA、MPS）。目前仅测试构建了 NVIDIA GPU CUDA 环境，计划支持 CPU 和 Apple M1/M2 芯片。
   
2. **自动化构建**：`build.sh` 脚本将根据检测到的设备类型选择正确的 `Dockerfile` 和 `docker-compose.override`，自动构建所需的 Docker 镜像，启动服务，并使用自定义 Docker 网络 `mimirnet` 进行通信。

3. **vLLM 仓库自动获取**：脚本会检测 `vLLM` 目录是否存在并且是否为有效的 Git 仓库，如果无效或缺失，将会从官方仓库拉取指定版本。当设备不选择 CUDA/CPU 时，暂不构建 vLLM。

### 项目结构

```
Docker/
├── LLMCore/
│   ├── Dockerfile
│   ├── Dockerfile.cpu
│   ├── Dockerfile.mps
│   ├── llmcore.env
│   ├── requirements-cpu.txt
│   ├── requirements-cuda.txt
│   ├── requirements-mps.txt
│   └── requirements.txt
├── Weaviate/
│   ├── data/
│   ├── Dockerfile
│   ├── weaviate.env
├── vLLM/
│   └── # 官方 Git 仓库的内容
├── .env
├── build.sh
├── docker-compose.override.cpu.yml
├── docker-compose.override.cuda.yml
├── docker-compose.override.mps.yml
└── docker-compose.yml
```

## 使用步骤

1. **进入 Docker 目录**：

   ```bash
   cd Docker
   ```

2. **配置环境变量**：根据 `.env` 文件配置相应的服务版本和路径。

3. **运行构建脚本**：

   ```bash
   ./build.sh
   ```

   脚本将会：
   - 自动检测设备类型（CPU、CUDA、MPS）
   - 自动获取 vLLM 仓库（如果不存在）
   - 根据设备类型选择合适的 `docker-compose` 配置文件，构建并启动服务

4. **访问端口(宿主机)**：
   - Docker 网络内请直接使用容器名:默认端口进行通信
   - LLMCore 服务默认端口：`24910`
   - Weaviate 服务默认端口：`24980` (HTTP) 和 `50052` (gRPC)
   - vLLM 服务默认端口：`24900`

5. **关闭服务**：

   ```bash
   docker-compose down
   ```