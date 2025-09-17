"""
日志扩展

TODO: 后续开发 - 日志配置和管理
模仿 Dify 的 ext_logging.py 设计
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask


def init_app(app: "Flask") -> None:
    """
    初始化日志扩展 - 待开发

    Args:
        app: Flask 应用实例
    """
    # TODO: 实现日志扩展初始化
    pass


def is_enabled() -> bool:
    """检查日志扩展是否启用 - 目前禁用"""
    return False
