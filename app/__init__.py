from flask import Flask
from flask_restx import Api
from config import Config

from app.models.schemas import init_models
from app.api.user import init_user_api
from app.api.book import init_book_api
from app.api.room import init_room_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # 加载配置类

    api = Api(app, version='1.0', title='图书馆管理系统 API',
        description='图书馆管理系统的API接口文档',
        doc='/docs'
    )
    app.api = api
    # 初始化数据模型
    models = init_models(api)

    # 注册API命名空间
    api.add_namespace(init_user_api(api, models))
    api.add_namespace(init_book_api(api, models))
    api.add_namespace(init_room_api(api, models))

    return app


def main():
    app = create_app()
    app.run(host='0.0.0.0', port=8888, debug=True)

if __name__ == "__main__":
    main() 