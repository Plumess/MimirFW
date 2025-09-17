"""
中间件配置
"""

import os
from typing import Any, Literal, Optional
from urllib.parse import parse_qsl, quote_plus

from pydantic import Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, PositiveInt, computed_field
from pydantic_settings import BaseSettings

from .cache.redis_config import RedisConfig
from .vdb.weaviate_config import WeaviateConfig


class DatabaseConfig(BaseSettings):
    """
    数据库连接配置
    """

    DB_HOST: str = Field(
        description="数据库服务器的主机名或 IP 地址",
        default="localhost",
    )

    DB_PORT: PositiveInt = Field(
        description="数据库连接端口号",
        default=5432,
    )

    DB_USERNAME: str = Field(
        description="数据库认证用户名",
        default="mimirfw",
    )

    DB_PASSWORD: str = Field(
        description="数据库认证密码",
        default="password",
    )

    DB_DATABASE: str = Field(
        description="要连接的数据库名称",
        default="mimirfw",
    )

    DB_CHARSET: str = Field(
        description="数据库连接的字符集",
        default="utf8",
    )

    DB_EXTRAS: str = Field(
        description="额外的数据库连接参数。示例：'keepalives_idle=60&keepalives=1'",
        default="",
    )

    SQLALCHEMY_DATABASE_URI_SCHEME: str = Field(
        description="SQLAlchemy 连接的数据库 URI 方案",
        default="postgresql",
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """动态生成 SQLAlchemy 数据库 URI"""
        db_extras = (
            f"{self.DB_EXTRAS}&client_encoding={self.DB_CHARSET}" if self.DB_CHARSET else self.DB_EXTRAS
        ).strip("&")
        db_extras = f"?{db_extras}" if db_extras else ""
        return (
            f"{self.SQLALCHEMY_DATABASE_URI_SCHEME}://"
            f"{quote_plus(self.DB_USERNAME)}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
            f"{db_extras}"
        )

    SQLALCHEMY_POOL_SIZE: NonNegativeInt = Field(
        description="连接池中的最大数据库连接数",
        default=30,
    )

    SQLALCHEMY_MAX_OVERFLOW: NonNegativeInt = Field(
        description="可以创建的超出 pool_size 的最大连接数",
        default=10,
    )

    SQLALCHEMY_POOL_RECYCLE: NonNegativeInt = Field(
        description="连接自动回收的秒数",
        default=3600,
    )

    SQLALCHEMY_POOL_USE_LIFO: bool = Field(
        description="如果为 True，SQLAlchemy 将使用后进先出的方式从池中检索连接",
        default=False,
    )

    SQLALCHEMY_POOL_PRE_PING: bool = Field(
        description="如果为 True，启用连接池预 ping 功能以检查连接",
        default=False,
    )

    SQLALCHEMY_ECHO: bool | str = Field(
        description="如果为 True，SQLAlchemy 将记录所有 SQL 语句",
        default=False,
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict[str, Any]:
        """动态生成 SQLAlchemy 引擎选项"""
        # 解析 DB_EXTRAS 中的 'options'
        db_extras_dict = dict(parse_qsl(self.DB_EXTRAS))
        options = db_extras_dict.get("options", "")
        # 始终包含时区
        timezone_opt = "-c timezone=UTC"
        if options:
            # 合并用户选项和时区
            merged_options = f"{options} {timezone_opt}"
        else:
            merged_options = timezone_opt

        connect_args = {"options": merged_options}

        return {
            "pool_size": self.SQLALCHEMY_POOL_SIZE,
            "max_overflow": self.SQLALCHEMY_MAX_OVERFLOW,
            "pool_recycle": self.SQLALCHEMY_POOL_RECYCLE,
            "pool_pre_ping": self.SQLALCHEMY_POOL_PRE_PING,
            "connect_args": connect_args,
            "pool_use_lifo": self.SQLALCHEMY_POOL_USE_LIFO,
            "pool_reset_on_return": None,
        }


class CeleryConfig(DatabaseConfig):
    """
    Celery 任务队列配置
    """

    CELERY_BACKEND: str = Field(
        description="Celery 任务结果的后端。选项：'database', 'redis', 'rabbitmq'",
        default="redis",
    )

    CELERY_BROKER_URL: Optional[str] = Field(
        description="Celery 任务的消息代理 URL",
        default=None,
    )

    CELERY_USE_SENTINEL: Optional[bool] = Field(
        description="是否使用 Redis Sentinel 实现高可用性",
        default=False,
    )

    CELERY_SENTINEL_MASTER_NAME: Optional[str] = Field(
        description="Redis Sentinel 主节点名称",
        default=None,
    )

    CELERY_SENTINEL_PASSWORD: Optional[str] = Field(
        description="Redis Sentinel 主节点密码",
        default=None,
    )

    CELERY_SENTINEL_SOCKET_TIMEOUT: Optional[PositiveFloat] = Field(
        description="Redis Sentinel 套接字操作的超时时间（秒）",
        default=0.1,
    )

    @computed_field
    def CELERY_RESULT_BACKEND(self) -> str | None:
        """动态生成 Celery 结果后端 URL"""
        if self.CELERY_BACKEND in ("database", "rabbitmq"):
            return f"db+{self.SQLALCHEMY_DATABASE_URI}"
        elif self.CELERY_BACKEND == "redis":
            return self.CELERY_BROKER_URL
        else:
            return None

    @property
    def BROKER_USE_SSL(self) -> bool:
        """检查是否使用 SSL 连接"""
        return self.CELERY_BROKER_URL.startswith("rediss://") if self.CELERY_BROKER_URL else False


class VectorStoreConfig(BaseSettings):
    """
    向量存储配置
    """

    VECTOR_STORE: Optional[str] = Field(
        description="要使用的向量存储类型。如果未使用向量存储，则设置为 None",
        default="weaviate",
    )

    VECTOR_STORE_WHITELIST_ENABLE: Optional[bool] = Field(
        description="启用向量存储白名单",
        default=False,
    )

    VECTOR_INDEX_NAME_PREFIX: Optional[str] = Field(
        description="在向量数据库中创建集合名称时使用的前缀",
        default="Vector_index",
    )


class MiddlewareConfig(
    # 按字母顺序排列配置
    CeleryConfig,
    DatabaseConfig,
    RedisConfig,
    # 向量数据库配置
    VectorStoreConfig,
    WeaviateConfig,
    # TODO: 其他向量数据库配置（后续开发）
    # MilvusConfig,
    # QdrantConfig,
    # ChromaConfig,
):
    pass
