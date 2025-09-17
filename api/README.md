# MimirFW 后端 API

> [!NOTE]
>
> 本文档描述了 MimirFW 后端 API 的**架构设计**。
> 借鉴 Dify 架构的最佳实践，采用功能域分离、工厂模式和事件驱动的设计理念，针对对话类游戏场景进行优化。

## 🏗️ 架构概述

MimirFW 后端 API 基于 Flask 3.x 构建，采用现代化的微服务架构设计。核心设计理念是通过精细化功能域分离、工厂模式应用和事件驱动架构，构建专门针对对话类游戏的高可用、高扩展、易维护的平台架构。

**核心设计理念**：
- **精细功能域分离**: 按业务功能域组织代码，每个域职责边界清晰
- **工厂模式驱动**: 模型提供商、游戏流程、玩家、工具等都通过工厂管理
- **事件驱动架构**: 基于事件流的游戏流程引擎，支持实时状态同步
- **可扩展设计**: 支持插件扩展、多模型提供商、多向量数据库
- **企业级特性（后续支持）**: 预留监控追踪、审核机制、安全控制等企业级功能（后续开发）

## 🚀 快速开始

### 1. 启动中间件服务

```bash
cd ../docker
cp middleware.env.example middleware.env
docker compose -f docker-compose.middleware.yaml --profile weaviate -p mimirfw up -d
cd ../api
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 生成 SECRET_KEY
sed -i "/^SECRET_KEY=/c\SECRET_KEY=$(openssl rand -base64 42)" .env
```

### 3. 安装依赖并启动

```bash
# 安装 uv 包管理器
pip install uv

# 安装依赖
uv sync --dev

# 数据库迁移
uv run flask db upgrade

# 启动 API 服务
uv run flask run --host 0.0.0.0 --port=8000 --debug
```

### 4. 启动异步任务处理

```bash
uv run celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q game,llm,tools,rag
```

## 📁 项目结构

### 现代化功能域驱动架构设计

