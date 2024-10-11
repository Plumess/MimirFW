import os
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from LLMCore.managers.model_loader import ModelLoaderInterface
from config import *

# 如果您使用的是 API，需要设置 API 密钥
# export API_KEY='***'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

def demo(model_type, inference_framework_type, llm_source, embedding_source):
    # 1.基本测试信息输出
    print("=" * 50)
    print(f"Running demo with:")
    print(f"  Model Type: {model_type}")
    print(f"  Inference Framework: {inference_framework_type}")
    print(f"  LLM Source: {llm_source}")
    print(f"  Embedding Source: {embedding_source}")
    print("=" * 50)
    print()

    # 使用封装好的 DEVICE_INFO
    print("=" * 50)
    print(f"设备信息：{DEVICE_INFO}")
    print("=" * 50)
    print()

    try:
        # 2.根据参数创建模型加载实例
        print(f"加载模型中...")
        if model_type == 'api':
            if inference_framework_type == 'openai':
                API_KEY = OPENAI_API_KEY
            elif inference_framework_type == 'qwen':
                API_KEY = DASHSCOPE_API_KEY

            # 创建模型加载器接口实例 API Version
            model_loader_interface = ModelLoaderInterface(
                model_type=model_type,                             # 'api'
                inference_framework_type=inference_framework_type  # 'openai', 'qwen'
            )
            # 设置 LLM 和 Embedding 模型标识符
            model_loader_interface.set_llm_model_source(llm_source)
            model_loader_interface.set_embedding_model_source(embedding_source)

            # 加载模型和 embeddings
            # 对于 API 版本，在加载模型时传递 api_key
            model_loader_interface.load_llm(api_key=API_KEY)
            llm = model_loader_interface.get_llm()
            model_loader_interface.load_embeddings(api_key=API_KEY)
            embeddings = model_loader_interface.get_embeddings()


        elif model_type == 'local':
            # 创建模型加载器接口实例 Local Version
            model_loader_interface = ModelLoaderInterface(
                model_type=model_type,                              # 'local'
                inference_framework_type=inference_framework_type,  # 'vllm'
            )
            # 设置 LLM 和 Embedding 模型路径
            model_loader_interface.set_llm_model_source(llm_source)
            model_loader_interface.set_embedding_model_source(embedding_source)

            model_loader_interface.load_llm(
                max_tokens=512,
                temperature=0.7,
            )
            llm = model_loader_interface.get_llm()
            model_loader_interface.load_embeddings()
            embeddings = model_loader_interface.get_embeddings()

        print("模型加载完毕。")
        print("=" * 50)
        print()

        # 3. 连接 Weaviate 向量数据库
        # 初始化 weaviate_client 为 None
        weaviate_client = None
        # https://weaviate.io/developers/weaviate/connections
        print(f"尝试连接 Weaviate 数据库，URL: http://{WEAVIATE_URL}:{WEAVIATE_PORT}...")
        weaviate_client = weaviate.connect_to_local(
            host=WEAVIATE_URL,
            port=WEAVIATE_PORT,
            grpc_port=50051,
        )
        print("成功连接到 Weaviate 数据库。")
        print("=" * 50)
        print()

        # 4. 定义模板化输出和输出解析器
        print("定义模板化输出和输出解析器...")
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="请根据以下问题提供详细的回答：{question}"
        )
        # 创建输出解析器
        parser = StrOutputParser()
        print("模板化输出和输出解析器定义完毕。")
        print("=" * 50)
        print()

        # 示例输入
        question = "请介绍一下LangChain的主要功能。"
        text_path = os.path.join(PROJECT_ROOT, 'LLMCore/test/test_data.txt')

        # 5. 检索向量数据库中的内容
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
            # 使用管道操作符组合组件
            chain_with_context = prompt_with_context | llm | parser
            # 调用模型时，传递完整的 context
            response = chain_with_context.invoke({"display_context": display_context, "question": question, "context": context})
        else:
            # 无上下文时直接生成响应
            chain = prompt_template | llm | parser
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


# main 函数
def main():
    # 定义多种test测试例子，使用字典存储
    test_cases = {
        'test1': {
            'model_type': 'api',
            'inference_framework_type': 'openai',
            'llm_source': 'gpt-4o',
            'embedding_source': 'text-embedding-ada-002'
        },
        'test2': {
            'model_type': 'api',
            'inference_framework_type': 'qwen',
            'llm_source': 'qwen-plus',
            'embedding_source': 'text-embedding-v3'
        },
        'test3': {
            'model_type': 'local',
            'inference_framework_type': 'vllm',
            'llm_source': 'Qwen2.5-7B-Instruct-AWQ',
            'embedding_source': 'xiaobu-embedding-v2'
        },
    }

    # 选择要执行的test
    selected_test = 'test3'  # 修改这里可以选择不同的test

    # 获取选定的test的参数并调用demo函数
    test_params = test_cases[selected_test]
    demo(**test_params)

# 运行main函数
if __name__ == "__main__":
    main()

# python LLMCore/demo.py > ./LLMCore/logs/demo0914.log
