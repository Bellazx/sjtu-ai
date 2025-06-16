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
        
                # 动态获取所有已注册的命名空间信息
        namespace_mapping = {}
        print("已注册的命名空间:")
        
        # 简化的方法：直接从已注册的命名空间获取路径信息
        for ns in app.api.namespaces:
            # 清理命名空间路径
            namespace_path = ns.path
            if namespace_path == '/':
                namespace_path = ''
            else:
                namespace_path = namespace_path.rstrip('/')
            
            print(f"  命名空间: '{namespace_path}' (原始: '{ns.path}')")
            
            # 将命名空间路径存储到映射中
            if namespace_path:
                # 提取命名空间名称（路径的最后一部分）
                namespace_name = namespace_path.split('/')[-1] if '/' in namespace_path else namespace_path.lstrip('/')
                if namespace_name:
                    namespace_mapping[namespace_name] = namespace_path
                    print(f"    映射: {namespace_name} -> {namespace_path}")
        
        print(f"\n命名空间映射表: {namespace_mapping}")
        
        # 从URL规则中补充路由信息
        print("\n从Flask URL规则中发现的路由:")
        for rule in app.url_map.iter_rules():
            if rule.rule.startswith('/lib/'):
                print(f"  规则: {rule.rule} -> 端点: {rule.endpoint}")
                
                # 从完整路径提取信息
                path_parts = rule.rule.split('/')
                if len(path_parts) >= 3:  # /lib/namespace/route
                    namespace = path_parts[2] if len(path_parts) > 2 else ''
                    route = '/'.join(path_parts[3:]) if len(path_parts) > 3 else ''
                    
                    if namespace and route:
                        # 清理路由，移除参数
                        clean_route = '/' + route.split('<')[0].rstrip('/')
                        if clean_route != '/':
                            namespace_mapping[clean_route] = f'/{namespace}{clean_route}'
                            print(f"    路由映射: {clean_route} -> /{namespace}{clean_route}")
        
        print(f"\n最终路径映射表: {namespace_mapping}")

        # 转换为标准 OpenAPI 格式
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "图书馆智能AI系统 API",
                "description": "图书馆智能AI系统的API接口文档",
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
        print(f"\n开始处理 {len(openapi_spec.get('paths', {}))} 个原始路径:")
        for path, methods in openapi_spec.get("paths", {}).items():
            print(f"原始路径: {path}")
            
            # 构建完整路径
            clean_path = path.strip()
            if not clean_path.startswith('/'):
                clean_path = '/' + clean_path
                
            # 构建最终路径
            final_path = clean_path
            
            # 如果路径已经包含/lib前缀，直接使用
            if clean_path.startswith('/lib/'):
                final_path = clean_path
            elif clean_path.startswith('/lib'):
                # 如果是/lib但没有后面的斜杠，添加斜杠
                final_path = clean_path.replace('/lib', '/lib/', 1)
            else:
                # 路径不包含/lib前缀，需要构建完整路径
                # 先从实际的URL规则中查找匹配
                matched = False
                for rule in app.url_map.iter_rules():
                    if rule.rule.startswith('/lib/') and rule.rule.endswith(clean_path):
                        final_path = rule.rule.split('<')[0].rstrip('/')  # 移除参数部分
                        if not final_path.endswith('/'):
                            final_path = final_path
                        matched = True
                        print(f"  从URL规则匹配到: {final_path}")
                        break
                
                # 如果没有匹配到，使用简单的路径构建
                if not matched:
                    # 根据路径内容推断命名空间
                    if any(keyword in clean_path for keyword in ['user', 'get_user', 'can_book']):
                        final_path = '/lib/user' + clean_path
                    elif any(keyword in clean_path for keyword in ['book', 'renew']):
                        final_path = '/lib/book' + clean_path
                    elif any(keyword in clean_path for keyword in ['auth', 'encrypt', 'login']):
                        final_path = '/lib/auth' + clean_path
                    else:
                        final_path = '/lib' + clean_path
            
            # 清理路径，去除重复斜杠
            while '//' in final_path:
                final_path = final_path.replace('//', '/')
                
            print(f"最终路径: {final_path}")
            spec["paths"][final_path] = {}
            for method, details in methods.items():
                method_spec = {
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "operationId": details.get("operationId", ""),
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
                
                # 处理parameters（用于GET请求的查询参数）
                if details.get("parameters"):
                    method_spec["parameters"] = details.get("parameters", [])
                
                # 处理requestBody（用于POST请求的请求体）
                if details.get("requestBody"):
                    method_spec["requestBody"] = details.get("requestBody")
                
                spec["paths"][final_path][method] = method_spec

        # 处理模型定义
        for name, schema in openapi_spec.get("definitions", {}).items():
            spec["components"]["schemas"][name] = schema

        # 将规范转换为 YAML 格式
        yaml_spec = yaml.dump(
            spec, 
            allow_unicode=True, 
            sort_keys=False, 
            default_flow_style=False,
            width=float('inf'),  # 避免自动换行
            indent=2,           # 设置缩进为2个空格
            explicit_start=False,  # 不添加文档开始标记
            explicit_end=False     # 不添加文档结束标记
        )

        # 保存到文件
        with open('openapi.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml_spec)
            
        print(f"\n✅ OpenAPI 规范已成功生成到 openapi.yaml 文件")
        print(f"📝 生成了 {len(spec['paths'])} 个API路径:")
        for path in spec['paths'].keys():
            print(f"   - {path}")
        print(f"🔧 生成了 {len(spec['components']['schemas'])} 个数据模型")
