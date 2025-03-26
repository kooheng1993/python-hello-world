import re
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/normalize', methods=['POST'])
def api_normalize():
    try:
        data = request.get_json()
        phone_numbers = data.get('phone_numbers', [])

        if not phone_numbers:
            return jsonify({
                'error': '未提供手机号码',
                'message': '请在 phone_numbers 字段提供手机号码数组'
            }), 400

        normalized_numbers = normalize_australian_mobile(phone_numbers)

        return jsonify({
            'normalized_numbers': normalized_numbers
        }), 200

    except Exception as e:
        return jsonify({
            'error': '服务器内部错误',
            'message': str(e)
        }), 500

def handler(event, context):
    return app(event, context)
