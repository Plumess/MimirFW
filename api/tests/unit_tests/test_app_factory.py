"""
测试应用工厂模块

验证应用创建和配置功能
"""

from flask import Flask

from app_factory import create_app, create_flask_app_with_configs, create_migrations_app


class TestAppFactory:
    """测试应用工厂功能"""

    def test_create_flask_app_with_configs(self) -> None:
        """测试创建带配置的 Flask 应用"""
        app = create_flask_app_with_configs()

        assert isinstance(app, Flask)
        # Flask 应用名称默认是模块名，这里是 __main__
        assert app.name in ["__main__", "app_factory"]

    def test_create_app(self) -> None:
        """测试创建完整应用"""
        app = create_app()

        assert isinstance(app, Flask)
        # Flask 应用名称默认是模块名
        assert app.name in ["__main__", "app_factory"]

    def test_health_endpoint(self) -> None:
        """测试健康检查端点"""
        app = create_app()

        with app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 200

            data = response.get_json()
            assert data["status"] == "healthy"
            assert "service" in data
            assert "version" in data
            assert "environment" in data

    def test_root_endpoint(self) -> None:
        """测试根端点"""
        app = create_app()

        with app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200

            data = response.get_json()
            assert data["service"] == "MimirFW API"
            assert data["status"] == "running"
            assert "version" in data
            assert "environment" in data
            assert "debug" in data

    def test_404_error_handler(self) -> None:
        """测试 404 错误处理"""
        app = create_app()

        with app.test_client() as client:
            response = client.get("/nonexistent")
            assert response.status_code == 404

            data = response.get_json()
            assert data["error"] == "Not Found"
            assert "message" in data
            assert "service" in data
            assert "version" in data

    def test_error_handlers_registered(self) -> None:
        """测试错误处理器是否注册"""
        app = create_app()

        # 检查错误处理器是否已注册
        assert 404 in app.error_handler_spec[None]
        assert 500 in app.error_handler_spec[None]

    def test_create_migrations_app(self) -> None:
        """测试创建迁移应用"""
        app = create_migrations_app()

        assert isinstance(app, Flask)
        # Flask 应用名称默认是模块名
        assert app.name in ["__main__", "app_factory"]

    def test_app_config_loading(self) -> None:
        """测试应用配置加载"""
        app = create_flask_app_with_configs()

        # 检查配置是否正确加载
        assert "APPLICATION_NAME" in app.config
        assert app.config["APPLICATION_NAME"] == "MimirFW"
        assert "DEBUG" in app.config
        assert isinstance(app.config["DEBUG"], bool)

    def test_extensions_initialization_skipped(self) -> None:
        """测试扩展初始化被跳过（因为未实现）"""
        app = create_app()

        # 当前扩展初始化被跳过，应用仍能正常创建
        assert isinstance(app, Flask)

    def test_routes_registered(self) -> None:
        """测试路由是否正确注册"""
        app = create_app()

        # 检查基本路由是否注册
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        assert "/" in routes
        assert "/health" in routes
