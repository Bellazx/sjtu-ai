import requests

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
        return "接口数据查询失败"
