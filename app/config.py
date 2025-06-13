import os
from dotenv import load_dotenv
from functools import lru_cache


load_dotenv()

class Config:
    # SERVER_NAME = '172.20.0.3:8888'  # 注释掉这行，让Flask自动处理
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    API_BASE_URL = os.getenv('API_BASE_URL')
    API_KEY = os.getenv('API_KEY')
    API_PREFIX = os.getenv('API_PREFIX', '/api')
    API_USERCODE = os.getenv('API_USERCODE')
    API_PWD = os.getenv('API_PWD')
    # API_NAMESPACE = os.getenv('API_NAMESPACE', '/sjtu')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_booking_permission_mapping():
        """获取所有用户类型的预约权限映射"""
        return {
            'faculty': os.getenv('USER_TYPE_FACULTY') == 'Y',
            'student': os.getenv('USER_TYPE_STUDENT') == 'Y',
            'yxy': os.getenv('USER_TYPE_YXY') == 'Y',
            'fs': os.getenv('USER_TYPE_FS') == 'Y',
            'vip': os.getenv('USER_TYPE_VIP') == 'Y',
            'postphd': os.getenv('USER_TYPE_POSTPHD') == 'Y',
            'external_teacher': os.getenv('USER_TYPE_EXTERNAL_TEACHER') == 'Y',
            'summer': os.getenv('USER_TYPE_SUMMER') == 'Y',
            'team': os.getenv('USER_TYPE_TEAM') == 'Y',
            'alumni/schoolFellow': os.getenv('USER_TYPE_ALUMNI_SCHOOLFELLOW') == 'Y',
            'green': os.getenv('USER_TYPE_GREEN') == 'Y',
            'outside': os.getenv('USER_TYPE_OUTSIDE') == 'Y',
            'fszxsjs': os.getenv('USER_TYPE_FSZXSJS') == 'Y',
            'freshman': os.getenv('USER_TYPE_FRESHMAN') == 'Y',
            'fwzx': os.getenv('USER_TYPE_FWZX') == 'Y',
            'meeting': os.getenv('USER_TYPE_MEETING') == 'Y',
            'outsider': os.getenv('USER_TYPE_OUTSIDER') == 'Y',
            'studentother': os.getenv('USER_TYPE_STUDENTOTHER') == 'Y',
            'xmdl': os.getenv('USER_TYPE_XMDL') == 'Y',
        }

    @classmethod
    def can_book_seat(cls, user_type):
        """检查指定用户类型是否有预约权限"""
        mapping = cls.get_booking_permission_mapping()
        return mapping.get(user_type.lower(), False) and os.getenv('SEAT_BOOKING_ENABLED') == 'True'
