# MimirFW Docker 部署指南

> [!IMPORTANT]
>
> MimirFW 的 Docker Compose 配置文件是**自动生成**的，请勿直接修改 `docker-compose.yaml` 文件。
> 如需自定义配置，请修改 `.env.example` 或 `docker-compose-template.yaml` 文件，然后运行生成脚本。

## 🚀 快速开始

### 1. 环境准备
确保您的系统已安装 Docker 和 Docker Compose。

### 2. 配置环境变量
```bash
cd docker
cp .env.example .env
# 根据需要自定义 .env 文件中的配置
```

### 3. 启动服务
```bash
# 启动中间件服务（数据库、缓存等）
docker compose -f docker-compose.middleware.yaml --profile weaviate -p mimirfw up -d

# 启动完整应用栈
docker compose up -d
```

## 📁 配置文件说明

- **`.env.example`**: 环境变量模板文件，包含所有可配置选项
- **`docker-compose-template.yaml`**: Docker Compose 配置模板
- **`docker-compose.middleware.yaml`**: 中间件服务配置（数据库、Redis、向量数据库等）
- **`generate_docker_compose`**: 自动生成脚本，根据模板和环境变量生成最终配置

## 🔧 自定义配置

如需修改 Docker 配置：

1. **环境变量配置**: 编辑 `.env` 文件
2. **服务配置**: 修改 `docker-compose-template.yaml` 模板
3. **重新生成**: 运行 `./generate_docker_compose` 脚本

## 📚 详细说明

更多详细的部署说明和配置选项，请参考：
- [后端 API 服务部署](../api/README.md)
- [前端服务部署](../web/README.md)

## ⚠️ 注意事项

- 不要直接编辑 `docker-compose.yaml` 文件，它会在下次生成时被覆盖
- 所有自定义配置应通过环境变量或模板文件进行
- 生产环境部署前请仔细检查安全配置
