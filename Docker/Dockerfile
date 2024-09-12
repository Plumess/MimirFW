# ==============================
# 基础阶段: 使用 LangChain 基础镜像
# ==============================
FROM langchain/langchain:latest AS base

# 维护者信息
LABEL maintainer="Plumess"

# 设置环境变量
ENV LANGCHAIN_ENV=development \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 设置工作目录
WORKDIR /app

# 安装基础依赖
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r /app/requirements.txt

# ==============================
# 阶段 1: LLM 应用搭建
# ==============================
FROM base AS llm_stage

# 复制 LLM 代码到工作目录
COPY ../LLMCore /app/LLMCore

# 安装 LLM 相关的依赖
# 向量数据库 faiss
RUN pip install faiss-gpu

# 暴露 LLM 相关服务的端口
# EXPOSE 5000

# ==============================
# 阶段 2: 游戏逻辑搭建
# 从 llm_stage 基础上构建
# ==============================
FROM llm_stage AS game_logic_stage

# 复制游戏逻辑代码到工作目录
COPY ../GameLogic /app/GameLogic

# 安装游戏逻辑相关的依赖
# RUN pip install game_logic_package  # 示例依赖，替换为你的游戏逻辑依赖

# 暴露游戏逻辑相关服务的端口
# EXPOSE 5001

# ==============================
# 阶段 3: 对外交互的 Adapter 搭建
# 从 game_logic_stage 基础上构建
# ==============================
FROM game_logic_stage AS adapter_stage

# 复制对外交互 Adapter 代码到工作目录
COPY ../Adapter /app/Adapter

# 安装对外交互（API、前端框架、QQ 机器人等）的依赖
# RUN npm install --global frontend-framework && pip install qq-bot-api-package  # 示例依赖，替换为你的 Adapter 依赖

# 暴露对外交互 Adapter 的服务端口
# EXPOSE 5002

# ==============================
# 综合阶段: 完整构建所有内容
# ==============================
FROM adapter_stage AS full_build

# 确保所有依赖和代码已安装
# 因为 adapter_stage 已包含前面所有内容，所以无需再复制和安装
# 此处只需要添加其他非开发的环境即可，例如应用部署需要用到的环境（如果有）

# 暴露所有服务端口
# EXPOSE 5000 5001 5002

# 设置综合阶段的默认启动命令（可选）
# CMD ["python", "main.py"] 或者其他多服务启动命令
