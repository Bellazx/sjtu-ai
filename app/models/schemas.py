from flask_restx import fields

def init_models(api):
    # 用户信息模型
    user_info_model = api.model('UserInfo', {
        'user_id': fields.String(description='用户唯一标识符'),
        'user_name': fields.String(description='用户姓名'),
        'user_email': fields.String(description='用户邮箱地址'),
        'user_phone': fields.String(description='用户电话号码'),
        'user_address': fields.String(description='用户地址'),
        'user_status': fields.String(description='用户状态'),
        'permission': fields.String(description='用户权限类型'),
        'user_period_of_validity': fields.DateTime(description='用户有效期'),
        'ALeph_wallet': fields.Float(description='用户钱包余额')
    })

    # 借阅信息模型
    borrow_info_model = api.model('BorrowInfo', {
        'book_id': fields.String(description='图书ID'),
        'book_name': fields.String(description='图书名称'),
        'borrow_time': fields.DateTime(description='借阅时间'),
        'borrow_end_time': fields.DateTime(description='应还时间'),
        'borrow_status': fields.String(description='借阅状态'),
        'borrow_user_id': fields.String(description='借阅用户ID')
    })

    # 预约信息模型
    reserve_info_model = api.model('ReserveInfo', {
        'room_id': fields.String(description='房间ID'),
        'room_name': fields.String(description='房间名称'),
        'reserve_time': fields.DateTime(description='预约时间'),
        'reserve_status': fields.String(description='预约状态'),
        'reserve_user_id': fields.String(description='预约用户ID'),
        'reserve_user_name': fields.String(description='预约用户名称'),
        'reserve_room_id': fields.String(description='预约房间ID'),
        'reserve_start_time': fields.DateTime(description='预约开始时间'),
        'reserve_end_time': fields.DateTime(description='预约结束时间')
    })

    # 借阅信息列表模型
    borrow_info_list = api.model('BorrowInfoList', {
        'borrow_info': fields.List(fields.Nested(borrow_info_model))
    })

    # 预约信息包装模型
    reserve_info_wrapper = api.model('ReserveInfoWrapper', {
        'reserve_info': fields.Nested(reserve_info_model)
    })

    # 续借检查响应模型
    renew_check = api.model('RenewCheck', {
        'can_renew': fields.Boolean(description='是否可以续借')
    })

    # 预约检查响应模型
    reserve_check = api.model('ReserveCheck', {
        'can_reserve_room': fields.Boolean(description='是否可以预约')
    })

    # 通用响应模型
    response_model = api.model('Response', {
        'data': fields.Raw(description='响应数据'),
        'status': fields.String(description='响应状态')
    })

    # 错误响应模型
    error_model = api.model('Error', {
        'error': fields.String(description='错误信息'),
        'status': fields.String(description='错误状态')
    })

    # 用户信息响应模型
    user_info_response = api.model('UserInfoResponse', {
        'data': fields.Nested(user_info_model),
        'status': fields.String(description='响应状态')
    })

    # 借阅信息响应模型
    borrow_info_response = api.model('BorrowInfoResponse', {
        'data': fields.Nested(borrow_info_list),
        'status': fields.String(description='响应状态')
    })

    # 预约信息响应模型
    reserve_info_response = api.model('ReserveInfoResponse', {
        'data': fields.Nested(reserve_info_wrapper),
        'status': fields.String(description='响应状态')
    })

    # 续借检查响应模型
    renew_check_response = api.model('RenewCheckResponse', {
        'data': fields.Nested(renew_check),
        'status': fields.String(description='响应状态')
    })

    # 预约检查响应模型
    reserve_check_response = api.model('ReserveCheckResponse', {
        'data': fields.Nested(reserve_check),
        'status': fields.String(description='响应状态')
    })

    return {
        'user_info_model': user_info_model,
        'borrow_info_model': borrow_info_model,
        'reserve_info_model': reserve_info_model,
        'response_model': response_model,
        'error_model': error_model,
        'user_info_response': user_info_response,
        'borrow_info_response': borrow_info_response,
        'reserve_info_response': reserve_info_response,
        'renew_check_response': renew_check_response,
        'reserve_check_response': reserve_check_response
    } 