"""
功能配置模块

包含所有应用功能相关的配置设置
"""

from typing import Literal, Optional

from pydantic import (
    AliasChoices,
    Field,
    HttpUrl,
    NegativeInt,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    computed_field,
)
from pydantic_settings import BaseSettings

# from .hosted_service import HostedServiceConfig


class SecurityConfig(BaseSettings):
    """
    安全相关配置
    """

    SECRET_KEY: str = Field(
        description="用于安全会话 cookie 签名的密钥。"
        "请确保为您的部署更改此密钥为强密钥。"
        "使用 `openssl rand -base64 42` 生成强密钥或通过 `SECRET_KEY` 环境变量设置。",
        default="",
    )

    RESET_PASSWORD_TOKEN_EXPIRY_MINUTES: PositiveInt = Field(
        description="密码重置令牌保持有效的持续时间（分钟）",
        default=5,
    )
    CHANGE_EMAIL_TOKEN_EXPIRY_MINUTES: PositiveInt = Field(
        description="更改邮箱令牌保持有效的持续时间（分钟）",
        default=5,
    )

    OWNER_TRANSFER_TOKEN_EXPIRY_MINUTES: PositiveInt = Field(
        description="所有者转移令牌保持有效的持续时间（分钟）",
        default=5,
    )

    LOGIN_DISABLED: bool = Field(
        description="是否禁用登录检查",
        default=False,
    )

    ADMIN_API_KEY_ENABLE: bool = Field(
        description="是否启用管理员 API 密钥进行认证",
        default=False,
    )

    ADMIN_API_KEY: Optional[str] = Field(
        description="管理员 API 密钥用于认证",
        default=None,
    )


class AppExecutionConfig(BaseSettings):
    """
    应用执行配置参数
    """

    APP_MAX_EXECUTION_TIME: PositiveInt = Field(
        description="应用允许的最大执行时间（秒）",
        default=1200,
    )
    APP_MAX_ACTIVE_REQUESTS: NonNegativeInt = Field(
        description="每个应用的最大并发活跃请求数（0 表示无限制）",
        default=0,
    )
    APP_DAILY_RATE_LIMIT: NonNegativeInt = Field(
        description="每个应用每天的最大请求数",
        default=5000,
    )


class CodeExecutionSandboxConfig(BaseSettings):
    """
    代码执行沙箱环境配置
    """

    CODE_EXECUTION_ENDPOINT: HttpUrl = Field(
        description="代码执行服务的 URL 端点",
        default=HttpUrl("http://sandbox:8194"),
    )

    CODE_EXECUTION_API_KEY: str = Field(
        description="访问代码执行服务的 API 密钥",
        default="mimir-sandbox",
    )

    CODE_EXECUTION_CONNECT_TIMEOUT: Optional[float] = Field(
        description="代码执行请求的连接超时时间（秒）",
        default=10.0,
    )

    CODE_EXECUTION_READ_TIMEOUT: Optional[float] = Field(
        description="代码执行请求的读取超时时间（秒）",
        default=60.0,
    )

    CODE_EXECUTION_WRITE_TIMEOUT: Optional[float] = Field(
        description="代码执行请求的写入超时时间（秒）",
        default=10.0,
    )

    CODE_MAX_NUMBER: PositiveInt = Field(
        description="代码执行中允许的最大数值",
        default=9223372036854775807,
    )

    CODE_MIN_NUMBER: NegativeInt = Field(
        description="代码执行中允许的最小数值",
        default=-9223372036854775807,
    )

    CODE_MAX_DEPTH: PositiveInt = Field(
        description="代码执行中嵌套结构的最大深度",
        default=5,
    )

    CODE_MAX_PRECISION: PositiveInt = Field(
        description="代码执行中浮点数的小数位数最大值",
        default=20,
    )

    CODE_MAX_STRING_LENGTH: PositiveInt = Field(
        description="代码执行中字符串的最大长度",
        default=80000,
    )

    CODE_MAX_STRING_ARRAY_LENGTH: PositiveInt = Field(
        description="代码执行中字符串数组的最大长度",
        default=30,
    )

    CODE_MAX_OBJECT_ARRAY_LENGTH: PositiveInt = Field(
        description="代码执行中对象数组的最大长度",
        default=30,
    )

    CODE_MAX_NUMBER_ARRAY_LENGTH: PositiveInt = Field(
        description="代码执行中数值数组的最大长度",
        default=1000,
    )


