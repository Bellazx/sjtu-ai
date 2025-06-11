from flask import request, current_app
from flask_restx import Resource, Namespace
import requests
import json


def call_api(url, payload):
    """通用API调用函数"""
    try:
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"接口调用失败({url}): {str(e)}")
        return None


def call_basic_info(qry_str):
    payload = {
        "userCode": "dingzixuan",
        "userPwd": "F3F8828238A7F0DDD445FE58BAF94AB3",
        "qryType": 1,
        "qryStr": qry_str
    }

    # 调用第一个接口获取基本信息
    basic_info = call_api(
        "http://10.119.4.239/docaffiresinterface/getAlephSysID.ashx",
        payload
    )

    # 验证接口响应
    if not basic_info or basic_info.get('resStr') != '1':
        print("获取基本信息失败" + basic_info.get('msgStr'))
        return None

    # 在第一个接口结果中查找匹配用户
    target_user = next(
        (user for user in basic_info.get('retUser', [])
         if str(user.get('cardno')) == str(qry_str)),
        None
    )

    if not target_user:
        print(f"未找到卡号为 {qry_str} 的用户基本信息")
        return None
    return target_user

def call_gate_info(qry_str):
    payload = {
        "userCode": "dingzixuan",
        "userPwd": "F3F8828238A7F0DDD445FE58BAF94AB3",
        "qryType": 1,
        "qryStr": qry_str
    }

    # 调用第二个接口获取门禁信息
    gate_info = call_api(
        "http://10.119.4.239/docaffiresinterface/getGateInfo.ashx",
        payload
    )

    # 验证接口响应
    if not gate_info or gate_info.get('resStr') != '1':
        print("获取门禁信息失败" + gate_info.get('msgStr'))
        return None

    # 在门禁结果中查找匹配用户
    gate_user = next(
        (user for user in gate_info.get('retUser', [])
         if str(user.get('cardno')) == str(qry_str)),
        None
    )
    if not gate_user:
        print(f"未找到卡号为 {qry_str} 的用户门禁信息")
        return None
    return gate_user


def get_merged_user_info(qry_str):
    """获取并合并指定用户的完整信息"""
    target_user = call_basic_info(qry_str)
    gate_user = call_gate_info(qry_str)

    if gate_user:
        if target_user is None:
            target_user = {
                'userName': gate_user.get('username'),
                'cardid': gate_user.get('cardid'),
                'cardno': gate_user.get('cardno'),
                'userState': '未知'
            }
        target_user['isNormal'] = '正常' if gate_user.get('isNormal') == 1 else '异常'
        if target_user['userState'] != '未知':
            target_user['userState'] = '正常' if target_user.get('userState', '-1') == '0' else '异常'
        target_user['gateInfo'] = {  # 添加部分门禁信息
            'dept': gate_user.get('dept'),
            'usertype': gate_user.get('usertype'),
        }
    else:
        target_user['isNormal'] = '未知'
        print("门禁信息获取失败，仅返回基本信息")

    # 构造最终返回结构
    result = {
        'success': True,
        'message': '查询成功',
        'userInfo': target_user
    }

    return result

# def can_book_seat(qry_str):
#     """获取是否有预约座位权限"""
#     gate_user = call_gate_info(qry_str)
#     if gate_user:
#         return config.can_book_seat(gate_user.get('usertype'))
#     return False


