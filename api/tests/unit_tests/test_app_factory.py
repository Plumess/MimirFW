"""
应用工厂单元测试

测试 Flask 应用的创建和配置。
"""

import pytest
from flask import Flask

from app_factory import create_app
from configs import DevelopmentConfig, ProductionConfig, TestEnvConfig


class TestAppFactory:
    """应用工厂测试类"""

    def test_create_app_with_default_config(self) -> None:
        """测试使用默认配置创建应用"""
        app = create_app()

        assert isinstance(app, Flask)
        # 在测试环境下，默认配置实际上是 TestEnvConfig
        assert app.config["DEBUG"] is False  # 测试环境不开启 DEBUG
        assert "SECRET_KEY" in app.config
        assert app.config["APP_NAME"] == "MimirFW API"

        def test_create_app_with_development_config(self) -> None:
        """测试使用开发配置创建应用"""
        config = DevelopmentConfig()
        app = create_app(config)

        assert app.config["DEBUG"] is True
        # 注意：即使传入 DevelopmentConfig，环境变量 FLASK_ENV=testing 仍会影响配置
        assert app.config["FLASK_ENV"] == "development"  # 来自配置对象
        assert app.config["SQLALCHEMY_ECHO"] is True

    def test_create_app_with_testing_config(self) -> None:
        """测试使用测试配置创建应用"""
        config = TestEnvConfig()
        app = create_app(config)
        
        assert app.config["DEBUG"] is False
        assert app.config["FLASK_ENV"] == "testing"
        assert app.config["TESTING"] is True

    def test_health_check_endpoint(self) -> None:
        """测试健康检查端点"""
        app = create_app()
        
        with app.test_client() as client:
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.get_json()
            assert data["status"] == "healthy"
            assert data["service"] == "mimirfw-api"

    def test_root_endpoint(self) -> None:
        """测试根端点"""
        app = create_app()
        
        with app.test_client() as client:
            response = client.get("/")
            
            assert response.status_code == 200
            data = response.get_json()
            assert data["service"] == "MimirFW API"
            assert data["version"] == "0.1.0"
            assert data["status"] == "running"
            assert "environment" in data

    def test_404_error_handler(self) -> None:
        """测试 404 错误处理"""
        app = create_app()
        
        with app.test_client() as client:
            response = client.get("/nonexistent")
            
            assert response.status_code == 404
            data = response.get_json()
            assert data["error"] == "Not Found" 