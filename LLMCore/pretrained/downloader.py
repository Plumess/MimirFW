import os
from modelscope import snapshot_download
from config import *

class ModelDownloader:
    def check_exists(self, model_path):
        """检查模型或 embedding 是否存在"""
        return os.path.exists(model_path)

    def get_model_folder(self, model_id):
        """从 ModelScope ID 获取文件夹名称，使用 id 的后半部分（模型名）作为文件夹名"""
        return model_id.split('/')[-1]  # 返回 ID 的后半部分

    def download_with_modelscope(self, model_id, model_folder):
        """使用 ModelScope 的 Python API 下载模型到指定文件夹"""
        try:
            print(f"开始下载模型 {model_id} 到文件夹 {model_folder}")
            # 直接调用 snapshot_download 进行模型下载
            model_dir = snapshot_download(model_id, local_dir=model_folder)
            print(f"模型 {model_id} 下载完成，存储路径: {model_dir}")
            return {"error": False, "message": f"模型 {model_id} 已成功下载到 {model_dir}"}
        except Exception as e:
            print(f"模型 {model_id} 下载失败，错误: {str(e)}")
            return {"error": True, "message": f"模型 {model_id} 下载失败，错误: {str(e)}"}

    def download_model(self, model_id, embedding_id=None):
        """根据传递的 model_id 和 embedding_id 下载模型和 embedding"""
        
        # 自定义模型和 embedding
        model_folder = os.path.join(PROJECT_ROOT, MODELS_DIR, self.get_model_folder(model_id))
        embedding_folder = os.path.join(PROJECT_ROOT, EMBEDDINGS_DIR, self.get_model_folder(embedding_id))

        # 检查主模型是否存在
        model_exists = self.check_exists(model_folder)

        # 检查 embedding 是否存在
        embedding_exists = self.check_exists(embedding_folder)

        # 如果主模型不存在，则下载
        if not model_exists:
            print(f"主模型不存在，开始下载...")
            result = self.download_with_modelscope(model_id, model_folder)
            if result['error']:
                return result

        # 如果 embedding 不存在，则下载
        if embedding_id and not embedding_exists:
            print(f"embedding 模型不存在，开始下载到 {embedding_folder}...")
            embedding_result = self.download_with_modelscope(embedding_id, embedding_folder)
            if embedding_result['error']:
                return embedding_result

        return {"error": False, "message": "主模型和 embedding 模型都已成功下载或已存在"}

# 示例用法
if __name__ == "__main__":
    # 模拟前端传入的预设字典
    model_dict = {
        "Qwen2.5-3B-Instruct": "qwen/Qwen2.5-3B-Instruct",
        "Qwen2.5-3B-Instruct-AWQ": "qwen/Qwen2.5-3B-Instruct-AWQ",
        "Qwen2.5-7B-Instruct": "qwen/Qwen2.5-7B-Instruct",
        "Qwen2.5-7B-Instruct-AWQ": "qwen/Qwen2.5-7B-Instruct-AWQ",
        "Qwen2.5-14B-Instruct": "qwen/Qwen2.5-14B-Instruct",
        "Qwen2.5-14B-Instruct-AWQ": "qwen/Qwen2.5-14B-Instruct-AWQ",
        "Qwen2.5-32B-Instruct": "qwen/Qwen2.5-32B-Instruct",
        "Qwen2.5-32B-Instruct-AWQ": "qwen/Qwen2.5-32B-Instruct-AWQ",
        
        "Llama3.1-8B-Instruct": "LLM-Research/Meta-Llama-3.1-8B-Instruct",
    }

    embedding_dict = {
        # "xiaobu-embedding-v2": "Tolk8888/xiaobu-embedding-v2",
        "xiaobu-embedding-v2": "maple77/xiaobu-embedding-v2",
        "conan-embedding-v1": "KeplerAI/conan-embedding-v1-onnx",
        "zpoint_large_embedding_zh": "maple77/zpoint_large_embedding_zh"
    }

    # 假设前端传入了模型和 embedding 的 key
    model_key = "Qwen2.5-7B-Instruct-AWQ"
    embedding_key = "xiaobu-embedding-v2"

    # 获取对应的 ModelScope ID
    model_id = model_dict.get(model_key)
    embedding_id = embedding_dict.get(embedding_key)

    # 创建下载器实例
    downloader = ModelDownloader()

    # 下载模型和 embedding
    result = downloader.download_model(model_id, embedding_id)
    print(result)