class PluginConfig(BaseSettings):
    """
    插件配置
    """

    PLUGIN_DAEMON_URL: HttpUrl = Field(
        description="插件 API URL",
        default=HttpUrl("http://localhost:5002"),
    )

    PLUGIN_DAEMON_KEY: str = Field(
        description="插件 API 密钥",
        default="plugin-api-key",
    )

    INNER_API_KEY_FOR_PLUGIN: str = Field(description="插件内部 API 密钥", default="inner-api-key")

    PLUGIN_REMOTE_INSTALL_HOST: str = Field(
        description="插件远程安装主机",
        default="localhost",
    )

    PLUGIN_REMOTE_INSTALL_PORT: PositiveInt = Field(
        description="插件远程安装端口",
        default=5003,
    )

    PLUGIN_MAX_PACKAGE_SIZE: PositiveInt = Field(
        description="插件包的最大允许大小（字节）",
        default=15728640,
    )

    PLUGIN_MAX_BUNDLE_SIZE: PositiveInt = Field(
        description="插件捆绑包的最大允许大小（字节）",
        default=15728640 * 12,
    )


class MarketplaceConfig(BaseSettings):
    """
    插件市场配置
    """

    MARKETPLACE_ENABLED: bool = Field(
        description="启用或禁用插件市场功能",
        default=True,
    )

    MARKETPLACE_API_URL: HttpUrl = Field(
        description="插件市场 API URL",
        default=HttpUrl("https://marketplace.mimirfw.chat"),
    )


class EndpointConfig(BaseSettings):
    """
    各种应用端点和 URL 的配置
    """

    CONSOLE_API_URL: str = Field(
        description="控制台 API 的基础 URL，用于登录认证回调或 Notion 集成回调",
        default="",
    )

    CONSOLE_WEB_URL: str = Field(
        description="控制台 Web 界面的基础 URL，用于前端引用和 CORS 配置",
        default="",
    )

    SERVICE_API_URL: str = Field(
        description="服务 API 的基础 URL，向用户显示用于 API 访问",
        default="",
    )

    APP_WEB_URL: str = Field(
        description="Web 应用的基础 URL，用于前端引用",
        default="",
    )

    ENDPOINT_URL_TEMPLATE: str = Field(description="端点插件的模板 URL", default="http://localhost:5002/e/{hook_id}")


class FileAccessConfig(BaseSettings):
    """
    文件访问和处理配置
    """

    FILES_URL: str = Field(
        description="文件预览或下载的基础 URL，用于前端显示和多模态输入。URL 已签名并有过期时间。",
        validation_alias=AliasChoices("FILES_URL", "CONSOLE_API_URL"),
        # alias_priority=1,
        default="",
    )

    INTERNAL_FILES_URL: str = Field(
        description="Docker 网络内文件访问的内部基础 URL，"
        "用于插件守护进程和内部服务通信。"
        "如果未指定，则回退到 FILES_URL。",
        default="",
    )

    FILES_ACCESS_TIMEOUT: int = Field(
        description="文件访问 URL 的过期时间（秒）",
        default=300,
    )


