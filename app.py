# app.py
import re
from flask import Flask, request, jsonify, render_template

def create_app():
    app = Flask(__name__)

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

    @app.route('/', methods=['GET', 'POST'])
    def index():
        result = None
        input_numbers = ''
        
        if request.method == 'POST':
            input_text = request.form.get('phone_numbers', '')
            input_numbers = input_text
            
            # 处理多行或逗号分隔的输入
            phone_list = [num.strip() for num in re.split(r'[,\n]', input_text) if num.strip()]
            
            result = normalize_australian_mobile(phone_list)
        
        return render_template('index.html', result=result, input_numbers=input_numbers)

    @app.route('/api/normalize', methods=['POST'])
    def api_normalize():
        data = request.json
        
        if not data or 'phone_numbers' not in data:
            return jsonify({"error": "No phone numbers provided"}), 400
        
        phone_numbers = data['phone_numbers']
        normalized = normalize_australian_mobile(phone_numbers)
        
        return jsonify({"normalized_numbers": normalized})

    return app

app = create_app()

# Vercel 部署需要
def handler(event, context):
    return app(event, context)
