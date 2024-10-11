# 项目 Docker 环境搭建说明

本目录用于项目的 Docker 环境搭建，包含了 LLMCore 等的服务配置。这些服务可以根据设备的不同硬件进行配置。本 README 将介绍如何构建和启动这些服务。

## 功能概述

- **LLMCore**：用于处理模型的推理和管理的自建镜像。
- **Weaviate**：向量数据库，用于存储和检索嵌入向量，直接 Pull 的官方镜像。
- **vLLM-Emb**：模型后端推理，基于 vLLM 推理大模型 和 自定义的 Sentence-transformers API 推理嵌入模型

## 使用指南

1. **环境检测与准备**：脚本会自动检测当前设备的硬件配置，以选择合适的 Dockerfile（如 CPU、CUDA）。目前仅构建了 NVIDIA GPU CUDA 和 CPU 环境。
   
2. **自动化构建**：`build.sh` 脚本将根据检测到的设备类型选择正确的 `Dockerfile` 和 `docker-compose.override`，自动构建所需的 Docker 镜像，启动服务，并使用自定义 Docker 网络 `mimirnet` 进行通信。

### 项目结构

```
Docker/
├── LLMCore/
│   ├── Dockerfile
│   ├── Dockerfile.cpu
│   ├── llmcore.env
│   ├── requirements-cpu.txt
│   ├── requirements-cuda.txt
│   └── requirements.txt
├── vLLM-Emb/
│   ├── Dockerfile
│   ├── emb/
│   │    ├── emb.py
│   │    └── requirements.txt
│   ├── entrypoint_custom.sh
│   ├── requirements.txt
│   └── README.md
├── Weaviate/
│   ├── data/
│   ├── Dockerfile
│   └── weaviate.env
├── .env
├── build.sh
├── run.sh
├── docker-compose.override.cuda.yml
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
   ./run.sh
   ```

   脚本将会：
   - 自动检测设备类型（CPU、CUDA）
   - 根据设备类型选择合适的 `docker-compose` 配置文件，构建并启动服务

4. **访问端口(宿主机)**：
   - Docker 网络内请直接使用容器名:默认端口进行通信
   - LLMCore 服务默认端口：`24910`
   - Weaviate 服务默认端口：`24980` (HTTP) 和 `50052` (gRPC)
   - vLLM 服务默认端口：`24102`
   - Sentence-transformer 后端：`24101`

5. **关闭服务**：

   ```bash
   docker-compose down
   ```