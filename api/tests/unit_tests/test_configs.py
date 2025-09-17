"""
测试配置模块

验证 MimirFW 配置系统功能
"""

from configs import mimir_config


class TestMimirConfig:
    """测试 MimirConfig 配置类"""

    def test_mimir_config_instance(self) -> None:
        """测试配置实例创建"""
        assert mimir_config is not None
        assert hasattr(mimir_config, "APPLICATION_NAME")

    def test_required_fields_present(self) -> None:
        """测试必需的配置字段存在"""
        # 应用基础信息
        assert hasattr(mimir_config, "APPLICATION_NAME")
        # 版本信息从 project.version 获取
        assert hasattr(mimir_config, "project")
        assert hasattr(mimir_config.project, "version")

        # 部署配置
        assert hasattr(mimir_config, "DEBUG")
        assert hasattr(mimir_config, "DEPLOY_ENV")

        # 数据库配置
        assert hasattr(mimir_config, "DB_HOST")
        assert hasattr(mimir_config, "DB_PORT")
        assert hasattr(mimir_config, "DB_USERNAME")
        assert hasattr(mimir_config, "DB_DATABASE")

    def test_computed_fields(self) -> None:
        """测试计算字段"""
        # 测试数据库 URI 计算字段
        assert hasattr(mimir_config, "SQLALCHEMY_DATABASE_URI")
        assert isinstance(mimir_config.SQLALCHEMY_DATABASE_URI, str)
        assert "postgresql://" in mimir_config.SQLALCHEMY_DATABASE_URI

        # 测试 CORS 计算字段
        assert hasattr(mimir_config, "CONSOLE_CORS_ALLOW_ORIGINS")
        assert isinstance(mimir_config.CONSOLE_CORS_ALLOW_ORIGINS, list)

    def test_default_values(self) -> None:
        """测试默认值"""
        assert mimir_config.APPLICATION_NAME == "MimirFW"
        # 版本从 project.version 获取
        assert mimir_config.project.version == "0.1.0"
        assert mimir_config.DB_HOST == "localhost"
        assert mimir_config.DB_PORT == 5432
        assert mimir_config.REDIS_HOST == "localhost"
        assert mimir_config.REDIS_PORT == 6379

    def test_type_validation(self) -> None:
        """测试类型验证"""
        assert isinstance(mimir_config.DEBUG, bool)
        assert isinstance(mimir_config.DB_PORT, int)
        assert isinstance(mimir_config.REDIS_PORT, int)
        assert isinstance(mimir_config.APPLICATION_NAME, str)

    def test_storage_config(self) -> None:
        """测试存储配置"""
        assert hasattr(mimir_config, "STORAGE_TYPE")
        assert mimir_config.STORAGE_TYPE == "opendal"

    def test_vector_store_config(self) -> None:
        """测试向量数据库配置"""
        assert hasattr(mimir_config, "VECTOR_STORE")
        assert mimir_config.VECTOR_STORE == "weaviate"

        # Weaviate 配置
        assert hasattr(mimir_config, "WEAVIATE_ENDPOINT")
        assert mimir_config.WEAVIATE_ENDPOINT == "http://localhost:8080"

    def test_feature_config_fields(self) -> None:
        """测试功能配置字段"""
        # 测试一些关键的功能配置
        assert hasattr(mimir_config, "SECRET_KEY")
        assert hasattr(mimir_config, "WORKFLOW_MAX_EXECUTION_STEPS")
        assert hasattr(mimir_config, "APP_MAX_EXECUTION_TIME")
        assert hasattr(mimir_config, "FILES_URL")

    def test_middleware_config_fields(self) -> None:
        """测试中间件配置字段"""
        # Redis 配置
        assert hasattr(mimir_config, "REDIS_HOST")
        assert hasattr(mimir_config, "REDIS_PORT")
        assert hasattr(mimir_config, "REDIS_DB")

        # Celery 配置
        assert hasattr(mimir_config, "CELERY_BACKEND")
        assert hasattr(mimir_config, "CELERY_RESULT_BACKEND")

        # 数据库配置
        assert hasattr(mimir_config, "SQLALCHEMY_DATABASE_URI")
        assert hasattr(mimir_config, "SQLALCHEMY_ENGINE_OPTIONS")
