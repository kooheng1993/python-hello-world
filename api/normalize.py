import re
import json

def normalize_australian_mobile(phone_numbers):
    """
    标准化澳大利亚手机号码格式
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
    try:
        # 尝试解析 body
        body = json.loads(event.get('body', '{}'))
        phone_numbers = body.get('phone_numbers', [])

        # 验证输入
        if not phone_numbers:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': '未提供手机号码',
                    'message': '请在 phone_numbers 字段提供手机号码数组'
                })
            }

        # 标准化号码
        normalized_numbers = normalize_australian_mobile(phone_numbers)

        # 返回结果
        return {
            'statusCode': 200,
            'body': json.dumps({
                'normalized_numbers': normalized_numbers
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': '服务器内部错误',
                'message': str(e)
            })
        }

def main(request):
    """
    处理 HTTP 请求的主函数
    """
    if request.method == 'POST':
        try:
            body = request.get_json()
            phone_numbers = body.get('phone_numbers', [])

            # 验证输入
            if not phone_numbers:
                return json.dumps({
                    'error': '未提供手机号码',
                    'message': '请在 phone_numbers 字段提供手机号码数组'
                }), 400

            # 标准化号码
            normalized_numbers = normalize_australian_mobile(phone_numbers)

            return json.dumps({
                'normalized_numbers': normalized_numbers
            }), 200

        except Exception as e:
            return json.dumps({
                'error': '服务器内部错误',
                'message': str(e)
            }), 500
    
    return json.dumps({
        'message': '仅支持 POST 请求'
    }), 405
