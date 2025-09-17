"""
Redis 缓存配置

包含 Redis 连接、认证、SSL、哨兵、集群等配置
"""

from typing import Optional

from pydantic import Field, NonNegativeInt, PositiveFloat, PositiveInt
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    """
    Redis 连接配置设置
    """

    REDIS_HOST: str = Field(
        description="Redis 服务器的主机名或 IP 地址",
        default="localhost",
    )

    REDIS_PORT: PositiveInt = Field(
        description="Redis 服务器监听的端口号",
        default=6379,
    )

    REDIS_USERNAME: Optional[str] = Field(
        description="Redis 认证用户名（如果需要）",
        default=None,
    )

    REDIS_PASSWORD: Optional[str] = Field(
        description="Redis 认证密码（如果需要）",
        default=None,
    )

    REDIS_DB: NonNegativeInt = Field(
        description="使用的 Redis 数据库编号（0-15）",
        default=0,
    )

    REDIS_USE_SSL: bool = Field(
        description="为 Redis 连接启用 SSL/TLS",
        default=False,
    )

    REDIS_SSL_CERT_REQS: str = Field(
        description="SSL 证书要求（CERT_NONE、CERT_OPTIONAL、CERT_REQUIRED）",
        default="CERT_NONE",
    )

    REDIS_SSL_CA_CERTS: Optional[str] = Field(
        description="SSL 验证的 CA 证书文件路径",
        default=None,
    )

    REDIS_SSL_CERTFILE: Optional[str] = Field(
        description="SSL 认证的客户端证书文件路径",
        default=None,
    )

    REDIS_SSL_KEYFILE: Optional[str] = Field(
        description="SSL 认证的客户端私钥文件路径",
        default=None,
    )

    REDIS_USE_SENTINEL: Optional[bool] = Field(
        description="启用 Redis Sentinel 模式以实现高可用性",
        default=False,
    )

    REDIS_SENTINELS: Optional[str] = Field(
        description="Redis Sentinel 节点列表，逗号分隔（host:port）",
        default=None,
    )

    REDIS_SENTINEL_SERVICE_NAME: Optional[str] = Field(
        description="要监控的 Redis Sentinel 服务名称",
        default=None,
    )

    REDIS_SENTINEL_USERNAME: Optional[str] = Field(
        description="Redis Sentinel 认证用户名（如果需要）",
        default=None,
    )

    REDIS_SENTINEL_PASSWORD: Optional[str] = Field(
        description="Redis Sentinel 认证密码（如果需要）",
        default=None,
    )

    REDIS_SENTINEL_SOCKET_TIMEOUT: Optional[PositiveFloat] = Field(
        description="Redis Sentinel 连接的套接字超时时间（秒）",
        default=0.1,
    )

    REDIS_USE_CLUSTERS: bool = Field(
        description="启用 Redis 集群模式以实现高可用性",
        default=False,
    )

    REDIS_CLUSTERS: Optional[str] = Field(
        description="Redis 集群节点列表，逗号分隔（host:port）",
        default=None,
    )

    REDIS_CLUSTERS_PASSWORD: Optional[str] = Field(
        description="Redis 集群认证密码（如果需要）",
        default=None,
    )

    REDIS_SERIALIZATION_PROTOCOL: int = Field(
        description="Redis 序列化协议（RESP）版本",
        default=3,
    )

    REDIS_ENABLE_CLIENT_SIDE_CACHE: bool = Field(
        description="在 Redis 中启用客户端缓存",
        default=False,
    )
