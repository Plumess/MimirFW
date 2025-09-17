"""
Redis 扩展

完全模仿 Dify 的 ext_redis.py 设计
"""

import functools
import logging
import ssl
from collections.abc import Callable
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Optional, Union

import redis
from redis import RedisError
from redis.cluster import ClusterNode, RedisCluster
from redis.connection import Connection, SSLConnection
from redis.sentinel import Sentinel

from configs import mimir_config

if TYPE_CHECKING:
    from flask import Flask
    from redis.lock import Lock

logger = logging.getLogger(__name__)


class RedisClientWrapper:
    """
    Redis 客户端包装器
    
    解决全局 `redis_client` 变量无法在 Sentinel 返回新 Redis 实例时更新的问题。
    
    该类允许延迟初始化 Redis 客户端，使客户端能够在必要时重新初始化新实例。
    这在 Redis 实例可能动态变化的场景中特别有用，比如 Sentinel 管理的 Redis 设置中的故障转移。
    """

    _client: Union[redis.Redis, RedisCluster, None]

    def __init__(self) -> None:
        self._client = None

    def initialize(self, client: Union[redis.Redis, RedisCluster]) -> None:
        if self._client is None:
            self._client = client

    if TYPE_CHECKING:
        # IDE 支持和静态分析的类型提示
        # 这些在运行时不执行，但提供类型信息
        def get(self, name: str | bytes) -> Any: ...

        def set(
            self,
            name: str | bytes,
            value: Any,
            ex: int | None = None,
            px: int | None = None,
            nx: bool = False,
            xx: bool = False,
            keepttl: bool = False,
            get: bool = False,
            exat: int | None = None,
            pxat: int | None = None,
        ) -> Any: ...

        def setex(self, name: str | bytes, time: int | timedelta, value: Any) -> Any: ...
        def setnx(self, name: str | bytes, value: Any) -> Any: ...
        def delete(self, *names: str | bytes) -> Any: ...
        def incr(self, name: str | bytes, amount: int = 1) -> Any: ...
        def expire(
            self,
            name: str | bytes,
            time: int | timedelta,
            nx: bool = False,
            xx: bool = False,
            gt: bool = False,
            lt: bool = False,
        ) -> Any: ...
        def lock(
            self,
            name: str,
            timeout: float | None = None,
            sleep: float = 0.1,
            blocking: bool = True,
            blocking_timeout: float | None = None,
            thread_local: bool = True,
        ) -> "Lock": ...
        def zadd(
            self,
            name: str | bytes,
            mapping: dict[str | bytes | int | float, float | int | str | bytes],
            nx: bool = False,
            xx: bool = False,
            ch: bool = False,
            incr: bool = False,
            gt: bool = False,
            lt: bool = False,
        ) -> Any: ...
        def zremrangebyscore(self, name: str | bytes, min: float | str, max: float | str) -> Any: ...
        def zcard(self, name: str | bytes) -> Any: ...
        def getdel(self, name: str | bytes) -> Any: ...

    def __getattr__(self, item: str) -> Any:
        if self._client is None:
            raise RuntimeError("Redis client is not initialized. Call init_app first.")
        return getattr(self._client, item)


redis_client: RedisClientWrapper = RedisClientWrapper()


def _get_ssl_configuration() -> tuple[type[Union[Connection, SSLConnection]], dict[str, Any]]:
    """获取 Redis 连接的 SSL 配置"""
    if not mimir_config.REDIS_USE_SSL:
        return Connection, {}

    cert_reqs_map = {
        "CERT_NONE": ssl.CERT_NONE,
        "CERT_OPTIONAL": ssl.CERT_OPTIONAL,
        "CERT_REQUIRED": ssl.CERT_REQUIRED,
    }
    ssl_cert_reqs = cert_reqs_map.get(mimir_config.REDIS_SSL_CERT_REQS, ssl.CERT_NONE)

    ssl_kwargs = {
        "ssl_cert_reqs": ssl_cert_reqs,
        "ssl_ca_certs": mimir_config.REDIS_SSL_CA_CERTS,
        "ssl_certfile": mimir_config.REDIS_SSL_CERTFILE,
        "ssl_keyfile": mimir_config.REDIS_SSL_KEYFILE,
    }

    return SSLConnection, ssl_kwargs


