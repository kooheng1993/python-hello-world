import re

def normalize_australian_mobile(phone_numbers):
    """
    标准化澳大利亚手机号码格式
    
    Args:
        phone_numbers (list): 原始手机号码列表
    
    Returns:
        list: 标准化后的手机号码列表
    """
    def clean_number(number):
        # 移除所有非数字字符
        digits = re.sub(r'\D', '', str(number))
        
        # 处理不同前缀的情况
        if digits.startswith('614'):
            return f'+{digits}'
        elif digits.startswith('6104'):
            return f'+614{digits[4:]}'
        elif digits.startswith('04'):
            return f'+614{digits[2:]}'
        elif digits.startswith('4'):
            return f'+614{digits}'
        
        return number  # 如果无法识别，保持原样

    # 处理整个列表
    normalized_numbers = [clean_number(number) for number in phone_numbers]
    
    return normalized_numbers

def handler(event, context):
    """
    Vercel Serverless Function 入口点
    """
    from http import HTTPStatus
    import json

    # 处理 GET 请求
    if event['method'] == 'GET':
        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({
                'message': '澳大利亚手机号码标准化 API',
                'usage': '发送 POST 请求到 /api/normalize，携带 phone_numbers 数组'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # 处理 POST 请求
    if event['method'] == 'POST':
        try:
            # 解析请求体
            body = json.loads(event.get('body', '{}'))
            phone_numbers = body.get('phone_numbers', [])

            # 验证输入
            if not phone_numbers:
                return {
                    'statusCode': HTTPStatus.BAD_REQUEST,
                    'body': json.dumps({
                        'error': '未提供手机号码',
                        'message': '请在 phone_numbers 字段提供手机号码数组'
                    }),
                    'headers': {
                        'Content-Type': 'application/json'
                    }
                }

            # 标准化号码
            normalized_numbers = normalize_australian_mobile(phone_numbers)

            # 返回结果
            return {
                'statusCode': HTTPStatus.OK,
                'body': json.dumps({
                    'normalized_numbers': normalized_numbers
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        except Exception as e:
            return {
                'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
                'body': json.dumps({
                    'error': '服务器内部错误',
                    'message': str(e)
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

    # 处理其他方法
    return {
        'statusCode': HTTPStatus.METHOD_NOT_ALLOWED,
        'body': json.dumps({
            'error': '不支持的方法',
            'allowed_methods': ['GET', 'POST']
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
