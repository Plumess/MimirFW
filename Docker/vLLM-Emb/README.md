# vLLM-Emb

**vLLM-Emb** 是本项目自定义的基于 vLLM 官方镜像的 Docker 镜像，添加了自定义的嵌入模型推理后端。该项目旨在提供一个统一的接口，支持大语言模型和嵌入模型的异步推理，以便于在 LangChain 等框架中集成使用。

## 项目内容

### 1. 自定义嵌入模型异步推理响应函数

- **使用 FastAPI 定制 API 后端**：利用 FastAPI 构建高性能的异步 API 服务，作为嵌入模型的推理后端。

- **编写响应 API，自定义 LangChain 中的 Embeddings 需求**：实现符合 LangChain 要求的自定义接口 `SentenceTransformersEmbeddings`，使其能够调用嵌入模型自定义 API 服务。

- **基于 Sentence-Transformers 库，支持异步响应**：后端 API 采用 Sentence-Transformers 提供的预训练嵌入模型，自动检测运行环境中的设备类型，支持高效的文本向量化，并通过异步方式提高响应速度。

### 2. 基于 vLLM 的大模型异步推理响应函数

- **GPU 推理，兼容 OpenAI API**：利用 vLLM 后端实现大语言模型的高性能推理，兼容 OpenAI API 接口，方便在 LangChain 中使用 `ChatOpenAI` 等组件进行调用。

- **自动设备识别，支持 CPU 推理**：vLLM 官方镜像能够自动检测运行环境中的设备类型，如果没有可用的 GPU，将自动切换到 CPU 推理模式。

## 使用说明

- **嵌入模型服务**

  - 服务地址：`http://localhost:8000/embeddings`
  - 接口为**仿写** HuggingFaceEmbeddings 的自定义 LangChain 集成 `SentenceTransformersEmbeddings`

- **大模型服务**

  - 服务地址：`http://localhost:8000/v1`
  - 接口兼容 OpenAI API，可以使用 LangChain 中的 `ChatOpenAI` 或 `VLLMOpenAI` 组件进行调用
  - 基于本地模型推理，不需要提供 `openai_api_key`

### 与 LangChain 集成

- **嵌入模型**

    ```python
    from LLMCore.customs.langchain_embeddings import SentenceTransformersEmbeddings

    embeddings = SentenceTransformersEmbeddings(
            model_name=embedding_source,  # 本地模型名称
            api_url=emb_url  # 自定义的 FastAPI URL
            # 其他支持的参数
        )
    ```

- **大模型（Chat Models）**

    ```python
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_core.prompts.chat import (
        ChatPromptTemplate,
        HumanMessagePromptTemplate,
        SystemMessagePromptTemplate,
    )
    from langchain_openai import ChatOpenAI

    inference_server_url = "http://localhost:8000/v1"

    llm = ChatOpenAI(
        model="/models/Qwen2.5-7B-Instruct-AWQ",  # 容器内本地模型绝对路径
        openai_api_key="EMPTY",
        openai_api_base=inference_server_url,
        max_tokens=512,
        temperature=0,
        # 其他支持的参数
    )
    ```

## 测试 Demo

参考 [vllm-emb.py](../../LLMCore/test/vllm-emb.py)

## 参考链接

- **LangChain vLLM 集成及其用法**：
  - [vLLM LangChain LLMs 集成文档](https://python.langchain.com/docs/integrations/llms/vllm/)
  - [vLLM LangChain ChatModels 集成文档](https://python.langchain.com/docs/integrations/chat/vllm/)

- **Sentence-Transformers**：[Sentence-Transformers 官网](https://www.sbert.net/)

- **FastAPI**：[FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)

## 项目结构

```
vllm-emb/
├── Dockerfile                # 基于 vLLM 官方镜像的自定义构建文件
├── emb/                      # 包含嵌入模型的 FastAPI 接口实现
│    ├── emb.py               # FastAPI 接口定义文件
│    └── requirements.txt     # 嵌入模型推理依赖
├── entrypoint_custom.sh      # 自定义的容器启动入口
├── requirements.txt          # 依赖包列表
└── README.md                 # 项目说明文档
```

## 常见问题

### **如何切换模型？**

vLLM 在容器启动时，默认会启动一个模型，但可以在调用的时候通过以下方式动态指定请求的模型：

``` python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="/models/Qwen2.5-7B-Instruct-AWQ", # 此处指定容器内绝对路径
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:8000/v1",
    # 其他支持的参数
)
```

### **在没有 GPU 的环境下性能如何？**

在 CPU 环境下，推理速度会较慢，适合测试和开发环境。建议在生产环境中使用 GPU 以获得最佳性能。
