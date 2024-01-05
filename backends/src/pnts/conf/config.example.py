from typing import (
    Union,
)

# ================================================= #
# ******************** SSH 配置 ******************** #
# ================================================= #
# 连接配置
SSH_HOSTNAME: str = "localhost"
SSH_PORT: int = 22
SSH_USERNAME: str = "root"
SSH_PASSWORD: str | None = None
SSH_KEY_FILE: str | None = "ed25519_key"
SSH_KEY_TYPE: str | None = "Ed25519"

# ================================================= #
# ******************** 默认配置 ******************** #
# ================================================= #
# 项目属性
DJANGO_PROJECT_NAME = 'pnts'
# 生产环境不要使用DEBUG
DEBUG = False
# 生产环境加密
SECRET_KEY = 'django-insecure-00000000000000000000000000000000000000000000000000'
# 只允许访问的ip地址列表
ALLOWED_HOSTS = ['*']
# 跨域允许cookies
CORS_ALLOW_CREDENTIALS = True
# 允许所有域名
CORS_ORIGIN_ALLOW_ALL = True
# 白名单
CORS_ORIGIN_WHITELIST = []
# 正则表达式白名单
CORS_ORIGIN_REGEX_WHITELIST = []