```
api/
├── core/                    # 核心功能域
│   ├── model_runtime/       # 模型运行时管理
│   │   ├── model_providers/ # 模型提供商集合
│   │   │   ├── __base/      # 基础抽象类和接口
│   │   │   ├── openai/      # OpenAI 提供商实现
│   │   │   ├── anthropic/   # Anthropic 提供商实现
│   │   │   ├── local/       # 本地模型提供商（vLLM集成）
│   │   │   ├── [更多提供商]/
│   │   │   └── model_provider_factory.py # 工厂管理器
│   │   ├── entities/        # 模型相关实体定义
│   │   ├── schema_validators/ # 配置验证器
│   │   ├── callbacks/       # 模型回调处理
│   │   ├── errors/          # 模型相关错误
│   │   └── utils/           # 模型工具函数
│   ├── workflow/            # 游戏流程引擎
│   │   ├── graph_engine/    # 游戏流程图引擎
│   │   │   ├── entities/    # 图相关实体
│   │   │   ├── game_graph.py # 游戏图结构
│   │   │   ├── game_event.py # 游戏事件定义
│   │   │   └── workflow_engine.py # 核心执行引擎
│   │   ├── nodes/           # 游戏节点类型
│   │   │   ├── base/        # 基础节点类
│   │   │   ├── llm_node/    # LLM 生成节点
│   │   │   ├── tool_node/   # 工具调用节点
│   │   │   ├── condition_node/ # 条件分支节点
│   │   │   ├── player_input_node/ # 玩家输入节点
│   │   │   ├── npc_node/    # NPC 行为节点
│   │   │   ├── dice_node/   # 骰子投掷节点
│   │   │   ├── combat_node/ # 战斗计算节点
│   │   │   ├── story_node/  # 剧情推进节点
│   │   │   ├── state_node/  # 状态管理节点
│   │   │   ├── timer_node/  # 定时器节点
│   │   │   ├── random_node/ # 随机事件节点
│   │   │   ├── inventory_node/ # 物品操作节点
│   │   │   ├── skill_check_node/ # 技能检定节点
│   │   │   ├── save_load_node/ # 存档加载节点
│   │   │   ├── multiplayer_sync_node/ # 多人同步节点
│   │   │   └── node_mapping.py # 节点类型映射
│   │   ├── entities/        # 游戏流程实体
│   │   ├── callbacks/       # 游戏事件回调
│   │   ├── repositories/    # 游戏数据访问层
│   │   ├── utils/           # 游戏工具函数
│   │   └── game_entry.py    # 游戏执行入口
│   ├── tools/               # 工具管理
│   │   ├── builtin_tool/    # 内置工具集合
│   │   │   ├── dice/        # 骰子工具
│   │   │   ├── calculator/  # 计算器工具
│   │   │   ├── random/      # 随机数生成器
│   │   │   ├── timer/       # 计时器工具
│   │   │   └── text_utils/  # 文本处理工具
│   │   ├── mcp_tool/        # MCP 协议工具
│   │   ├── game_tool/       # 游戏专用工具
│   │   │   ├── character_gen/ # 角色生成工具
│   │   │   ├── world_gen/   # 世界生成工具
│   │   │   ├── story_gen/   # 剧情生成工具
│   │   │   └── balance_check/ # 平衡性检查工具
│   │   ├── custom_tool/     # 自定义 API 工具
│   │   ├── plugin_tool/     # 插件工具
│   │   ├── __base/          # 基础抽象类
│   │   ├── entities/        # 工具实体定义
│   │   ├── utils/           # 工具工具函数
│   │   ├── tool_manager.py  # 统一工具管理器
│   │   ├── tool_engine.py   # 工具执行引擎
│   │   ├── tool_file_manager.py # 工具文件管理
│   │   ├── tool_label_manager.py # 工具标签管理
│   │   ├── errors.py        # 工具相关错误
│   │   └── signature.py     # 工具签名管理
│   ├── rag/                 # RAG 知识库
│   │   ├── datasource/      # 数据源管理
│   │   │   └── vdb/         # 向量数据库集成
│   │   │       ├── weaviate/ # Weaviate 实现
│   │   │       ├── milvus/  # Milvus 实现
│   │   │       ├── qdrant/  # Qdrant 实现
│   │   │       └── chroma/  # Chroma 实现
│   │   ├── retrieval/       # 检索算法实现
│   │   ├── rerank/          # 重排序算法
│   │   ├── embedding/       # 嵌入模型管理
│   │   ├── game_knowledge/  # 游戏知识管理
│   │   │   ├── world_setting/ # 世界设定知识
│   │   │   ├── character_knowledge/ # 角色知识
│   │   │   ├── rule_knowledge/ # 规则知识
│   │   │   ├── story_knowledge/ # 剧情知识
│   │   │   └── lore_knowledge/ # 背景知识
│   │   ├── extractor/       # 内容提取器
│   │   ├── splitter/        # 文档分割器
│   │   ├── cleaner/         # 文档清理器
│   │   ├── docstore/        # 文档存储
│   │   ├── data_post_processor/ # 数据后处理
│   │   ├── index_processor/ # 索引处理器
│   │   └── entities/        # RAG 实体定义
│   ├── player/              # 玩家管理功能域
│   │   ├── session/         # 会话管理
│   │   │   ├── game_session.py # 游戏会话管理
│   │   │   ├── player_session.py # 玩家会话管理
│   │   │   └── session_factory.py # 会话工厂
│   │   ├── character/       # 角色管理
│   │   │   ├── character_sheet.py # 角色表管理
│   │   │   ├── attributes.py # 属性系统
│   │   │   ├── skills.py    # 技能系统
│   │   │   ├── progression.py # 成长系统
│   │   │   └── character_factory.py # 角色工厂
│   │   ├── inventory/       # 物品管理
│   │   │   ├── item_manager.py # 物品管理器
│   │   │   ├── equipment.py # 装备系统
│   │   │   ├── consumables.py # 消耗品系统
│   │   │   └── inventory_factory.py # 物品工厂
│   │   ├── entities/        # 玩家相关实体
│   │   └── player_factory.py # 玩家工厂
│   ├── ops/                 # 运维监控（企业级目标，后续开发）
│   │   ├── trace/           # 链路追踪
│   │   │   ├── game_trace/  # 游戏链路追踪
│   │   │   ├── llm_trace/   # LLM 调用追踪
│   │   │   ├── player_trace/ # 玩家行为追踪
│   │   │   └── trace_manager.py # 追踪管理器
│   │   ├── metrics/         # 指标收集
│   │   │   ├── game_metrics.py # 游戏指标
│   │   │   ├── performance_metrics.py # 性能指标
│   │   │   └── business_metrics.py # 业务指标
│   │   ├── monitoring/      # 监控系统
│   │   │   ├── health_check.py # 健康检查
│   │   │   ├── alerting.py  # 告警系统
│   │   │   └── dashboard.py # 监控面板
│   │   └── logging/         # 日志系统
│   │       ├── game_logger.py # 游戏日志
│   │       ├── audit_logger.py # 审计日志
│   │       └── security_logger.py # 安全日志
│   ├── moderation/          # 审核系统（企业级目标，后续开发）
│   │   ├── content/         # 内容审核
│   │   │   ├── text_moderation.py # 文本审核
│   │   │   ├── chat_moderation.py # 聊天审核
│   │   │   └── content_filter.py # 内容过滤
│   │   ├── behavior/        # 行为审核
│   │   │   ├── player_behavior.py # 玩家行为审核
│   │   │   ├── anti_cheat.py # 反作弊系统
│   │   │   └── abuse_detection.py # 滥用检测
│   │   ├── api/             # 审核 API 集成
│   │   ├── keywords/        # 关键词审核
│   │   ├── base.py          # 审核基类
│   │   ├── factory.py       # 审核工厂
│   │   └── entities/        # 审核实体
│   ├── plugin/              # 插件系统（后续开发）
│   │   ├── backwards_invocation/ # 向后兼容调用
│   │   ├── endpoint/        # 插件端点管理
│   │   ├── security/        # 插件安全机制
│   │   │   ├── sandbox.py   # 沙箱环境
│   │   │   ├── permission.py # 权限控制
│   │   │   └── isolation.py # 隔离机制
│   │   ├── lifecycle/       # 插件生命周期
│   │   │   ├── loader.py    # 插件加载器
│   │   │   ├── manager.py   # 插件管理器
│   │   │   └── registry.py  # 插件注册表
│   │   ├── entities/        # 插件实体定义
│   │   ├── impl/            # 插件实现
│   │   └── utils/           # 插件工具函数
│   ├── memory/              # 内存管理
│   │   ├── token_buffer_memory.py # Token 缓冲区
│   │   ├── game_state_memory.py # 游戏状态内存
│   │   ├── player_memory.py # 玩家记忆管理
│   │   └── conversation_memory.py # 对话记忆
│   ├── variables/           # 变量系统
│   │   ├── game_variables/  # 游戏变量
│   │   ├── player_variables/ # 玩家变量
│   │   ├── session_variables/ # 会话变量
│   │   ├── segments.py      # 变量片段
│   │   ├── types.py         # 变量类型
│   │   ├── utils.py         # 变量工具
│   │   ├── variables.py     # 变量主体
│   │   └── variable_factory.py # 变量工厂
│   ├── file/                # 文件管理
│   │   ├── game_assets/     # 游戏资源文件
│   │   ├── user_uploads/    # 用户上传文件
│   │   ├── models.py        # 文件模型定义
│   │   ├── file_manager.py  # 文件管理器
│   │   ├── helpers.py       # 文件助手函数
│   │   ├── constants.py     # 文件常量
│   │   └── enums.py         # 文件枚举
│   ├── extension/           # 扩展系统
│   │   ├── game_extensions/ # 游戏扩展
│   │   ├── api_based_extension_requestor.py # 基于 API 的扩展
│   │   ├── extensible.py    # 可扩展性基类
│   │   └── extension.py     # 扩展基类
│   ├── entities/            # 核心实体定义
│   │   ├── game_entities.py # 游戏实体
│   │   ├── player_entities.py # 玩家实体
│   │   ├── model_entities.py # 模型实体
│   │   ├── tool_entities.py # 工具实体
│   │   └── provider_entities.py # 提供商实体
│   ├── repositories/        # 仓储模式实现
│   │   ├── game_repository.py # 游戏仓储
│   │   ├── player_repository.py # 玩家仓储
│   │   ├── factory.py       # 仓储工厂
│   │   └── base.py          # 基础仓储类
│   ├── callback_handler/    # 回调处理
│   │   ├── game_callback_handler.py # 游戏回调
│   │   ├── tool_callback_handler.py # 工具回调
│   │   └── player_callback_handler.py # 玩家回调
│   ├── helper/              # 辅助工具集合
│   │   ├── game_helper/     # 游戏助手
│   │   ├── crypto/          # 加密工具
│   │   ├── cache/           # 缓存工具
│   │   ├── validation/      # 验证工具
│   │   └── networking/      # 网络工具
│   └── errors/              # 错误处理
│       ├── game_errors.py   # 游戏相关错误
│       ├── player_errors.py # 玩家相关错误
│       ├── model_errors.py  # 模型相关错误
│       └── base_errors.py   # 基础错误类
├── controllers/             # API 控制器（按场景分组）
│   ├── console/            # 管理控制台 API（游戏管理员）
│   │   ├── __init__.py
│   │   ├── games.py        # 游戏管理接口
│   │   ├── models.py       # 模型管理接口
│   │   ├── tools.py        # 工具管理接口
│   │   ├── knowledge.py    # 知识库管理接口
│   │   ├── plugins.py      # 插件管理接口
│   │   ├── monitoring.py   # 监控管理接口
│   │   ├── moderation.py   # 审核管理接口
│   │   └── system.py       # 系统管理接口
│   ├── web/                # Web 应用 API（玩家使用）
│   │   ├── __init__.py
│   │   ├── games.py        # 游戏参与接口
│   │   ├── chat.py         # 游戏对话接口
│   │   ├── characters.py   # 角色管理接口
│   │   ├── inventory.py    # 物品管理接口
│   │   ├── auth.py         # 用户认证接口
│   │   ├── social.py       # 社交功能接口
│   │   └── files.py        # 文件操作接口
│   ├── service_api/        # 服务 API（系统集成）
│   │   ├── __init__.py
│   │   ├── webhooks.py     # Webhook 接口
│   │   ├── integrations.py # 第三方集成接口
│   │   └── external.py     # 外部系统接口
│   ├── inner_api/          # 内部 API（微服务间通信）
│   │   ├── __init__.py
│   │   ├── health.py       # 健康检查接口
│   │   ├── metrics.py      # 指标接口
│   │   └── maintenance.py  # 维护接口
│   └── common/             # 通用 API 组件
│       ├── __init__.py
│       ├── decorators.py   # 通用装饰器
│       ├── validators.py   # 通用验证器
│       └── responses.py    # 通用响应格式
├── services/                # 业务服务层（扁平化组织）
│   ├── __init__.py
│   ├── game_service.py     # 游戏管理服务（核心编排）
│   ├── model_provider_service.py # 模型提供商服务
│   ├── conversation_service.py # 对话服务
│   ├── tool_service.py     # 工具服务管理
│   ├── rag_service.py      # RAG 知识库服务
│   ├── player_service.py   # 玩家管理服务
│   ├── character_service.py # 角色管理服务
│   ├── inventory_service.py # 物品管理服务
│   ├── session_service.py  # 会话管理服务
│   ├── plugin_service.py   # 插件管理服务
│   ├── monitoring_service.py # 监控服务（企业级目标，后续开发）
│   ├── moderation_service.py # 审核服务（企业级目标，后续开发）
│   ├── file_service.py     # 文件服务
│   ├── notification_service.py # 通知服务
│   ├── analytics_service.py # 分析服务（企业级目标，后续开发）
│   └── billing_service.py  # 计费服务（企业级目标，后续开发）
├── models/                  # 数据模型（扁平化）
│   ├── __init__.py
│   ├── base.py             # 基础模型类
│   ├── game.py             # 游戏模型（核心业务模型）
│   ├── player.py           # 玩家模型
│   ├── character.py        # 角色模型
│   ├── conversation.py     # 对话模型
│   ├── session.py          # 会话模型
│   ├── inventory.py        # 物品模型
│   ├── tool.py             # 工具模型
│   ├── knowledge.py        # 知识库模型
│   ├── plugin.py           # 插件模型（后续开发）
│   ├── trace.py            # 追踪模型
│   └── billing.py          # 计费模型（企业级目标，后续开发）
├── repositories/            # 数据访问层
│   ├── __init__.py
│   ├── base.py             # 基础仓储类
│   ├── game.py             # 游戏数据访问
│   ├── player.py           # 玩家数据访问
│   ├── character.py        # 角色数据访问
│   ├── conversation.py     # 对话数据访问
│   ├── session.py          # 会话数据访问
│   └── inventory.py        # 物品数据访问
├── extensions/              # Flask 扩展配置
│   ├── __init__.py
│   ├── ext_database.py     # 数据库扩展
│   ├── ext_redis.py        # Redis 扩展
│   ├── ext_celery.py       # Celery 扩展
│   ├── ext_cors.py         # CORS 扩展
│   ├── ext_monitoring.py   # 监控扩展
│   ├── ext_tracing.py      # 追踪扩展
│   ├── ext_security.py     # 安全扩展
│   ├── ext_storage.py      # 存储扩展
│   ├── ext_mail.py         # 邮件扩展
│   ├── ext_logging.py      # 日志扩展
│   └── [更多扩展]
├── configs/                 # 配置管理（分层配置）
│   ├── __init__.py
│   ├── settings.py         # 应用配置
│   ├── constants.py        # 常量定义
│   ├── feature/            # 功能特性配置
│   ├── deploy/             # 部署配置
│   ├── monitoring/         # 监控配置
│   └── security/           # 安全配置
├── entities/                # 数据传输对象
│   ├── __init__.py
│   ├── game.py             # 游戏相关 DTO
│   ├── player.py           # 玩家相关 DTO
│   ├── character.py        # 角色相关 DTO
│   ├── conversation.py     # 对话相关 DTO
│   ├── response.py         # 通用响应 DTO
│   └── api_entities.py     # API 实体定义
├── contexts/                # 上下文管理
│   ├── __init__.py
│   ├── tenant.py           # 多租户上下文
│   ├── game.py             # 游戏上下文
│   ├── player.py           # 玩家上下文
│   └── request.py          # 请求上下文
├── libs/                    # 共享工具库
│   ├── __init__.py
│   ├── helper.py           # 辅助函数
│   ├── validators.py       # 数据验证
│   ├── exceptions.py       # 异常定义
│   ├── crypto.py           # 加密工具
│   ├── datetime_utils.py   # 日期时间工具
│   ├── json_utils.py       # JSON 工具
│   ├── http_utils.py       # HTTP 工具
│   ├── file_utils.py       # 文件工具
│   └── game_utils.py       # 游戏专用工具
├── factories/               # 工厂类（全面工厂模式）
│   ├── __init__.py
│   ├── model_factory.py    # 模型工厂
│   ├── game_factory.py     # 游戏工厂
│   ├── player_factory.py   # 玩家工厂
│   ├── character_factory.py # 角色工厂
│   ├── tool_factory.py     # 工具工厂
│   ├── plugin_factory.py   # 插件工厂
│   └── service_factory.py  # 服务工厂
├── events/                  # 事件系统
│   ├── __init__.py
│   ├── game_events.py      # 游戏事件
│   ├── player_events.py    # 玩家事件
│   ├── system_events.py    # 系统事件
│   └── event_handlers/     # 事件处理器
├── tasks/                   # 异步任务
│   ├── __init__.py
│   ├── game_tasks.py       # 游戏相关任务
│   ├── player_tasks.py     # 玩家相关任务
│   ├── cleanup_tasks.py    # 清理任务
│   ├── monitoring_tasks.py # 监控任务
│   ├── notification_tasks.py # 通知任务
│   └── [更多任务类型]
├── tests/                   # 测试代码
│   ├── __init__.py
│   ├── unit_tests/         # 单元测试
│   ├── integration_tests/  # 集成测试
│   ├── performance_tests/  # 性能测试
│   ├── security_tests/     # 安全测试
│   └── fixtures/           # 测试数据
├── migrations/              # 数据库迁移
├── constants/               # 常量定义
├── fields/                  # 自定义字段
├── schedule/                # 定时任务
├── templates/               # 模板文件
├── app.py                   # 应用入口
├── app_factory.py           # 应用工厂
└── pyproject.toml          # 项目配置
```

