"""
阿里云 OSS 存储配置

支持阿里云对象存储服务
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class AliyunOSSStorageConfig(BaseSettings):
    """
    阿里云对象存储服务（OSS）配置
    """

    ALIYUN_OSS_BUCKET_NAME: Optional[str] = Field(
        description="用于存储和检索对象的阿里云 OSS 存储桶名称",
        default=None,
    )

    ALIYUN_OSS_ACCESS_KEY: Optional[str] = Field(
        description="用于阿里云 OSS 认证的访问密钥 ID",
        default=None,
    )

    ALIYUN_OSS_SECRET_KEY: Optional[str] = Field(
        description="用于阿里云 OSS 认证的密钥访问密钥",
        default=None,
    )

    ALIYUN_OSS_ENDPOINT: Optional[str] = Field(
        description="所选区域的阿里云 OSS 端点 URL",
        default=None,
    )

    ALIYUN_OSS_REGION: Optional[str] = Field(
        description="存储桶所在的阿里云 OSS 区域（例如：'oss-cn-hangzhou'）",
        default=None,
    )

    ALIYUN_OSS_AUTH_VERSION: Optional[str] = Field(
        description="与阿里云 OSS 一起使用的认证协议版本（例如：'v4'）",
        default=None,
    )

    ALIYUN_OSS_PATH: Optional[str] = Field(
        description="存储桶内存储对象的基础路径（例如：'my-app-data/'）",
        default=None,
    )
