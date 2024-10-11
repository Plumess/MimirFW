# syntax=docker/dockerfile:1.4

FROM vllm/vllm-openai:latest

# 维护者信息
LABEL maintainer="Plumess"

# vllm 官方镜像 默认工作路径
WORKDIR /workspace

# 复制自定义嵌入模型推理 API 目录
COPY ./emb /emb

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /emb/requirements.txt

# 复制定制的启动脚本
COPY entrypoint_custom.sh /entrypoint_custom.sh
RUN chmod +x /entrypoint_custom.sh

# 设置自定义的 ENTRYPOINT
ENTRYPOINT ["/entrypoint_custom.sh"]
