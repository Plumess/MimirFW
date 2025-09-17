"""
MimirFW 主配置类

采用多重继承组合不同配置模块
"""

import logging
from pathlib import Path

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource

from libs.file_utils import search_file_upwards

from .deploy import DeploymentConfig
from .feature import FeatureConfig
from .middleware import MiddlewareConfig
from .packaging import PackagingInfo

# 预留配置模块 - 暂时不实现具体内容
# from .extra import ExtraServiceConfig
# from .observability import ObservabilityConfig
# from .remote_settings_sources import RemoteSettingsSourceConfig

logger = logging.getLogger(__name__)


class MimirConfig(
    # 打包信息
    PackagingInfo,
    # 部署配置
    DeploymentConfig,
    # 功能配置
    FeatureConfig,
    # 中间件配置
    MiddlewareConfig,
    # 预留配置模块 - 暂时不实现具体内容
    # ExtraServiceConfig,
    # ObservabilityConfig,
    # RemoteSettingsSourceConfig,
):
    """
    MimirFW 主配置类

    通过多重继承组合所有配置模块，提供统一的配置管理接口
    """

    model_config = SettingsConfigDict(
        # 从 .env 文件读取配置
        env_file=".env",
        env_file_encoding="utf-8",
        # 忽略额外属性
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        自定义配置源优先级

        配置源优先级（从高到低）：
        1. init_settings - 初始化参数
        2. env_settings - 环境变量
        3. dotenv_settings - .env 文件
        4. file_secret_settings - 密钥文件
        5. TomlConfigSettingsSource - pyproject.toml
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(
                settings_cls=settings_cls,
                toml_file=search_file_upwards(
                    base_dir_path=Path(__file__).parent,
                    target_file_name="pyproject.toml",
                    max_search_parent_depth=2,
                ),
            ),
        )
