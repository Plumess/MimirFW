"""
额外服务配置（后续开发）
"""

from pydantic_settings import BaseSettings


class ExtraServiceConfig(BaseSettings):
    """
    额外服务配置设置
    """

    # TODO: 添加邮件服务配置（后续开发）
    # MAIL_TYPE: Optional[str] = Field(description="Email service type", default=None)
    # SMTP_SERVER: Optional[str] = Field(description="SMTP server", default=None)
    # SMTP_PORT: int = Field(description="SMTP port", default=587)

    pass
