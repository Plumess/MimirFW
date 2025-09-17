"""
OpenDAL 存储配置

OpenDAL 是一个统一的数据访问层，支持多种存储后端
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class OpenDALStorageConfig(BaseSettings):
    """
    OpenDAL 存储配置
    """

    OPENDAL_SCHEME: str = Field(
        default="fs",
        description="OpenDAL 存储方案。支持 'fs'（文件系统）、's3'、'oss'、'azblob' 等",
    )
