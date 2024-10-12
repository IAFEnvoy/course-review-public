# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
# Flask-Mail 配置
    MAIL_SERVER = ''
    MAIL_PORT = 
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''  # 你的 Gmail 地址
    MAIL_PASSWORD = '' # 应用专用密码
    MAIL_DEFAULT_SENDER = ''  # 默认发件人

    BAIDU_APP_ID = ''
    BAIDU_API_KEY = ''
    BAIDU_SECRET_KEY = ''

    EMAIL_SUFFIX = '@shu.ehu.cn'

# Azure OpenAI Service 配置
    AZURE_OPENAI_API_KEY = ''  # 替换为你的 API Key
    AZURE_OPENAI_ENDPOINT = ''  # 替换为你的 Azure OpenAI 服务端点
    AZURE_OPENAI_API_TYPE = ''
    AZURE_OPENAI_API_VERSION = ''  # 使用合适的 API 版本
    AZURE_OPENAI_ENGINE = ''  # 替换为你在 Azure 上部署的模型名称