def format_user_info(user_info):
    """格式化打印用户信息"""
    if not user_info or not user_info.get('success'):
        print("没有可用的用户信息")
        return

    user = user_info.get('userInfo', {})
    user_type = user.get('gateInfo', {}).get('usertype', '未知').lower()

    # 身份类型中文映射
    type_mapping = {
        'faculty': '教职工',
        'student': '学生',
        'yxy': '医学院教职工',
        'fs': '附属单位职工',
        'vip': 'VIP',
        'postphd': '博士后',
        'external_teacher': '外聘教师',
        'summer': '暑期生',
        'team': '集体账号',
        'alumni/schoolfellow': '校友',
        'green': '绿色通道',
        'outside': '校外人员',
        'fszxjs': '附属中学教师',
        'freshman': '新生',
        'fwxz': '访问学者',
        'meeting': '会议账号',
        'studentother': '非正规学生',
        'xmdl': '项目代理'
    }

    # 转换日期格式函数
    def format_date(original_date):
        if not original_date or len(original_date) != 8:
            return "未知"
        try:
            year = original_date[:4]
            month = original_date[4:6].lstrip('0')
            day = original_date[6:8].lstrip('0')
            return f"{year}年{month}月{day}日"
        except:
            return original_date  # 转换失败返回原值

    # 转换有效期
    expire_date = format_date(user.get('userExpireDate'))
    address_expire_date = format_date(user.get('addressExpireDate'))

    lines = [
        "\n【用户信息汇总】",
        f"查询状态: {user_info.get('message', '未知')}",
        "-" * 50,
        f"姓名: {user.get('userName', '未知')}",
        f"学工号: {user.get('cardno', '未知')}",
        f"系统ID: {user.get('sysId', '未知')}",
        f"物理卡号: {user.get('cardid', '未知')}",
        f"NFC ID: {user.get('nfcId', '未知')}",
        f"邮箱: {user.get('userEmail', '未知')}",
        f"电话: {user.get('userTel', '未知')}",
        "-" * 50,
        "【权限状态】",
        f"进馆权限: {user.get('isNormal')}",
        f"借阅权限: {user.get('userState')}",
        "-" * 50,
        "【身份信息】",
        f"部门: {user.get('gateInfo', {}).get('dept', '未知')}",
        f"读者身份有效期: {expire_date}",
        f"读者通讯有效期: {address_expire_date}",
        f"身份类型: {type_mapping.get(user_type, user_type)}",
        f"逾期费: {user.get('fee', '0')}元",
        "=" * 50
    ]
    print('\n'.join(lines))
    return '\n'.join(lines)


def init_user_api(api, models):
    ns = Namespace('/test', description='图书馆管理系统接口')

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

            user_info = get_merged_user_info(user_id)

            return format_user_info(user_info)
            #
            #
            # if user_id == "user_1234567890":
            #     return {
            #         "data": {
            #             "user_id": "user_1234567890",
            #             "user_name": "John Doe",
            #             "user_email": "john.doe@example.com",
            #             "user_phone": "+1234567890",
            #             "user_address": "123 Main St, Anytown, USA",
            #             "user_status": "expired",
            #             "permission": "体制内读者",
            #             "user_period_of_validity": "2024-01-01 12:00:00",
            #             "ALeph_wallet": -1.5
            #         },
            #         "status": "success"
            #     }
            # elif user_id == "user_1234567891":
            #     return {
            #         "data": {
            #             "user_id": "user_1234567891",
            #             "user_name": "harry",
            #             "user_email": "harry@example.com",
            #             "user_phone": "+1234567891",
            #             "user_address": "456 Main St, Anytown, USA",
            #             "user_status": "active",
            #             "permission": "体制内读者",
            #             "user_period_of_validity": "2026-01-01 12:00:00",
            #             "ALeph_wallet": -6.0
            #         },
            #         "status": "success"
            #     }
            # elif user_id == "user_1234567892":
            #     return {
            #         "data": {
            #             "user_id": "user_1234567892",
            #             "user_name": "Tom",
            #             "user_email": "tom@example.com",
            #             "user_phone": "+1234567892",
            #             "user_address": "789 Main St, Anytown, USA",
            #             "user_status": "active",
            #             "permission": "校友卡",
            #             "user_period_of_validity": "2026-01-01 12:00:00",
            #             "ALeph_wallet": 100.0
            #         },
            #         "status": "success"
            #     }
            # else:
            #     return {
            #         "data": {
            #             "user_id": "user_1234567893",
            #             "user_name": "Maggie",
            #             "user_email": "maggie@example.com",
            #             "user_phone": "+1234567892",
            #             "user_address": "789 Main St, Anytown, USA",
            #             "user_status": "active",
            #             "permission": "体制内读者",
            #             "user_period_of_validity": "2026-01-01 12:00:00",
            #             "ALeph_wallet": 100.0
            #         },
            #         "status": "success"
            #     }

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
                        }, {
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


if __name__ == '__main__':
    # 示例查询卡号
    query_cardno = "61396"  # 可以修改为需要查询的卡号

    # 获取用户信息
    merged_info = get_merged_user_info(query_cardno)

    # 打印结果
    if merged_info:
        format_user_info(merged_info)
