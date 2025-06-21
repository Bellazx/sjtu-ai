from flask import request, current_app
from flask_restx import Resource, Namespace
from .api import call_api
import json

def call_encrypt_api(qry_str, qry_type):
    print(f"当前API_KEY配置值: {current_app.config['API_KEY']}")
    """调用加解密接口,以获取登录URL"""
    payload = {
        "userCode": current_app.config["API_USERCODE"],
        "userPwd": current_app.config["API_PWD"],
        "qryType": qry_type,
        "qryKey": current_app.config["API_KEY"],
        "qryStr": qry_str
    }
    print(payload)
    # 调用加解密接口
    encrypt_res = call_api(
        current_app.config["API_URL"] + "/getEncryptCode.ashx",
        payload
    )
    print(encrypt_res)
    
    # 验证接口响应
    if not encrypt_res or encrypt_res.get('resStr') != '1':
        print("加解密失败: " + str(encrypt_res.get('msgStr', '未知错误')))
        return {
            'success': False,
            'message': "加解密失败: " + str(encrypt_res.get('msgStr', '未知错误'))
        }
    
    # 解析返回结果，提取encodeStr字段
    encrypt_data = {
        'user_code': encrypt_res.get('userCode'),
        'qry_key': encrypt_res.get('qryKey'),  
        'qry_str': encrypt_res.get('qryStr'),
        'encode_str': encrypt_res.get('encodeStr')  # 重点解析的字段
    }
    
    return {
        'success': True,
        'data': encrypt_data['encode_str'],
        'message': encrypt_res.get('msgStr', '加解密成功')
    }

def init_login_api(api, models):
    """初始化登录相关API"""
    ns = Namespace('/auth', description='认证加解密接口')

    @ns.route('/encrypt')
    class EncryptCode(Resource):
        @ns.doc('encrypt_code')
        @ns.param('qry_str', '待加解密字符串', required=True, type=str)
        @ns.param('qry_type', '加解密类型', required=True, type=int)
        @ns.response(200, '成功', models['response_model'])
        @ns.response(400, '错误', models['error_model'])
        def get(self):
            """字符串加解密接口,用于对指定字符串进行加解密处理"""
            try:
                qry_str = request.args.get('qryStr')
                qry_type = request.args.get('qryType')
                
                # 参数验证
                if not qry_str:
                    return {
                        "message": "qry_str is required",
                        "success": False
                    }, 400
                if not qry_type:
                    return {
                        "message": "qry_type is required",
                    "success": False
                }, 400
                return call_encrypt_api(qry_str, qry_type)
                
            except json.JSONDecodeError:
                return {
                    "message": "Invalid JSON format",
                    "success": False
                }, 400
            except Exception as e:
                return {
                    "message": f"Internal server error: {str(e)}",
                    "success": False
                }, 500

    return ns