class FileUploadConfig(BaseSettings):
    """
    文件上传限制配置
    """

    UPLOAD_FILE_SIZE_LIMIT: NonNegativeInt = Field(
        description="上传文件的最大允许大小（MB）",
        default=15,
    )

    UPLOAD_FILE_BATCH_LIMIT: NonNegativeInt = Field(
        description="单次上传批次中允许的最大文件数",
        default=5,
    )

    UPLOAD_IMAGE_FILE_SIZE_LIMIT: NonNegativeInt = Field(
        description="上传图片文件的最大允许大小（MB）",
        default=10,
    )

    UPLOAD_VIDEO_FILE_SIZE_LIMIT: NonNegativeInt = Field(
        description="上传视频文件的大小限制（MB）",
        default=100,
    )

    UPLOAD_AUDIO_FILE_SIZE_LIMIT: NonNegativeInt = Field(
        description="上传音频文件的大小限制（MB）",
        default=50,
    )

    BATCH_UPLOAD_LIMIT: NonNegativeInt = Field(
        description="批量上传操作中允许的最大文件数",
        default=20,
    )

    WORKFLOW_FILE_UPLOAD_LIMIT: PositiveInt = Field(
        description="工作流上传操作中允许的最大文件数",
        default=10,
    )


class HttpConfig(BaseSettings):
    """
    应用的 HTTP 相关配置
    """

    API_COMPRESSION_ENABLED: bool = Field(
        description="启用或禁用 HTTP 响应的 gzip 压缩",
        default=False,
    )

    inner_CONSOLE_CORS_ALLOW_ORIGINS: str = Field(
        description="控制台 CORS 允许的来源列表，逗号分隔",
        validation_alias=AliasChoices("CONSOLE_CORS_ALLOW_ORIGINS", "CONSOLE_WEB_URL"),
        default="",
    )

    @computed_field
    def CONSOLE_CORS_ALLOW_ORIGINS(self) -> list[str]:
        return self.inner_CONSOLE_CORS_ALLOW_ORIGINS.split(",")

    inner_WEB_API_CORS_ALLOW_ORIGINS: str = Field(
        description="",
        validation_alias=AliasChoices("WEB_API_CORS_ALLOW_ORIGINS"),
        default="*",
    )

    @computed_field
    def WEB_API_CORS_ALLOW_ORIGINS(self) -> list[str]:
        return self.inner_WEB_API_CORS_ALLOW_ORIGINS.split(",")

    HTTP_REQUEST_MAX_CONNECT_TIMEOUT: int = Field(ge=1, description="HTTP 请求的最大连接超时时间（秒）", default=10)

    HTTP_REQUEST_MAX_READ_TIMEOUT: int = Field(ge=1, description="HTTP 请求的最大读取超时时间（秒）", default=60)

    HTTP_REQUEST_MAX_WRITE_TIMEOUT: int = Field(ge=1, description="HTTP 请求的最大写入超时时间（秒）", default=20)

    HTTP_REQUEST_NODE_MAX_BINARY_SIZE: PositiveInt = Field(
        description="HTTP 请求中二进制数据的最大允许大小（字节）",
        default=10 * 1024 * 1024,
    )

    HTTP_REQUEST_NODE_MAX_TEXT_SIZE: PositiveInt = Field(
        description="HTTP 请求中文本数据的最大允许大小（字节）",
        default=1 * 1024 * 1024,
    )

    HTTP_REQUEST_NODE_SSL_VERIFY: bool = Field(
        description="启用或禁用 HTTP 请求的 SSL 验证",
        default=True,
    )

    SSRF_DEFAULT_MAX_RETRIES: PositiveInt = Field(
        description="网络请求的最大重试次数（SSRF）",
        default=3,
    )

    SSRF_PROXY_ALL_URL: Optional[str] = Field(
        description="用于防止服务器端请求伪造（SSRF）的 HTTP 或 HTTPS 请求代理 URL",
        default=None,
    )

    SSRF_PROXY_HTTP_URL: Optional[str] = Field(
        description="用于防止服务器端请求伪造（SSRF）的 HTTP 请求代理 URL",
        default=None,
    )

    SSRF_PROXY_HTTPS_URL: Optional[str] = Field(
        description="用于防止服务器端请求伪造（SSRF）的 HTTPS 请求代理 URL",
        default=None,
    )

    SSRF_DEFAULT_TIME_OUT: PositiveFloat = Field(
        description="网络请求使用的默认超时时间（SSRF）",
        default=5,
    )

    SSRF_DEFAULT_CONNECT_TIME_OUT: PositiveFloat = Field(
        description="网络请求使用的默认连接超时时间（SSRF）",
        default=5,
    )

    SSRF_DEFAULT_READ_TIME_OUT: PositiveFloat = Field(
        description="网络请求使用的默认读取超时时间（SSRF）",
        default=5,
    )

    SSRF_DEFAULT_WRITE_TIME_OUT: PositiveFloat = Field(
        description="网络请求使用的默认写入超时时间（SSRF）",
        default=5,
    )

    RESPECT_XFORWARD_HEADERS_ENABLED: bool = Field(
        description="当应用位于单个受信任的反向代理后面时，"
        "启用对 X-Forwarded-For、X-Forwarded-Proto 和 X-Forwarded-Port 头的处理。",
        default=False,
    )


