from flask import request, current_app
from flask_restx import Resource, Namespace
from .api import call_api


def call_book_renew_api(book_id):
    payload = {
        "userCode": "dingzixuan",
        "userPwd": "F3F8828238A7F0DDD445FE58BAF94AB3",
        "qryType": 1,
        "qryStr": "|".join(str(n) for n in book_id) if len(book_id) > 1 else (str(book_id[0]) if book_id else "")

    }
    # 调用第二个接口获取门禁信息
    renew_info_res = call_api(
        "http://10.119.4.239/docaffiresinterface/getBookRenewStatus.ashx",
        payload
    )
    # 验证接口响应
    if not renew_info_res or renew_info_res.get('resStr') != '1':
        print("获取续借状态失败" + renew_info_res.get('msgStr'))
        return {
            'success': False,
            'message': "未获取到图书信息" + renew_info_res.get('msgStr')
        }
    renew_info = renew_info_res.get('retBookRenew')
    renew_res = []
    for item in renew_info:
        new_item = {
            'barcode': item['barcode'],
            'title': item['title'],
            'call_no': item['callno'],
            'sublibrary': item['sublibrary'],
            'collection_cod': item['collection'],
            'can_renew': (item['isExpired'] or item['isReserved'] or item['isTeachingGuide']) == 0,
        }
        new_item['renew_status'] = '可续借' if new_item['can_renew'] else '不可续借'

        renew_description = ''
        if item['isExpired'] != 0:
            renew_description += '书本已超期'
        if item['isReserved'] != 0:
            renew_description += '书本已被预约'
        if item['isTeachingGuide'] != 0:
            renew_description += '书本不可借阅'

        new_item['renew_description'] = renew_description
        renew_res.append(new_item)
    return {
        'success': True,
        "data": renew_res
    }


def init_book_api(api, models):
    ns = Namespace('/test', description='图书馆管理系统接口')

    @ns.route('/check_book_can_renew')
    class BookRenew(Resource):
        @ns.doc('check_book_can_renew')
        @ns.param('book_id', '图书条码', required=True)
        @ns.response(200, '成功', models['renew_check_response'])
        @ns.response(400, '错误', models['error_model'])
        def get(self):
            """检查图书是否可以续借,根据条码判断图书是否可以被续借"""
            book_id = request.args.get('book_id')
            if not book_id:
                return {
                    "message": "book_id is required",
                    "success": False
                }, 400

            return call_book_renew_api(book_id)
            # if book_id == "book_ztr":
            #     return {
            #         "data": {
            #             "can_renew": False
            #         },
            #         "status": "success"
            #     }
            # return {
            #     "data": {
            #         "can_renew": True
            #     },
            #     "status": "success"
            # }

    return ns


if __name__ == '__main__':
    import pprint
    book_id_list = [32086180,32003825]
    pprint.pprint(call_book_renew_api(book_id_list))
