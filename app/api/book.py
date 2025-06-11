from flask import request, current_app
from flask_restx import Resource, Namespace

def init_book_api(api, models):
    ns = Namespace('/test', description='图书馆管理系统接口')
    
    @ns.route('/check_book_can_renew')
    class BookRenew(Resource):
        @ns.doc('check_book_can_renew')
        @ns.param('book_id', '图书唯一标识符', required=True)
        @ns.response(200, '成功', models['renew_check_response'])
        @ns.response(400, '错误', models['error_model'])
        def get(self):
            """检查图书是否可以续借"""
            book_id = request.args.get('book_id')
            if not book_id:
                return {
                    "error": "book_id is required",
                    "status": "error"
                }, 400
            if book_id == "book_ztr":
                return {
                    "data": {
                        "can_renew": False
                    },
                    "status": "success"
                }
            return {
                "data": {
                    "can_renew": True
                },
                "status": "success"
            }

    return ns 