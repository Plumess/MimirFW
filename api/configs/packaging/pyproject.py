"""
PyProject 配置

从 pyproject.toml 文件中读取项目配置信息
"""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class PyProjectConfig(BaseModel):
    """
    PyProject 项目配置
    """

    version: str = Field(description="MimirFW 版本号", default="")

    description: str = Field(description="MimirFW API 介绍", default="")


class PyProjectTomlConfig(BaseSettings):
    """
    api/pyproject.toml 中的配置
    """

    project: PyProjectConfig = Field(
        description="pyproject.toml 中 project 部分的配置",
        default=PyProjectConfig(),
    )