class InnerAPIConfig(BaseSettings):
    """
    内部 API 功能配置
    """

    INNER_API: bool = Field(
        description="启用或禁用内部 API",
        default=False,
    )

    INNER_API_KEY: Optional[str] = Field(
        description="访问内部 API 的 API 密钥",
        default=None,
    )


class LoggingConfig(BaseSettings):
    """
    应用日志配置
    """

    LOG_LEVEL: str = Field(
        description="日志级别，默认为 INFO。生产环境建议设置为 ERROR。",
        default="INFO",
    )

    LOG_FILE: Optional[str] = Field(
        description="日志输出的文件路径。",
        default=None,
    )

    LOG_FILE_MAX_SIZE: PositiveInt = Field(
        description="文件轮转保留的最大文件大小，单位为 MB",
        default=20,
    )

    LOG_FILE_BACKUP_COUNT: PositiveInt = Field(
        description="文件轮转保留的最大文件备份数量",
        default=5,
    )

    LOG_FORMAT: str = Field(
        description="日志消息的格式字符串",
        default="%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s",
    )

    LOG_DATEFORMAT: Optional[str] = Field(
        description="日志时间戳的日期格式字符串",
        default=None,
    )

    LOG_TZ: Optional[str] = Field(
        description="日志时间戳的时区（例如：'America/New_York'）",
        default="UTC",
    )


class ModelLoadBalanceConfig(BaseSettings):
    """
    模型负载均衡和令牌计数配置
    """

    MODEL_LB_ENABLED: bool = Field(
        description="启用或禁用模型的负载均衡",
        default=False,
    )

    PLUGIN_BASED_TOKEN_COUNTING_ENABLED: bool = Field(
        description="启用或禁用基于插件的令牌计数。如果禁用，令牌计数将返回 0。",
        default=False,
    )


class BillingConfig(BaseSettings):
    """
    平台计费功能配置
    """

    BILLING_ENABLED: bool = Field(
        description="启用或禁用计费功能",
        default=False,
    )


class UpdateConfig(BaseSettings):
    """
    应用更新检查配置
    """

    CHECK_UPDATE_URL: str = Field(
        description="检查应用更新的 URL",
        default="https://updates.mimirfw.chat",
    )


class WorkflowConfig(BaseSettings):
    """
    工作流执行配置
    """

    WORKFLOW_MAX_EXECUTION_STEPS: PositiveInt = Field(
        description="单个工作流执行中允许的最大步数",
        default=500,
    )

    WORKFLOW_MAX_EXECUTION_TIME: PositiveInt = Field(
        description="单个工作流的最大执行时间（秒）",
        default=1200,
    )

    WORKFLOW_CALL_MAX_DEPTH: PositiveInt = Field(
        description="嵌套工作流调用的最大允许深度",
        default=5,
    )

    WORKFLOW_PARALLEL_DEPTH_LIMIT: PositiveInt = Field(
        description="嵌套并行执行的最大允许深度",
        default=3,
    )

    MAX_VARIABLE_SIZE: PositiveInt = Field(
        description="工作流中单个变量的最大大小（字节）。默认为 200 KB。",
        default=200 * 1024,
    )


