# from flask import request, current_app
# from flask_restx import Resource, Namespace
#
# def init_room_api(api, models):
#     ns = Namespace('/lib', description='图书馆管理系统接口')
#
#     @ns.route('/check_user_can_reserve_room')
#     class RoomReserve(Resource):
#         @ns.doc('check_user_can_reserve_room')
#         @ns.param('user_id', '用户唯一标识符', required=True)
#         @ns.response(200, '成功', models['reserve_check_response'])
#         @ns.response(400, '错误', models['error_model'])
#         def get(self):
#             """检查用户是否可以预约座位"""
#             user_id = request.args.get('user_id')
#             if not user_id:
#                 return {
#                     "error": "user_id is required",
#                     "status": "error"
#                 }, 400
#             return {
#                 "data": {
#                     "can_reserve_room": True
#                 },
#                 "status": "success"
#             }
#
#     @ns.route('/get_user_reserve_info')
#     class UserReserveInfo(Resource):
#         @ns.doc('get_user_reserve_info')
#         @ns.param('user_id', '用户唯一标识符', required=True)
#         @ns.response(200, '成功', models['reserve_info_response'])
#         @ns.response(400, '错误', models['error_model'])
#         def get(self):
#             """获取用户预约信息"""
#             user_id = request.args.get('user_id')
#             if not user_id:
#                 return {
#                     "error": "user_id is required",
#                     "status": "error"
#                 }, 400
#             return {
#                 "data": {
#                     "reserve_info": {
#                         "room_id": "room_1234567890",
#                         "room_name": "Room 1",
#                         "reserve_time": "2025-6-3 12:00:00",
#                         "reserve_status": "success",
#                         "reserve_user_id": "user_1234567890",
#                         "reserve_user_name": "John Doe",
#                         "reserve_room_id": "room_1234567890",
#                         "reserve_start_time": "2025-6-3 12:00:00",
#                         "reserve_end_time": "2025-6-13 12:00:00",
#                     }
#                 },
#                 "status": "success"
#             }
#
#     return ns