"""
MimirFW API 应用入口

完全模仿 Dify 的 app.py 设计
"""

from app_factory import create_app
from configs import mimir_config

# 创建 Flask 应用实例
app = create_app()

if __name__ == "__main__":
    # 开发环境启动配置 - 完全从配置中读取，无硬编码
    app.run(
        host="0.0.0.0",
        port=mimir_config.API_PORT,  # 从配置中读取端口
        debug=mimir_config.DEBUG,  # 从配置中读取调试模式
    )
