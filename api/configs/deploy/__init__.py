from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class DeploymentConfig(BaseSettings):
    """
    部署配置类
    """

    APPLICATION_NAME: str = Field(
        description="应用程序名称，用于识别和日志记录",
        default="MimirFW API",
    )

    DEBUG: bool = Field(
        description="是否启用调试模式，提供额外的日志和开发功能",
        default=False,
    )

    ENABLE_REQUEST_LOGGING: bool = Field(
        description="是否启用请求和响应体日志记录",
        default=False,
    )

    DEPLOY_ENV: str = Field(
        description="部署环境（例如：'PRODUCTION', 'DEVELOPMENT'），默认为 PRODUCTION",
        default="PRODUCTION",
    )

    API_PORT: PositiveInt = Field(
        description="MimirFW API 服务端口",
        default=8000,
    )
