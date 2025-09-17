"""
Amazon S3 存储配置

支持 S3 兼容的对象存储服务
"""

from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class S3StorageConfig(BaseSettings):
    """
    S3 兼容对象存储配置
    """

    S3_ENDPOINT: Optional[str] = Field(
        description="S3 兼容存储端点的 URL（例如：'https://s3.amazonaws.com'）",
        default=None,
    )

    S3_REGION: Optional[str] = Field(
        description="S3 存储桶所在的区域（例如：'us-east-1'）",
        default=None,
    )

    S3_BUCKET_NAME: Optional[str] = Field(
        description="用于存储和检索对象的 S3 存储桶名称",
        default=None,
    )

    S3_ACCESS_KEY: Optional[str] = Field(
        description="用于 S3 服务认证的访问密钥 ID",
        default=None,
    )

    S3_SECRET_KEY: Optional[str] = Field(
        description="用于 S3 服务认证的密钥访问密钥",
        default=None,
    )

    S3_ADDRESS_STYLE: Literal["auto", "virtual", "path"] = Field(
        description="S3 寻址样式：'auto'、'path' 或 'virtual'",
        default="auto",
    )

    S3_USE_AWS_MANAGED_IAM: bool = Field(
        description="使用 AWS 托管 IAM 角色进行认证，而不是访问/密钥",
        default=False,
    )
