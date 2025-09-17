from pydantic import Field
from pydantic_settings import BaseSettings


class PackagingInfo(BaseSettings):
    """
    打包信息配置类
    """

    APPLICATION_NAME: str = Field(
        description="应用程序名称",
        default="MimirFW",
    )
    DESCRIPTION: str = Field(
        description="应用程序描述",
        default="基于大语言模型的对话类游戏搭建框架",
    )
    VERSION: str = Field(
        description="应用程序版本",
        default="0.1.0",
    )
