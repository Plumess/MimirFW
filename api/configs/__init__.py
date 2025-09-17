"""
MimirFW 配置模块

完全模仿 Dify 的配置导入方式
"""

from .app_config import MimirConfig, mimir_config

__all__ = [
    "MimirConfig",
    "mimir_config",
]