## 🧩 核心模块详细说明

### `core/` - 核心功能域

#### `core/model_runtime/` - 模型运行时管理

基于工厂模式设计，提供统一的模型管理接口：

**核心特性**：
- **多模型提供商**：支持主流 LLM 提供商的统一管理
- **动态加载机制**：运行时动态注册新提供商
- **配置验证系统**：自动验证和修复配置错误
- **回调处理机制**：完整的模型调用生命周期管理
- **错误恢复机制**：自动故障转移和降级策略

**工厂模式实现**：
```python
# 模型提供商工厂
class ModelProviderFactory:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.provider_cache = {}
        self.fallback_chains = {}  # 故障转移链
        self.load_balancer = LoadBalancer()  # 负载均衡
    
    def get_provider_instance(self, provider: str) -> AIModel:
        # 支持负载均衡和故障转移的提供商获取
        pass
    
    def register_provider(self, provider_class: Type[AIModel]):
        # 动态注册新提供商
        pass
```

#### `core/workflow/` - 事件驱动游戏流程引擎

借鉴 Dify workflow 设计，构建特化的对话游戏编排引擎

**丰富的游戏节点类型**：
- **基础节点**：开始、结束、条件分支
- **游戏逻辑节点**：骰子投掷、技能检定、战斗计算
- **交互节点**：玩家输入、NPC对话、选择分支
- **状态节点**：属性修改、物品管理、存档加载
- **高级节点**：多人同步、定时器、随机事件