def _get_base_redis_params() -> dict[str, Any]:
    """获取基础 Redis 连接参数"""
    return {
        "username": mimir_config.REDIS_USERNAME,
        "password": mimir_config.REDIS_PASSWORD or None,
        "db": mimir_config.REDIS_DB,
        "encoding": "utf-8",
        "encoding_errors": "strict",
        "decode_responses": False,
        "protocol": mimir_config.REDIS_SERIALIZATION_PROTOCOL,
    }


def _create_sentinel_client(redis_params: dict[str, Any]) -> Union[redis.Redis, RedisCluster]:
    """使用 Sentinel 配置创建 Redis 客户端"""
    if not mimir_config.REDIS_SENTINELS:
        raise ValueError("REDIS_SENTINELS must be set when REDIS_USE_SENTINEL is True")

    if not mimir_config.REDIS_SENTINEL_SERVICE_NAME:
        raise ValueError("REDIS_SENTINEL_SERVICE_NAME must be set when REDIS_USE_SENTINEL is True")

    sentinel_hosts = [
        (node.split(":")[0], int(node.split(":")[1])) 
        for node in mimir_config.REDIS_SENTINELS.split(",")
    ]

    sentinel = Sentinel(
        sentinel_hosts,
        sentinel_kwargs={
            "socket_timeout": mimir_config.REDIS_SENTINEL_SOCKET_TIMEOUT,
            "username": mimir_config.REDIS_SENTINEL_USERNAME,
            "password": mimir_config.REDIS_SENTINEL_PASSWORD,
        },
    )

    master: redis.Redis = sentinel.master_for(mimir_config.REDIS_SENTINEL_SERVICE_NAME, **redis_params)
    return master


def _create_cluster_client() -> Union[redis.Redis, RedisCluster]:
    """创建 Redis 集群客户端"""
    if not mimir_config.REDIS_CLUSTERS:
        raise ValueError("REDIS_CLUSTERS must be set when REDIS_USE_CLUSTERS is True")

    nodes = [
        ClusterNode(host=node.split(":")[0], port=int(node.split(":")[1]))
        for node in mimir_config.REDIS_CLUSTERS.split(",")
    ]

    cluster: RedisCluster = RedisCluster(
        startup_nodes=nodes,
        password=mimir_config.REDIS_CLUSTERS_PASSWORD,
        protocol=mimir_config.REDIS_SERIALIZATION_PROTOCOL,
    )
    return cluster


def _create_standalone_client(redis_params: dict[str, Any]) -> Union[redis.Redis, RedisCluster]:
    """创建独立 Redis 客户端"""
    connection_class, ssl_kwargs = _get_ssl_configuration()

    redis_params.update(
        {
            "host": mimir_config.REDIS_HOST,
            "port": mimir_config.REDIS_PORT,
            "connection_class": connection_class,
        }
    )

    if ssl_kwargs:
        redis_params.update(ssl_kwargs)

    pool = redis.ConnectionPool(**redis_params)
    client: redis.Redis = redis.Redis(connection_pool=pool)
    return client


def init_app(app: "Flask") -> None:
    """初始化 Redis 客户端并附加到应用"""
    global redis_client

    # 确定 Redis 模式并创建适当的客户端
    if mimir_config.REDIS_USE_SENTINEL:
        redis_params = _get_base_redis_params()
        client = _create_sentinel_client(redis_params)
    elif mimir_config.REDIS_USE_CLUSTERS:
        client = _create_cluster_client()
    else:
        redis_params = _get_base_redis_params()
        client = _create_standalone_client(redis_params)

    # 初始化包装器并附加到应用
    redis_client.initialize(client)
    app.extensions["redis"] = redis_client


def redis_fallback(default_return: Optional[Any] = None) -> Callable:
    """
    装饰器，用于处理 Redis 操作异常并在 Redis 不可用时返回默认值
    
    Args:
        default_return: Redis 操作失败时返回的值。默认为 None。
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except RedisError as e:
                logger.warning("Redis operation failed in %s: %s", func.__name__, str(e), exc_info=True)
                return default_return

        return wrapper

    return decorator
