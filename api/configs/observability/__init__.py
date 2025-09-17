"""
可观测性配置（后续开发）
"""

from pydantic_settings import BaseSettings


class ObservabilityConfig(BaseSettings):
    """
    可观测性配置设置
    """

    # TODO: 添加监控配置（后续开发）
    # SENTRY_DSN: Optional[str] = Field(description="Sentry DSN for error monitoring", default=None)
    # ENABLE_TRACING: bool = Field(description="Enable distributed tracing", default=False)
    # METRICS_ENABLED: bool = Field(description="Enable metrics collection", default=False)
    pass
