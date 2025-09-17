"""
Celery 扩展

TODO: 后续开发 - 异步任务队列配置和管理
模仿 Dify 的 ext_celery.py 设计
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask


def init_app(app: "Flask") -> None:
    """
    初始化 Celery 扩展 - 待开发
    
    Args:
        app: Flask 应用实例
    """
    # TODO: 实现 Celery 扩展初始化
    pass


def is_enabled() -> bool:
    """检查 Celery 扩展是否启用 - 目前禁用"""
    return False
