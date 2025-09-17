"""
数据库扩展

模仿 Dify 的 ext_database.py 设计
"""

import logging
from typing import TYPE_CHECKING, Any

import gevent  # type: ignore[import-untyped]
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.pool import Pool

if TYPE_CHECKING:
    from flask import Flask

logger = logging.getLogger(__name__)

# 全局数据库实例
db = SQLAlchemy()

# 全局标志以避免重复注册事件监听器
_GEVENT_COMPATIBILITY_SETUP: bool = False


def _safe_rollback(connection: Any) -> None:
    """
    安全地回滚数据库连接

    Args:
        connection: 数据库连接对象
    """
    try:
        connection.rollback()
    except Exception:
        logger.exception("Failed to rollback connection")


def _setup_gevent_compatibility() -> None:
    """设置 gevent 兼容性"""
    global _GEVENT_COMPATIBILITY_SETUP

    # 避免重复注册
    if _GEVENT_COMPATIBILITY_SETUP:
        return

    @event.listens_for(Pool, "reset")
    def _safe_reset(dbapi_connection: Any, connection_record: Any, reset_state: Any) -> None:
        """安全重置连接池"""
        if reset_state.terminate_only:
            return

        # 安全回滚连接
        try:
            hub = gevent.get_hub()
            if hasattr(hub, "loop") and getattr(hub.loop, "in_callback", False):
                gevent.spawn_later(0, lambda: _safe_rollback(dbapi_connection))
            else:
                _safe_rollback(dbapi_connection)
        except (AttributeError, ImportError):
            _safe_rollback(dbapi_connection)

    _GEVENT_COMPATIBILITY_SETUP = True


def init_app(app: "Flask") -> None:
    """
    初始化数据库扩展

    Args:
        app: Flask 应用实例
    """

    # 直接初始化数据库
    db.init_app(app)

    # 设置 gevent 兼容性
    _setup_gevent_compatibility()

    logger.info("Database extension initialized")
