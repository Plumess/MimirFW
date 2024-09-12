import os
from modelscope import snapshot_download

class ModelDownloader:
    def __init__(self, model_dict=None):
        # 默认支持的模型字典
        self.model_dict = model_dict or {
            "Qwen": {
                "2-instruct-AWQ": {
                    "1.5B": "qwen/Qwen2-1.5B-Instruct-AWQ",
                    "7B": "qwen/Qwen2-7B-Instruct-AWQ",
                    "72B": "qwen/Qwen2-72B-Instruct-AWQ",
                },
                "2-instruct": {
                    "1.5B": "qwen/qwen2-1.5b-instruct",
                    "7B": "qwen/qwen2-7b-instruct",
                    "72B": "qwen/qwen2-72b-instruct",
                },
            },
            "Llama": {
                "3.1": {
                    "8B": "LLM-Research/Meta-Llama-3.1-8B-Instruct",
                    "70B": "LLM-Research/Meta-Llama-3.1-70B-Instruct"
                }
            }
        }

    def get_modelscope_id(self, key):
        """根据传入的模型 key 获取 modelscope 的模型 id"""
        model_name, version, size = key.get('name'), key.get('version'), key.get('size')
        custom_model_id = key.get('custom_model_id')
        
        # 如果是自定义模型并传入了 model id
        if custom_model_id:
            return custom_model_id
        
        # 如果是默认支持的模型
        if model_name in self.model_dict:
            if version in self.model_dict[model_name]:
                if size in self.model_dict[model_name][version]:
                    return self.model_dict[model_name][version][size]
        return None

    def check_model_exists(self, key, save_dir):
        """检查模型文件夹是否已经存在"""
        model_dir = f"{key['name']}-{key['version']}-{key['size']}"
        model_path = os.path.join(save_dir, model_dir)
        return os.path.exists(model_path), model_dir

    def download_with_modelscope(self, model_id, model_folder):
        """使用 ModelScope 的 Python API 下载模型到指定文件夹"""
        try:
            # 直接调用 snapshot_download 进行模型下载
            model_dir = snapshot_download(model_id, local_dir=model_folder)
            return {"error": False, "message": f"模型 {model_id} 已成功下载到 {model_dir}"}
        except Exception as e:
            return {"error": True, "message": f"模型 {model_id} 下载失败，错误: {str(e)}"}

    def download_model(self, key):
        """根据 key 检查模型存在性并下载，支持自定义模型下载"""
        model_name = key['name']
        
        # 确定存放目录的基础路径
        if model_name.lower() == "qwen":
            save_dir = "./qwen"
        elif model_name.lower() == "llama":
            save_dir = "./llama"
        else:
            save_dir = "./customs"

        # 创建存放目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 根据 key 构建模型文件夹
        model_exists, model_dir = self.check_model_exists(key, save_dir)
        model_folder = os.path.join(save_dir, model_dir)

        # 如果模型已经存在，直接返回成功
        if model_exists:
            return {"error": False, "message": f"模型文件夹 {model_dir} 已确认存在"}

        # 使用 ModelScope Python API 下载模型到该文件夹
        model_id = self.get_modelscope_id(key)
        if model_id:
            return self.download_with_modelscope(model_id, model_folder)
        else:
            return {"error": True, "message": "No matching model ID found for the given key."}

# 示例用法
if __name__ == "__main__":
    # 模拟从前端传入的 key（选择预设模型）
    key = {
        "name": "Qwen",
        "version": "2-instruct-AWQ",
        "size": "1.5B"
    }

    downloader = ModelDownloader()

    # 下载预设模型到 qwen 目录
    result = downloader.download_model(key)
    print(result)
