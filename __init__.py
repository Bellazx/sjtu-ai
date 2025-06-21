from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.config import Config

from app.models.schemas import init_models
from app.api.user import init_user_api
from app.api.book import init_book_api
from app.api.login import init_login_api
from app.api.api import call_api   

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # 加载配置类

    # 配置跨域资源共享(CORS)
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],  # 从配置文件获取允许的来源
         methods=app.config['CORS_METHODS'],  # 允许的HTTP方法
         allow_headers=app.config['CORS_ALLOW_HEADERS'],  # 允许的请求头
         supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS']  # 支持携带认证信息
    )
    api = Api(app, version='1.0', title='图书馆管理系统 API',
        description='图书馆管理系统的API接口文档',
        doc='/docs',
        prefix='/lib'
    )
    app.api = api
    # 初始化数据模型
    models = init_models(api)

    # 注册API命名空间
    api.add_namespace(init_user_api(api, models))
    api.add_namespace(init_book_api(api, models))
    api.add_namespace(init_login_api(api, models))
    # api.add_namespace(init_room_api(api, models))

    return app


def main():
    app = create_app()
    app.run(host='0.0.0.0', port=8888, debug=True)

if __name__ == "__main__":
    main() 