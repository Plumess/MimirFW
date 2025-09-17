"""
功能特性配置
"""

from typing import Optional

from pydantic import Field, PositiveInt, computed_field
from pydantic_settings import BaseSettings


class SecurityConfig(BaseSettings):
    """
    安全相关配置
    """

    SECRET_KEY: str = Field(
        description="用于安全会话 cookie 签名的密钥。"
        "请确保为您的部署更改此密钥为强密钥。"
        "使用 `openssl rand -base64 42` 生成强密钥或通过 `SECRET_KEY` 环境变量设置。",
        default="",
    )

    JWT_SECRET_KEY: str = Field(
        description="JWT 密钥，用于生成和验证 JWT 令牌",
        default="",
    )

    JWT_ACCESS_TOKEN_EXPIRES: PositiveInt = Field(
        description="JWT 访问令牌过期时间（秒）",
        default=3600,
    )


class GameConfig(BaseSettings):
    """
    游戏相关配置
    """

    GAME_MAX_PLAYERS_PER_SESSION: PositiveInt = Field(
        description="每个游戏会话的最大玩家数",
        default=8,
    )

    GAME_SESSION_TIMEOUT_MINUTES: PositiveInt = Field(
        description="游戏会话超时时间（分钟）",
        default=60,
    )

    GAME_AUTO_SAVE_INTERVAL_SECONDS: PositiveInt = Field(
        description="游戏自动保存间隔（秒）",
        default=300,
    )


class LoggingConfig(BaseSettings):
    """
    日志配置
    """

    LOG_LEVEL: str = Field(
        description="日志级别，默认为 INFO。生产环境建议设置为 ERROR。",
        default="INFO",
    )

    LOG_FILE: Optional[str] = Field(
        description="日志文件路径",
        default=None,
    )

    LOG_FORMAT: str = Field(
        description="日志消息的格式字符串",
        default="%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s",
    )

    LOG_DATEFORMAT: Optional[str] = Field(
        description="日志时间戳的日期格式字符串",
        default=None,
    )

    LOG_TZ: str = Field(
        description="日志时间戳的时区",
        default="UTC",
    )


class HttpConfig(BaseSettings):
    """
    HTTP 相关配置
    """

    inner_CONSOLE_CORS_ALLOW_ORIGINS: str = Field(
        description="控制台 CORS 允许的来源，逗号分隔",
        default="",
    )

    @computed_field
    def CONSOLE_CORS_ALLOW_ORIGINS(self) -> list[str]:
        """将 CORS 源字符串转换为列表"""
        return [origin.strip() for origin in self.inner_CONSOLE_CORS_ALLOW_ORIGINS.split(",") if origin.strip()]

    inner_WEB_API_CORS_ALLOW_ORIGINS: str = Field(
        description="Web API CORS 允许的来源，逗号分隔",
        default="*",
    )

    @computed_field
    def WEB_API_CORS_ALLOW_ORIGINS(self) -> list[str]:
        """将 CORS 源字符串转换为列表"""
        return [origin.strip() for origin in self.inner_WEB_API_CORS_ALLOW_ORIGINS.split(",") if origin.strip()]


class FeatureConfig(
    # 按字母顺序排列配置
    GameConfig,
    HttpConfig,
    LoggingConfig,
    SecurityConfig,
):
    pass
