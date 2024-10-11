import os
import weaviate
import requests
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from langchain_openai import ChatOpenAI
from LLMCore.customs.langchain_embeddings import SentenceTransformersEmbeddings

from config import *

chat_url = "http://vllm-emb:8000/v1"
emb_url = "http://vllm-emb:24101/embeddings"

def demo(embedding_source, llm_source):
    try:
        # 1. 初始化自定义 SentenceTransformersEmbeddings 和 TransformersChatModels 类
        embeddings = SentenceTransformersEmbeddings(
            model_name=embedding_source,  # 本地模型名称
            api_url=emb_url  # 自定义的 FastAPI URL
            # 其他支持的参数
        )
        llm = ChatOpenAI(
            model=llm_source,
            openai_api_key="EMPTY",
            openai_api_base=chat_url,
            max_tokens=512,
            temperature=0,
            # 其他支持的参数
        )
        print("自定义模型加载完毕。")
        print("=" * 50)

        # 2. 连接 Weaviate 向量数据库
        print(f"尝试连接 Weaviate 数据库，URL: http://weaviate:8080...")
        weaviate_client = None
        # https://weaviate.io/developers/weaviate/connections
        weaviate_client = weaviate.connect_to_local(
            host="weaviate",
            port=8080,
            grpc_port=50051,
        )
        print("成功连接到 Weaviate 数据库。")
        print("=" * 50)

        # 3. 定义模板和输出解析器
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="请根据以下问题提供详细的回答：{question}"
        )
        parser = StrOutputParser()
        print("模板化输出和解析器定义完毕。")
        print("=" * 50)

        # 4. 加载并处理文档
        text_path = os.path.join(PROJECT_ROOT, 'LLMCore/test/test_data.txt')
        loader = TextLoader(text_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        # 5. 创建向量存储
        db = WeaviateVectorStore.from_documents(docs, embedding=embeddings, client=weaviate_client)
        print("向量存储创建完毕。")
        print("=" * 50)

        # 6. 执行相似度搜索
        question = "请介绍一下LangChain的主要功能。"
        retrieved_docs = db.similarity_search(question)
        context = "\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""
        print(f"检索到 {len(retrieved_docs)} 条相关内容。" if retrieved_docs else "未检索到相关内容。")

        # 7. 使用模型生成响应
        print("使用模型生成响应...")
        if context:
            prompt_with_context = PromptTemplate(
                input_variables=["display_context", "question"],
                template="请回答以下问题：\n{question}"
            )
            chain_with_context = prompt_with_context | llm | parser
            response = chain_with_context.invoke({
                "display_context": context,
                "question": question
            })
        else:
            chain = prompt_template | llm | parser
            response = chain.invoke({"question": question})

        print("模型响应：")
        print(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"运行时发生错误: {e}")

    finally:
        if weaviate_client:
            weaviate_client.close()
            print("Weaviate 客户端连接已关闭。")
            print("=" * 50)

if __name__ == "__main__":
    embedding_source = "xiaobu-embedding-v2"
    llm_source = "/models/Qwen2.5-7B-Instruct-AWQ"
    demo(embedding_source, llm_source)
    