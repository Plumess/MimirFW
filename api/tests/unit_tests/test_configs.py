"""
配置模块单元测试

测试配置加载和验证
"""

from configs import MimirConfig, mimir_config


class TestMimirConfig:
    """MimirConfig 测试类"""

    def test_mimir_config_instance(self) -> None:
        """测试全局配置实例可用"""
        assert mimir_config is not None
        assert isinstance(mimir_config, MimirConfig)

    def test_required_fields_present(self) -> None:
        """测试必需的配置字段存在"""
        # 应用基础信息
        assert hasattr(mimir_config, "APPLICATION_NAME")
        assert hasattr(mimir_config, "VERSION")
        assert hasattr(mimir_config, "DESCRIPTION")

        # 部署配置
        assert hasattr(mimir_config, "DEBUG")
        assert hasattr(mimir_config, "DEPLOY_ENV")
        assert hasattr(mimir_config, "API_PORT")

        # 数据库配置
        assert hasattr(mimir_config, "SQLALCHEMY_DATABASE_URI")
        assert hasattr(mimir_config, "DB_HOST")
        assert hasattr(mimir_config, "DB_PORT")

        # Redis 配置
        assert hasattr(mimir_config, "REDIS_HOST")
        assert hasattr(mimir_config, "REDIS_PORT")

    def test_computed_fields(self) -> None:
        """测试动态计算字段"""
        # 测试数据库 URI 动态生成
        uri = mimir_config.SQLALCHEMY_DATABASE_URI
        assert uri.startswith("postgresql://")
        assert mimir_config.DB_HOST in uri
        assert str(mimir_config.DB_PORT) in uri
        assert mimir_config.DB_DATABASE in uri

    def test_default_values(self) -> None:
        """测试默认值"""
        assert mimir_config.APPLICATION_NAME == "MimirFW"
        assert mimir_config.VERSION == "0.1.0"
        assert mimir_config.API_PORT == 8000
        assert mimir_config.DB_PORT == 5432
        assert mimir_config.REDIS_PORT == 6379

    def test_type_validation(self) -> None:
        """测试类型验证"""
        assert isinstance(mimir_config.DEBUG, bool)
        assert isinstance(mimir_config.API_PORT, int)
        assert isinstance(mimir_config.DB_PORT, int)
        assert isinstance(mimir_config.REDIS_PORT, int)
        assert isinstance(mimir_config.APPLICATION_NAME, str)
