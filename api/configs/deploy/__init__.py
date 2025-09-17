"""
部署配置模块

包含应用部署相关的配置设置
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class DeploymentConfig(BaseSettings):
    """
    应用部署配置
    """

    APPLICATION_NAME: str = Field(
        description="应用名称，用于标识和日志记录",
        default="MimirFW",
    )

    DEBUG: bool = Field(
        description="启用调试模式，提供额外的日志记录和开发功能",
        default=False,
    )

    # 请求日志配置
    ENABLE_REQUEST_LOGGING: bool = Field(
        description="启用请求和响应体日志记录",
        default=False,
    )

    EDITION: str = Field(
        description="应用部署版本（如 'SELF_HOSTED'、'CLOUD'）",
        default="SELF_HOSTED",
    )

    DEPLOY_ENV: str = Field(
        description="部署环境（如 'PRODUCTION'、'DEVELOPMENT'），默认为 PRODUCTION",
        default="PRODUCTION",
    )
