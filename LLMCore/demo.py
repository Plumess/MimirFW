from config import WEAVIATE_URL, WEAVIATE_PORT, PROJECT_ROOT
from LLMCore.utils.model_selecter import get_all_models

import os
import torch
import weaviate
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def main():
    # 检查可用设备
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"可用设备：{device}")

    # 1. 获取所有可用的模型
    print("获取可用的大模型和embedding模型...")
    models = get_all_models()
    large_model_info = models['large_models'][0]
    embedding_model_info = models['embedding_models'][0]

    large_model_path = large_model_info['path']
    embedding_model_path = embedding_model_info['path']

    print(f"使用的大模型: {large_model_info['name']}")
    print(f"使用的embedding模型: {embedding_model_info['name']}")

    # 初始化 weaviate_client 为 None
    weaviate_client = None

    try:
        # 2. 加载大模型
        print(f"加载大模型 '{large_model_info['name']}'...")
        tokenizer = AutoTokenizer.from_pretrained(large_model_path)

        # 使用 device_map="auto" 和 torch_dtype 确保模型在 GPU 上加载
        model = AutoModelForCausalLM.from_pretrained(
            large_model_path,
            device_map="auto" if device == "cuda" else None,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True  # 这个参数在处理量化模型时很有用
        )

        llm_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=1024,  # 限制全文的token长度（包含输入和回答）
            max_new_tokens=512,  # 设置回答生成的长度
            truncation=True
        )
        llm = HuggingFacePipeline(pipeline=llm_pipeline)
        print("大模型加载完毕。")

        # 3. 加载embedding模型
        print(f"加载embedding模型 '{embedding_model_info['name']}'...")
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_path)
        print("embedding模型加载完毕。")

        # 4. 连接 Weaviate 向量数据库
        # https://weaviate.io/developers/weaviate/connections
        print(f"尝试连接 Weaviate 数据库，URL: http://{WEAVIATE_URL}:{WEAVIATE_PORT}...")
        weaviate_client = weaviate.connect_to_local(
            host=WEAVIATE_URL,  # Use a string to specify the host
            port=WEAVIATE_PORT,
            grpc_port=50051,
        )
        print("成功连接到 Weaviate 数据库。")

        # 5. 定义模板化输出
        print("定义模板化输出...")
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="请根据以下问题提供详细的回答：{question}"
        )
        # 创建可运行的序列
        chain = prompt_template | llm
        print("模板化输出定义完毕。")

        # 示例输入
        question = "请介绍一下LangChain的主要功能。"
        text_path = os.path.join(PROJECT_ROOT, 'LLMCore/test_data.txt')

        # 6. 检索向量数据库中的内容
        # https://python.langchain.com/docs/integrations/vectorstores/weaviate/
        print("检索向量数据库中的相关内容...")

        # 先加载并处理文档
        loader = TextLoader(text_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        # 然后创建向量存储
        db = WeaviateVectorStore.from_documents(docs, embedding=embeddings, client=weaviate_client)

        # 执行相似度搜索
        retrieved_docs = db.similarity_search(question)

        if not retrieved_docs:
            print("向量数据库中没有找到相关内容，使用空上下文。")
            context = ""
        else:
            print(f"检索到 {len(retrieved_docs)} 条相关内容。")
            # 将检索到的文档内容合并
            context = "\n".join([doc.page_content for doc in retrieved_docs])

        # 7. 使用模型生成响应
        print("使用模型生成响应...")
        if context:
            # 更新提示模板，包含上下文
            prompt_with_context = PromptTemplate(
                input_variables=["context", "question"],
                template="基于以下内容：\n{context}\n\n\n请回答问题：{question}"
            )
            chain_with_context = prompt_with_context | llm
            response = chain_with_context.invoke({"context": context, "question": question})
        else:
            # 无上下文时直接生成响应
            response = chain.invoke({"question": question})

        print("模型响应：")
        print(response)

    except Exception as e:
        print(f"运行时发生错误: {e}")
    
    finally:
        # 确保 Weaviate 客户端连接被关闭
        if weaviate_client is not None:
            weaviate_client.close()
            print("Weaviate 客户端连接已关闭。")

if __name__ == "__main__":
    main()

# python LLMCore/demo.py > ./LLMCore/logs/demo0914.log