class WorkflowNodeExecutionConfig(BaseSettings):
    """
    工作流节点执行配置
    """

    MAX_SUBMIT_COUNT: PositiveInt = Field(
        description="并行节点执行的线程池中提交的最大线程数",
        default=100,
    )

    WORKFLOW_NODE_EXECUTION_STORAGE: str = Field(
        default="rdbms",
        description="WorkflowNodeExecution 的存储后端。选项：'rdbms'、'hybrid'",
    )


class RepositoryConfig(BaseSettings):
    """
    仓储实现配置
    """

    CORE_WORKFLOW_EXECUTION_REPOSITORY: str = Field(
        description="WorkflowExecution 的仓储实现。选项："
        "'core.repositories.sqlalchemy_workflow_execution_repository.SQLAlchemyWorkflowExecutionRepository'（默认），"
        "'core.repositories.celery_workflow_execution_repository.CeleryWorkflowExecutionRepository'",
        default="core.repositories.sqlalchemy_workflow_execution_repository.SQLAlchemyWorkflowExecutionRepository",
    )

    CORE_WORKFLOW_NODE_EXECUTION_REPOSITORY: str = Field(
        description="WorkflowNodeExecution 的仓储实现。选项："
        "'core.repositories.sqlalchemy_workflow_node_execution_repository."
        "SQLAlchemyWorkflowNodeExecutionRepository'（默认），"
        "'core.repositories.celery_workflow_node_execution_repository."
        "CeleryWorkflowNodeExecutionRepository'",
        default="core.repositories.sqlalchemy_workflow_node_execution_repository.SQLAlchemyWorkflowNodeExecutionRepository",
    )

    API_WORKFLOW_NODE_EXECUTION_REPOSITORY: str = Field(
        description="WorkflowNodeExecutionModel 操作的服务层仓储实现。指定为模块路径",
        default="repositories.sqlalchemy_api_workflow_node_execution_repository.MimirAPISQLAlchemyWorkflowNodeExecutionRepository",
    )

    API_WORKFLOW_RUN_REPOSITORY: str = Field(
        description="WorkflowRun 操作的服务层仓储实现。指定为模块路径",
        default="repositories.sqlalchemy_api_workflow_run_repository.MimirAPISQLAlchemyWorkflowRunRepository",
    )


