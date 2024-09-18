from config import WEAVIATE_URL, WEAVIATE_PORT, PROJECT_ROOT, DEVICE_INFO
from LLMCore.managers.utils.model_selecter import get_all_models
from LLMCore.managers.model_loader import load_model

import os
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def main():
    # 使用封装好的 DEVICE_INFO
    print("=" * 50)
    print(f"设备信息：{DEVICE_INFO}")
    print("=" * 50)

    # 1. 获取所有可用的模型
    print("获取可用的大模型和 embedding 模型...")
    models = get_all_models()
    large_model_info = models['large_models'][0]
    embedding_model_info = models['embedding_models'][0]

    large_model_path = large_model_info['path']
    embedding_model_path = embedding_model_info['path']

    print(f"使用的大模型: {large_model_info['name']}")
    print(f"使用的 embedding 模型: {embedding_model_info['name']}")
    print("=" * 50)

    # 初始化 weaviate_client 为 None
    weaviate_client = None

    try:
        # 2. 加载模型和 embeddings
        print(f"加载模型中...")
        model_loader = load_model(large_model_path, embedding_model_path, max_new_tokens=512)
        model_loader.load_llm()
        llm = model_loader.get_llm()
        model_loader.load_embeddings()
        embeddings = model_loader.get_embeddings()
        print("模型加载完毕。")
        print("=" * 50)

        # 3. 连接 Weaviate 向量数据库
        # https://weaviate.io/developers/weaviate/connections
        print(f"尝试连接 Weaviate 数据库，URL: http://{WEAVIATE_URL}:{WEAVIATE_PORT}...")
        weaviate_client = weaviate.connect_to_local(
            host=WEAVIATE_URL,
            port=WEAVIATE_PORT,
            grpc_port=50051,
        )
        print("成功连接到 Weaviate 数据库。")
        print("=" * 50)

        # 4. 定义模板化输出
        print("定义模板化输出...")
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="请根据以下问题提供详细的回答：{question}"
        )
        # 创建可运行的序列
        chain = prompt_template | llm
        print("模板化输出定义完毕。")
        print("=" * 50)

        # 示例输入
        question = "请介绍一下LangChain的主要功能。"
        text_path = os.path.join(PROJECT_ROOT, 'LLMCore/test_data.txt')

        # 5. 检索向量数据库中的内容
        # https://python.langchain.com/docs/integrations/vectorstores/weaviate/
        print("检索向量数据库中的相关内容...")

        # 加载并处理文档
        loader = TextLoader(text_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        # 创建向量存储
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

        # 6. 使用模型生成响应
        print("\n使用模型生成响应...")
        # 设置最大展示长度
        max_display_length = 200  # 展示的最大字符数
        display_context = context[:max_display_length]  # 截取用于展示的部分

        if context:
            # 更新提示模板，包含截取后的展示部分
            prompt_with_context = PromptTemplate(
                input_variables=["display_context", "question"],
                template="基于以下数据库内容：\n{display_context}\n……\n回答问题：\n{question}"
            )
            chain_with_context = prompt_with_context | llm
            # 调用模型时，传递完整的 context
            response = chain_with_context.invoke({"display_context": display_context, "question": question, "context": context})
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
            print()
            print("Weaviate 客户端连接已关闭。")
            print("=" * 50)
            print()

if __name__ == "__main__":
    main()

# python LLMCore/demo.py > ./LLMCore/logs/demo0914.log