**事件驱动实现**：
```python
# 游戏流程引擎
class WorkflowEngine:
    def __init__(self, graph: GameGraph):
        self.graph = graph
        self.event_bus = EventBus()
        self.state_manager = StateManager()
    
    def execute_node(self, node: GameNode, context: GameContext) -> Generator[GameEvent, None, None]:
        # 支持事件驱动的节点执行
        pass
```

#### `core/tools/` - 工具管理系统

统一的工具集成和管理系统：

**工具类型**：
- **内置工具**：骰子、计算器、随机数、计时器
- **游戏专用工具**：角色生成、世界生成、剧情生成、平衡性检查
- **MCP 工具**：标准协议工具集成
- **自定义工具**：用户自定义 API 工具
- **插件工具**：第三方插件工具

#### `core/rag/` - 游戏知识库系统

专门针对游戏场景的知识管理：

**游戏知识类型**：
- **世界设定知识**：地理、历史、文化背景
- **角色知识**：NPC信息、关系网络、行为模式
- **规则知识**：游戏规则、技能说明、平衡数据
- **剧情知识**：故事线索、分支结构、结局条件
- **背景知识**：传说、神话、世界观设定

#### `core/ops/` - 运维监控体系（后续开发）

为企业级部署预留的运维监控功能：

**监控追踪系统**：
- **游戏链路追踪**：完整的游戏流程追踪
- **LLM 调用追踪**：模型调用性能和成本监控
- **玩家行为追踪**：用户行为分析和异常检测

