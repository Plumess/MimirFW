"""
MimirFW 应用工厂
"""

import logging
import time
from typing import TYPE_CHECKING, Any

from flask import Flask

from configs import mimir_config

if TYPE_CHECKING:
    from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def create_flask_app_with_configs() -> Flask:
    """
    创建一个原始的 Flask 应用
    从 .env 文件加载配置
    """
    app = Flask(__name__)
    # 关键：将所有配置设置到 Flask 的 app.config 中
    app.config.from_mapping(mimir_config.model_dump())
    
    return app


def create_app() -> Flask:
    """创建应用"""
    start_time = time.perf_counter()
    app = create_flask_app_with_configs()
    initialize_extensions(app)
    register_blueprints(app)
    end_time = time.perf_counter()
    if mimir_config.DEBUG:
        logger.info("Finished create_app (%s ms)", round((end_time - start_time) * 1000, 2))
    return app


def initialize_extensions(app: Flask) -> None:
    """初始化扩展"""
    from extensions import (
        # 待开发的扩展
        ext_celery,
        ext_database,
        ext_logging,
        ext_redis,
    )
    
    # 按顺序加载扩展
    extensions = [
        ext_logging,      # 先初始化日志（待开发）
        ext_database,     # 数据库
        ext_redis,        # Redis
        ext_celery,       # Celery（待开发）
    ]
    
    for ext in extensions:
        short_name = ext.__name__.split(".")[-1]
        is_enabled = ext.is_enabled() if hasattr(ext, "is_enabled") else True
        if not is_enabled:
            if mimir_config.DEBUG:
                logger.info("Skipped %s (disabled)", short_name)
            continue

        start_time = time.perf_counter()
        ext.init_app(app)
        end_time = time.perf_counter()
        if mimir_config.DEBUG:
            logger.info("Loaded %s (%s ms)", short_name, round((end_time - start_time) * 1000, 2))


def register_blueprints(app: Flask) -> None:
    """注册蓝图 - 配置驱动"""
    
    # 基础健康检查端点 - 配置驱动
    @app.route("/health")
    def health_check() -> dict[str, Any]:
        return {
            "status": "healthy", 
            "service": mimir_config.APPLICATION_NAME.lower(),
            "version": mimir_config.VERSION,
            "environment": mimir_config.DEPLOY_ENV
        }
    
    # 根端点 - 配置驱动
    @app.route("/")
    def root() -> dict[str, Any]:
        return {
            "service": f"{mimir_config.APPLICATION_NAME} API",
            "version": mimir_config.VERSION,
            "description": mimir_config.DESCRIPTION,
            "status": "running",
            "environment": mimir_config.DEPLOY_ENV,
            "debug": mimir_config.DEBUG
        }
    
    # 注册错误处理器 - 配置驱动
    @app.errorhandler(404)
    def not_found(error: "HTTPException") -> tuple[dict[str, Any], int]:
        return {
            "error": "Not Found", 
            "message": "The requested resource was not found",
            "service": mimir_config.APPLICATION_NAME,
            "version": mimir_config.VERSION
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error: "HTTPException") -> tuple[dict[str, Any], int]:
        return {
            "error": "Internal Server Error", 
            "message": "An internal error occurred",
            "service": mimir_config.APPLICATION_NAME,
            "version": mimir_config.VERSION
        }, 500


def create_migrations_app() -> Flask:
    """创建迁移应用"""
    app = create_flask_app_with_configs()
    from extensions import ext_database
    
    # 只初始化必需的扩展
    ext_database.init_app(app)
    
    return app
