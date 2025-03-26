# 澳大利亚手机号码标准化工具

## 功能特点
- 支持多种澳大利亚手机号码格式
- Web 界面和 API 接口
- 一键转换为统一的 +614xxxxxx 格式

## 本地开发
1. 克隆仓库
2. 创建虚拟环境
3. 安装依赖
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 部署
### Vercel
1. Fork 仓库
2. 在 Vercel 中导入项目
3. 选择 Python 部署

### API 使用
POST `/api/normalize`
```json
{
    "phone_numbers": ["+6104123456", "0412345678"]
}
```

## 许可
MIT 许可证