**指标收集系统**：
- **游戏指标**：在线人数、游戏时长、完成率
- **性能指标**：响应时间、吞吐量、错误率
- **业务指标**：留存率、付费率、满意度

#### `core/moderation/` - 安全审核系统（后续开发）

为企业级部署预留的安全审核功能：

**内容审核**：
- **文本审核**：敏感词过滤、内容分级
- **聊天审核**：实时聊天监控、违规检测
- **内容过滤**：智能内容分类和过滤

**行为审核**：
- **玩家行为审核**：异常行为检测
- **反作弊系统**：作弊行为识别和防护
- **滥用检测**：系统滥用和攻击检测

#### `core/plugin/` - 插件扩展系统（后续开发）

为生态扩展预留的插件系统：

**插件安全机制**：
- **沙箱环境**：插件安全执行环境
- **权限控制**：细粒度的插件权限管理
- **隔离机制**：插件间的安全隔离

**插件生命周期**：
- **插件加载器**：动态插件加载和卸载
- **插件管理器**：插件状态管理和监控
- **插件注册表**：插件发现和版本管理

### `services/` - 业务服务层

采用扁平化服务设计，每个服务专注特定业务领域：

**核心服务**：
- `game_service.py` - 游戏管理服务（核心编排）
- `model_provider_service.py` - 模型提供商服务
- `conversation_service.py` - 对话服务
- `tool_service.py` - 工具管理服务
- `rag_service.py` - 知识库服务
- `player_service.py` - 玩家管理服务
- `character_service.py` - 角色管理服务