class AuthConfig(BaseSettings):
    """
    认证和 OAuth 配置
    """

    OAUTH_REDIRECT_PATH: str = Field(
        description="OAuth 认证回调的重定向路径",
        default="/console/api/oauth/authorize",
    )

    GITHUB_CLIENT_ID: Optional[str] = Field(
        description="GitHub OAuth 客户端 ID",
        default=None,
    )

    GITHUB_CLIENT_SECRET: Optional[str] = Field(
        description="GitHub OAuth 客户端密钥",
        default=None,
    )

    GOOGLE_CLIENT_ID: Optional[str] = Field(
        description="Google OAuth 客户端 ID",
        default=None,
    )

    GOOGLE_CLIENT_SECRET: Optional[str] = Field(
        description="Google OAuth 客户端密钥",
        default=None,
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(
        description="访问令牌的过期时间（分钟）",
        default=60,
    )

    REFRESH_TOKEN_EXPIRE_DAYS: PositiveFloat = Field(
        description="刷新令牌的过期时间（天）",
        default=30,
    )

    LOGIN_LOCKOUT_DURATION: PositiveInt = Field(
        description="用户超过速率限制后重试登录前必须等待的时间（秒）。",
        default=86400,
    )

    FORGOT_PASSWORD_LOCKOUT_DURATION: PositiveInt = Field(
        description="用户超过速率限制后重试密码重置前必须等待的时间（秒）。",
        default=86400,
    )

    CHANGE_EMAIL_LOCKOUT_DURATION: PositiveInt = Field(
        description="用户超过速率限制后重试更改邮箱前必须等待的时间（秒）。",
        default=86400,
    )

    OWNER_TRANSFER_LOCKOUT_DURATION: PositiveInt = Field(
        description="用户超过速率限制后重试所有者转移前必须等待的时间（秒）。",
        default=86400,
    )


class ModerationConfig(BaseSettings):
    """
    内容审核配置
    """

    MODERATION_BUFFER_SIZE: PositiveInt = Field(
        description="内容审核处理的缓冲区大小",
        default=300,
    )


class ToolConfig(BaseSettings):
    """
    工具管理配置
    """

    TOOL_ICON_CACHE_MAX_AGE: PositiveInt = Field(
        description="工具图标缓存的最大年龄（秒）",
        default=3600,
    )


class MailConfig(BaseSettings):
    """
    邮件服务配置
    """

    MAIL_TYPE: Optional[str] = Field(
        description="邮件服务提供商类型（'smtp' 或 'resend' 或 'sendGrid'），默认为 None。",
        default=None,
    )

    MAIL_DEFAULT_SEND_FROM: Optional[str] = Field(
        description="用作发送者的默认邮件地址",
        default=None,
    )

    RESEND_API_KEY: Optional[str] = Field(
        description="Resend 邮件服务的 API 密钥",
        default=None,
    )

    RESEND_API_URL: Optional[str] = Field(
        description="Resend 邮件服务的 API URL",
        default=None,
    )

    SMTP_SERVER: Optional[str] = Field(
        description="SMTP 服务器主机名",
        default=None,
    )

    SMTP_PORT: Optional[int] = Field(
        description="SMTP 服务器端口号",
        default=465,
    )

    SMTP_USERNAME: Optional[str] = Field(
        description="SMTP 认证用户名",
        default=None,
    )

    SMTP_PASSWORD: Optional[str] = Field(
        description="SMTP 认证密码",
        default=None,
    )

    SMTP_USE_TLS: bool = Field(
        description="为 SMTP 连接启用 TLS 加密",
        default=False,
    )

    SMTP_OPPORTUNISTIC_TLS: bool = Field(
        description="为 SMTP 连接启用机会性 TLS",
        default=False,
    )

    EMAIL_SEND_IP_LIMIT_PER_MINUTE: PositiveInt = Field(
        description="同一 IP 地址每分钟允许发送的最大邮件数",
        default=50,
    )

    SENDGRID_API_KEY: Optional[str] = Field(
        description="SendGrid 服务的 API 密钥",
        default=None,
    )


class RagEtlConfig(BaseSettings):
    """
    RAG ETL 流程配置
    """

    # TODO: 此配置不仅用于 rag etl，还用于文件上传，我们应该将其移动到文件上传配置
    ETL_TYPE: str = Field(
        description="RAG ETL 类型（'mimir' 或 'Unstructured'），默认为 'mimir'",
        default="mimir",
    )

    KEYWORD_DATA_SOURCE_TYPE: str = Field(
        description="关键词提取的数据源类型（'database' 或其他支持的类型），默认为 'database'",
        default="database",
    )

    UNSTRUCTURED_API_URL: Optional[str] = Field(
        description="Unstructured.io 服务的 API URL",
        default=None,
    )

    UNSTRUCTURED_API_KEY: Optional[str] = Field(
        description="Unstructured.io 服务的 API 密钥",
        default="",
    )

    SCARF_NO_ANALYTICS: Optional[str] = Field(
        description="这是关于是否在 Unstructured 库中禁用 Scarf 分析。",
        default="false",
    )


class DataSetConfig(BaseSettings):
    """
    数据集管理配置
    """

    PLAN_SANDBOX_CLEAN_DAY_SETTING: PositiveInt = Field(
        description="数据集清理操作的间隔天数 - 计划：沙箱",
        default=30,
    )

    PLAN_PRO_CLEAN_DAY_SETTING: PositiveInt = Field(
        description="数据集清理操作的间隔天数 - 计划：专业版和团队版",
        default=7,
    )

    DATASET_OPERATOR_ENABLED: bool = Field(
        description="启用或禁用数据集操作器功能",
        default=False,
    )

    TIDB_SERVERLESS_NUMBER: PositiveInt = Field(
        description="TiDB 无服务器集群数量",
        default=500,
    )

    CREATE_TIDB_SERVICE_JOB_ENABLED: bool = Field(
        description="启用或禁用创建 TiDB 服务作业",
        default=False,
    )

    PLAN_SANDBOX_CLEAN_MESSAGE_DAY_SETTING: PositiveInt = Field(
        description="消息清理操作的间隔天数 - 计划：沙箱",
        default=30,
    )


class WorkspaceConfig(BaseSettings):
    """
    工作空间管理配置
    """

    INVITE_EXPIRY_HOURS: PositiveInt = Field(
        description="工作空间邀请链接的过期时间（小时）",
        default=72,
    )


class IndexingConfig(BaseSettings):
    """
    索引操作配置
    """

    INDEXING_MAX_SEGMENTATION_TOKENS_LENGTH: PositiveInt = Field(
        description="索引期间文本分段的最大令牌长度",
        default=4000,
    )

    CHILD_CHUNKS_PREVIEW_NUMBER: PositiveInt = Field(
        description="要预览的子块的最大数量",
        default=50,
    )


class MultiModalTransferConfig(BaseSettings):
    MULTIMODAL_SEND_FORMAT: Literal["base64", "url"] = Field(
        description="多模态上下文中发送文件的格式（'base64' 或 'url'），默认为 base64",
        default="base64",
    )


class CeleryBeatConfig(BaseSettings):
    CELERY_BEAT_SCHEDULER_TIME: int = Field(
        description="Celery Beat 调度器执行的间隔天数，默认为 1 天",
        default=1,
    )


class CeleryScheduleTasksConfig(BaseSettings):
    ENABLE_CLEAN_EMBEDDING_CACHE_TASK: bool = Field(
        description="启用清理嵌入缓存任务",
        default=False,
    )
    ENABLE_CLEAN_UNUSED_DATASETS_TASK: bool = Field(
        description="启用清理未使用数据集任务",
        default=False,
    )
    ENABLE_CREATE_TIDB_SERVERLESS_TASK: bool = Field(
        description="启用创建 TiDB 服务作业任务",
        default=False,
    )
    ENABLE_UPDATE_TIDB_SERVERLESS_STATUS_TASK: bool = Field(
        description="启用更新 TiDB 服务作业状态任务",
        default=False,
    )
    ENABLE_CLEAN_MESSAGES: bool = Field(
        description="启用清理消息任务",
        default=False,
    )
    ENABLE_MAIL_CLEAN_DOCUMENT_NOTIFY_TASK: bool = Field(
        description="启用邮件清理文档通知任务",
        default=False,
    )
    ENABLE_DATASETS_QUEUE_MONITOR: bool = Field(
        description="启用队列监控任务",
        default=False,
    )
    ENABLE_CHECK_UPGRADABLE_PLUGIN_TASK: bool = Field(
        description="启用检查可升级插件任务",
        default=True,
    )


class PositionConfig(BaseSettings):
    POSITION_PROVIDER_PINS: str = Field(
        description="固定的模型提供商列表，逗号分隔",
        default="",
    )

    POSITION_PROVIDER_INCLUDES: str = Field(
        description="包含的模型提供商列表，逗号分隔",
        default="",
    )

    POSITION_PROVIDER_EXCLUDES: str = Field(
        description="排除的模型提供商列表，逗号分隔",
        default="",
    )

    POSITION_TOOL_PINS: str = Field(
        description="固定的工具列表，逗号分隔",
        default="",
    )

    POSITION_TOOL_INCLUDES: str = Field(
        description="包含的工具列表，逗号分隔",
        default="",
    )

    POSITION_TOOL_EXCLUDES: str = Field(
        description="排除的工具列表，逗号分隔",
        default="",
    )

    @property
    def POSITION_PROVIDER_PINS_LIST(self) -> list[str]:
        return [item.strip() for item in self.POSITION_PROVIDER_PINS.split(",") if item.strip() != ""]

    @property
    def POSITION_PROVIDER_INCLUDES_SET(self) -> set[str]:
        return {item.strip() for item in self.POSITION_PROVIDER_INCLUDES.split(",") if item.strip() != ""}

    @property
    def POSITION_PROVIDER_EXCLUDES_SET(self) -> set[str]:
        return {item.strip() for item in self.POSITION_PROVIDER_EXCLUDES.split(",") if item.strip() != ""}

    @property
    def POSITION_TOOL_PINS_LIST(self) -> list[str]:
        return [item.strip() for item in self.POSITION_TOOL_PINS.split(",") if item.strip() != ""]

    @property
    def POSITION_TOOL_INCLUDES_SET(self) -> set[str]:
        return {item.strip() for item in self.POSITION_TOOL_INCLUDES.split(",") if item.strip() != ""}

    @property
    def POSITION_TOOL_EXCLUDES_SET(self) -> set[str]:
        return {item.strip() for item in self.POSITION_TOOL_EXCLUDES.split(",") if item.strip() != ""}


class LoginConfig(BaseSettings):
    ENABLE_EMAIL_CODE_LOGIN: bool = Field(
        description="是否启用邮箱验证码登录",
        default=False,
    )
    ENABLE_EMAIL_PASSWORD_LOGIN: bool = Field(
        description="是否启用邮箱密码登录",
        default=True,
    )
    ENABLE_SOCIAL_OAUTH_LOGIN: bool = Field(
        description="是否启用 GitHub/Google OAuth 登录",
        default=False,
    )
    EMAIL_CODE_LOGIN_TOKEN_EXPIRY_MINUTES: PositiveInt = Field(
        description="邮箱验证码登录令牌的过期时间（分钟）",
        default=5,
    )
    ALLOW_REGISTER: bool = Field(
        description="是否启用注册",
        default=False,
    )
    ALLOW_CREATE_WORKSPACE: bool = Field(
        description="是否启用创建工作空间",
        default=False,
    )


class AccountConfig(BaseSettings):
    ACCOUNT_DELETION_TOKEN_EXPIRY_MINUTES: PositiveInt = Field(
        description="账户删除令牌保持有效的持续时间（分钟）",
        default=5,
    )

    EDUCATION_ENABLED: bool = Field(
        description="是否启用教育身份",
        default=False,
    )


class WorkflowLogConfig(BaseSettings):
    WORKFLOW_LOG_CLEANUP_ENABLED: bool = Field(default=True, description="启用工作流运行日志清理")
    WORKFLOW_LOG_RETENTION_DAYS: int = Field(default=30, description="工作流运行日志的保留天数")
    WORKFLOW_LOG_CLEANUP_BATCH_SIZE: int = Field(default=100, description="工作流运行日志清理操作的批次大小")


class SwaggerUIConfig(BaseSettings):
    SWAGGER_UI_ENABLED: bool = Field(
        description="是否在 API 模块中启用 Swagger UI",
        default=True,
    )

    SWAGGER_UI_PATH: str = Field(
        description="API 模块中 Swagger UI 页面路径",
        default="/swagger-ui.html",
    )


class FeatureConfig(
    AppExecutionConfig,
    AuthConfig,
    BillingConfig,
    CodeExecutionSandboxConfig,
    PluginConfig,
    MarketplaceConfig,
    DataSetConfig,
    EndpointConfig,
    FileAccessConfig,
    FileUploadConfig,
    HttpConfig,
    InnerAPIConfig,
    IndexingConfig,
    LoggingConfig,
    MailConfig,
    ModelLoadBalanceConfig,
    ModerationConfig,
    MultiModalTransferConfig,
    PositionConfig,
    RagEtlConfig,
    RepositoryConfig,
    SecurityConfig,
    ToolConfig,
    UpdateConfig,
    WorkflowConfig,
    WorkflowNodeExecutionConfig,
    WorkspaceConfig,
    LoginConfig,
    AccountConfig,
    SwaggerUIConfig,
    CeleryBeatConfig,
    CeleryScheduleTasksConfig,
    WorkflowLogConfig,
):
    """
    功能配置类

    通过多重继承组合所有功能相关的配置模块
    """

    pass
