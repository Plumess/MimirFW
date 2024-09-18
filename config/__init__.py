import os

# 获取项目根目录路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 设置 Weaviate Docker通信地址
WEAVIATE_URL = 'weaviate'
WEAVIATE_PORT = '8080'

# 设置设备环境变量
from LLMCore.utils.device_checker import check_device
DEVICE_INFO = check_device()