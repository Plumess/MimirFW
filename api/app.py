"""
MimirFW API 应用入口

基于配置系统启动应用
"""

from app_factory import create_app
from configs import mimir_config

# 创建 Flask 应用实例
app = create_app()

if __name__ == "__main__":
    # 开发环境启动配置 - 使用现有配置
    app.run(
        host="0.0.0.0",
        port=8000,  # 使用默认端口，因为配置中没有 API_PORT
        debug=mimir_config.DEBUG,  # 从配置中读取调试模式
    )
