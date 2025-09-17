"""
MimirFW 主配置

完全模仿 Dify 的配置架构设计，采用模块化配置管理：
- 打包信息 (PackagingInfo)
- 部署配置 (DeploymentConfig)
- 功能特性配置 (FeatureConfig)
- 中间件配置 (MiddlewareConfig)
- 可观测性配置 (ObservabilityConfig)
- 额外服务配置 (ExtraServiceConfig)
"""

from pydantic_settings import SettingsConfigDict

from .deploy import DeploymentConfig
from .extra import ExtraServiceConfig
from .feature import FeatureConfig
from .middleware import MiddlewareConfig
from .observability import ObservabilityConfig
from .packaging import PackagingInfo


class MimirConfig(
    # 打包信息
    PackagingInfo,
    # 部署配置
    DeploymentConfig,
    # 功能特性配置
    FeatureConfig,
    # 中间件配置
    MiddlewareConfig,
    # 可观测性配置
    ObservabilityConfig,
    # 额外服务配置
    ExtraServiceConfig,
):
    """
    MimirFW 主配置类

    通过多重继承组合所有配置模块，完全模仿 Dify 的 DifyConfig 设计
    """

    model_config = SettingsConfigDict(
        # 从 .env 格式配置文件读取
        env_file=".env",
        env_file_encoding="utf-8",
        # 忽略额外属性
        extra="ignore",
    )

    # 在添加任何配置之前，
    # 请考虑将其安排在现有或新增的适当配置组中，
    # 以便更好地提高可读性和可维护性。
    # 感谢您的专注和考虑。


# 创建全局配置实例 - 模仿 Dify 的 dify_config
mimir_config = MimirConfig()