**扩展服务**（后续开发）：
- `monitoring_service.py` - 监控服务
- `moderation_service.py` - 审核服务
- `plugin_service.py` - 插件管理服务
- `analytics_service.py` - 分析服务
- `billing_service.py` - 计费服务

### `controllers/` - 按场景分组的API

#### `controllers/console/` - 管理控制台 API
管理员功能：
- 游戏设计管理、模型管理、工具管理
- 插件管理、监控管理、审核管理
- 系统管理、安全管理

#### `controllers/web/` - 玩家 API
游戏体验功能：
- 游戏参与、对话交互、角色管理
- 物品管理、社交功能、文件操作

#### `controllers/service_api/` - 系统集成 API
第三方集成功能：
- Webhook接口、外部系统集成
- API 标准化接口

## 🔧 技术栈

- **Web 框架**: Flask 3.x
- **包管理**: UV（高性能 Python 包管理器）
- **数据库**: PostgreSQL（主数据库）+ Redis（缓存和队列）
- **向量数据库**: Weaviate（默认）+ Milvus + Qdrant + Chroma（可选）
- **任务队列**: Celery（异步任务处理）
- **工具协议**: MCP（Model Context Protocol）
- **代码质量**: Ruff（格式化和检查）+ MyPy（类型检查）
- **测试框架**: Pytest
- **容器化**: Docker
- **监控追踪**: OpenTelemetry（后续开发）

## 📚 相关文档

- [项目整体介绍](../README.md) - 项目概述和愿景
- [Docker 部署指南](../docker/README.md) - 部署配置说明
- [前端开发指南](../web/README.md) - Web 前端开发