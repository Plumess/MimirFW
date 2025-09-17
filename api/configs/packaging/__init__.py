"""
打包信息配置

包含项目打包和构建相关的配置信息
"""

from pydantic import Field

from .pyproject import PyProjectConfig, PyProjectTomlConfig


class PackagingInfo(PyProjectTomlConfig):
    """
    打包构建信息
    """

    COMMIT_SHA: str = Field(
        description="用于构建应用的 Git 提交的 SHA-1 校验和",
        default="",
    )
