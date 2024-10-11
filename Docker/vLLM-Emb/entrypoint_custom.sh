#!/bin/bash

# 启动 vLLM 服务（假设模型名称和端口）
python3 -m vllm.entrypoints.openai.api_server --model ${VLLM_MODEL:-/models/Qwen2.5-7B-Instruct-AWQ} --port ${VLLM_PORT:-8000} --download_dir="/models" &

# 等待 vLLM 服务启动（可选，根据需要调整）
sleep 5

# 启动嵌入模型 FastAPI 服务
cd /emb
uvicorn emb:app --host 0.0.0.0 --port ${EMB_PORT:-24101} >> /embeddings-api.log 2>&1

# 保持容器运行
wait -n
exit $?

