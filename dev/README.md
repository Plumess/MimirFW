# MimirFW 开发工具与脚本

> [!NOTE]
>
> 本目录包含 MimirFW 项目的**开发辅助工具**和**自动化脚本**。
> 这些工具旨在提高开发效率，确保代码质量，并简化常见的开发任务。

## 🚀 快速开始

### 1. 环境准备
确保您已经设置好 MimirFW 的开发环境：
```bash
cd api
uv sync --dev
```

### 2. 启动开发服务
```bash
cd dev
# 启动 API 服务器
./start-api

# 启动 Celery 后台任务处理器
./start-worker
```

## 🛠️ 开发工具说明

### 📱 服务启动脚本
- **`start-api`** - 启动 Flask 开发服务器，支持热重载和调试模式
- **`start-worker`** - 启动 Celery 后台任务处理器，处理异步任务

### 🎨 代码质量工具
- **`reformat`** - 使用 Ruff 进行代码格式化和代码规范检查
- **`mypy-check`** - 运行 MyPy 静态类型检查，确保类型安全

### 📦 包管理工具
- **`update-uv`** - 更新 Python 依赖包到最新版本
- **`sync-uv`** - 同步依赖包版本，确保环境一致性

### 🧪 测试运行脚本集合 (`pytest/` 目录)
- **`pytest_all_tests.sh`** - 运行完整的测试套件
- **`pytest_unit_tests.sh`** - 运行单元测试
- **`pytest_testcontainers.sh`** - 运行容器集成测试
- **`pytest_model_runtime.sh`** - 运行模型运行时测试
- **`pytest_tools.sh`** - 运行工具管理系统测试
- **`pytest_workflow.sh`** - 运行游戏流程引擎测试
- **`pytest_vdb.sh`** - 运行向量数据库测试

## 💡 使用建议

### 日常开发流程
```bash
# 1. 代码格式化和检查
./reformat

# 2. 类型检查
./mypy-check

# 3. 运行测试
./pytest/pytest_unit_tests.sh

# 4. 启动开发服务
./start-api
```

### 持续集成检查
```bash
# 运行完整的代码质量检查
./reformat && ./mypy-check && ./pytest/pytest_all_tests.sh
```

## 📚 详细说明

更多开发相关信息，请参考：
- [后端 API 开发指南](../api/README.md)

## ⚠️ 注意事项

- 请在提交代码前运行代码质量检查工具
- 开发服务启动前确保已安装所有依赖
- 测试脚本需要在正确的 Python 环境中运行
- 某些测试可能需要额外的中间件服务（如数据库、Redis）
