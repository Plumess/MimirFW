"""
MimirFW 配置系统

采用分层模块化配置管理
"""

from .app_config import MimirConfig

mimir_config = MimirConfig()

__all__ = ["MimirConfig", "mimir_config"]
