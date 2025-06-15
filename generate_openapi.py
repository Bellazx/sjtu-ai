import sys
from pathlib import Path
from __init__ import create_app
import yaml

# 设置项目根目录
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

app = create_app()
with app.app_context():
    with app.test_request_context():
    # 获取完整的 OpenAPI 规范
        openapi_spec = app.api.__schema__

        # 转换为标准 OpenAPI 格式
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "图书馆管理系统 API",
                "description": "图书馆管理系统的API接口文档",
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": "http://172.20.0.3:8888",
                    "description": "本地开发服务器"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {}
            }
        }

        # 处理路径
        for path, methods in openapi_spec.get("paths", {}).items():
            spec["paths"][path] = {}
            for method, details in methods.items():
                spec["paths"][path][method] = {
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "operationId": details.get("operationId", ""),
                    "parameters": details.get("parameters", []),
                    "responses": {
                        "200": {
                            "description": "成功",
                            "content": {
                                "application/json": {
                                    "schema": details.get("responses", {}).get("200", {}).get("schema", {})
                                }
                            }
                        },
                        "400": {
                            "description": "请求参数错误",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "success": {"type": "boolean"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

        # 处理模型定义
        for name, schema in openapi_spec.get("definitions", {}).items():
            spec["components"]["schemas"][name] = schema

        # 将规范转换为 YAML 格式
        yaml_spec = yaml.dump(spec, allow_unicode=True, sort_keys=False, default_flow_style=False)

        # 保存到文件
        with open('openapi.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml_spec)
