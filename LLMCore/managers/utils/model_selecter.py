from config import PROJECT_ROOT
import os

def list_models(model_dir):
    """遍历指定目录，返回模型名称和路径"""
    models = []
    for model_name in os.listdir(model_dir):
        model_path = os.path.join(model_dir, model_name)
        if os.path.isdir(model_path):
            models.append({
                "name": model_name,
                "path": model_path
            })
    return models

def get_all_models():
    """获取大模型和embedding模型的信息"""
    model_dir = os.path.join(PROJECT_ROOT, 'LLMCore/pretrained/models')
    embedding_dir = os.path.join(PROJECT_ROOT, 'LLMCore/pretrained/embedding')

    large_models = list_models(model_dir)
    embedding_models = list_models(embedding_dir)

    return {
        "large_models": large_models,
        "embedding_models": embedding_models
    }

# 使用示例
if __name__ == "__main__":
    all_models = get_all_models()
    print("大模型列表:", all_models["large_models"])
    print("Embedding模型列表:", all_models["embedding_models"])
