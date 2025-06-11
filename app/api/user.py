from flask import request, current_app
from flask_restx import Resource, Namespace

def init_user_api(api, models):
    ns = Namespace(current_app.config['API_PREFIX'], description='图书馆管理系统接口')
    
    @ns.route('/get_user_info')
    class UserInfo(Resource):
        @ns.doc('get_user_info')
        @ns.param('user_id', '用户唯一标识符', required=True)
        @ns.response(200, '成功', models['user_info_response'])
        @ns.response(400, '错误', models['error_model'])
        def get(self):
            """获取用户信息接口"""
            user_id = request.args.get('user_id')
            if not user_id:
                return {
                    "error": "user_id is required",
                    "status": "error"
                }, 400
            
            if user_id == "user_1234567890":
                return {
                    "data": {
                        "user_id": "user_1234567890",
                        "user_name": "John Doe",
                        "user_email": "john.doe@example.com",
                        "user_phone": "+1234567890",
                        "user_address": "123 Main St, Anytown, USA",
                        "user_status": "expired",
                        "permission": "体制内读者",
                        "user_period_of_validity": "2024-01-01 12:00:00",
                        "ALeph_wallet": -1.5
                    },
                    "status": "success"
                }
            elif user_id == "user_1234567891":
                return {
                    "data": {
                        "user_id": "user_1234567891",
                        "user_name": "harry",
                        "user_email": "harry@example.com",
                        "user_phone": "+1234567891",
                        "user_address": "456 Main St, Anytown, USA",
                        "user_status": "active",
                        "permission": "体制内读者",
                        "user_period_of_validity": "2026-01-01 12:00:00",
                        "ALeph_wallet": -6.0
                    },
                    "status": "success"
                }
            elif user_id == "user_1234567892":
                return {
                    "data": {
                        "user_id": "user_1234567892",
                        "user_name": "Tom",
                        "user_email": "tom@example.com",
                        "user_phone": "+1234567892",
                        "user_address": "789 Main St, Anytown, USA",
                        "user_status": "active",
                        "permission": "校友卡",
                        "user_period_of_validity": "2026-01-01 12:00:00",
                        "ALeph_wallet": 100.0
                    },
                    "status": "success"
                }
            else:
                return {
                    "data": {
                        "user_id": "user_1234567893",
                        "user_name": "Maggie",
                        "user_email": "maggie@example.com",
                        "user_phone": "+1234567892",
                        "user_address": "789 Main St, Anytown, USA",
                        "user_status": "active",
                        "permission": "体制内读者",
                        "user_period_of_validity": "2026-01-01 12:00:00",
                        "ALeph_wallet": 100.0
                    },
                    "status": "success"
                }

    @ns.route('/get_user_borrow_info')
    class UserBorrowInfo(Resource):
        @ns.doc('get_user_borrow_info')
        @ns.param('user_id', '用户唯一标识符', required=True)
        @ns.response(200, '成功', models['borrow_info_response'])
        @ns.response(400, '错误', models['error_model'])
        def get(self):
            """获取用户借阅信息"""
            user_id = request.args.get('user_id')
            if not user_id:
                return {
                    "error": "user_id is required",
                    "status": "error"
                }, 400
            if user_id == "user_1234567890":
                return {
                    "data": {
                        "borrow_info": [{
                            "book_id": "book_1234567890",
                            "book_name": "Book 1",
                            "borrow_time": "2024-01-01 12:00:00",
                            "borrow_end_time": "2025-01-01 12:00:00",
                            "borrow_status": "success",
                            "borrow_user_id": "user_1234567890",
                        },{
                            "book_id": "book_1234567891",
                            "book_name": "Book 2",
                            "borrow_time": "2024-01-01 12:00:00",
                            "borrow_end_time": "2026-01-01 12:00:00",
                            "borrow_status": "success",
                            "borrow_user_id": "user_1234567891",
                        }]
                    },
                    "status": "success"
                }
            else:
                return {
                    "data": {
                        "borrow_info": [{
                            "book_id": "book_1234567890",
                            "book_name": "Book 1",
                            "borrow_time": "2024-01-01 12:00:00",
                            "borrow_end_time": "2026-01-01 12:00:00",
                            "borrow_status": "success",
                            "borrow_user_id": "user_1234567890",
                        }]
                    },
                    "status": "success"
                }

    return ns 