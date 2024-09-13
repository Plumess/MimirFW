# ==============================
# 基础阶段: 使用 LangChain 基础镜像
# ==============================
FROM langchain/langchain:latest AS base

# 维护者信息
LABEL maintainer="Plumess"

# 设置工作目录
WORKDIR /app

# 复制 LLM 代码到工作目录
COPY ../../LLMCore /app/LLMCore

# 安装基础依赖
RUN pip install --upgrade pip

# ==============================
# 开发/测试阶段: 包含开发工具和依赖
# ==============================
FROM base AS development

# 安装开发环境的额外依赖

# ==============================
# 生产阶段: 最终的轻量化运行环境
# ==============================
FROM base AS production

# 仅安装生产所需依赖

# 示意暴露服务端口（并未实际映射）
EXPOSE 24910