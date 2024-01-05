import asyncio
from datetime import datetime
import httpx
import logging
from logging.config import dictConfig
import pandas as pd
from pathlib import Path
import random
import string
import time
from typing import TypedDict


# 定义一个字典类型别名，包含用户名和密码的字典
class UserDictType(TypedDict):
    username: str
    password: str


# 定义一个列表类型别名，其中每个元素都是 UserDictType 类型的字典
UserListType = list[UserDictType]

# 定义常量
ascii_letters_and_digits = string.ascii_letters + string.digits
base_dir = Path(__file__).resolve().parent
log_path = base_dir / "pandora_next_tools.log"
log_level = logging.DEBUG
log_name: str = "pandora_next_tools"
log_persist: bool = False
# 配置log
dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s",
            },
            "generic": {
                "format": "[%(asctime)s] [%(process)d] [%(thread)d] %(message)s",
            },
            "simple": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "formatter": "generic",
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": log_path,
                "maxBytes": 1024 * 1024 * 10,  # 10M
                "backupCount": "5",
                "encoding": "utf-8",
            },
        },
        "loggers": {
            # "": {"level": "DEBUG", "handlers": ["console"]},
            log_name: {
                "level": log_level,
                "handlers": ["console", "file"] if log_persist else ["console"],
            },
        },
    }
)
logger = logging.getLogger(log_name)


def format_timestamp(timestamp: float, fmt="%Y-%m-%d %H:%M:%S") -> str:
    """
    接受一个时间戳作为参数并返回格式化后的日期时间字符串

    :param timestamp: float - 时间戳
    :param fmt: str - 格式
    :return: str: 格式化时间
    """

    # 将时间戳转换成datetime对象
    dt_object = datetime.fromtimestamp(timestamp)

    # 将datetime对象格式化成所需的字符串格式
    formatted_date = dt_object.strftime(format=fmt)

    return formatted_date


def trans_dict2str(cookies: dict) -> str:
    """
    将字典形式的 cookies 转换为字符串形式

    :param cookies: dict - 包含 cookies 键值对的字典
    :return: str - cookies 字符串
    """

    return "; ".join([f"{key}={value}" for key, value in cookies.items()])


def trans_dict2url_params(params: dict) -> str:
    """
    生成请求参数字符串

    :param params: dict - 包含用户名和密码的字典
    :return: str: 生成的登录参数字符串，格式为 "key1=value1&key2=value2&..."
    """

    return "&".join([f"{k}={v}" for _ in params for k, v in params.items()])


def get_login_params_batch(account_list: UserListType) -> list[str]:
    """
    批量生成登录参数字符串列表

    :param account_list: UserListType - 包含多个用户账户信息的列表
    :return: list[str] - 包含每个用户账户登录参数字符串的列表
    """

    res_list = []
    for account in account_list:
        res_list.append(trans_dict2url_params(account))

    return res_list


async def fetch(url: str, data: dict | str, headers: dict) -> dict | str:
    async with httpx.AsyncClient() as client:
        # 发起 POST 请求，指定 data 参数为要发送的数据字典和 headers 参数为自定义请求头
        res = await client.post(url, data=data, headers=headers)

        # 检查响应状态
        if res.status_code == 200:
            try:
                return res.json()
            except Exception as e:
                logger.error(e)
                return res.text

        # 处理重定向，向重定向位置发出 POST 请求
        if res.status_code == 301:
            logger.info("执行重定向...")
            res = await client.post(res.headers["Location"], data=data, headers=headers)
            if res.status_code == 200:
                try:
                    return res.json()
                except Exception as e:
                    logger.error(e)
                    return res.text
            else:
                logger.error(f"请求失败，状态码: {res.status_code}")
                logger.error(f"失败结果: {res.text}")
                return {}

        logger.error(f"请求失败，状态码: {res.status_code}")
        logger.error(f"失败结果: {res.text}")
        return {}


def get_access_token(
    url: str,
    account: UserDictType,
    cookies: str | dict | None = None,
    route: str = "/api/auth/login",
) -> dict:
    """
    获取 access token

    :param url: str - api 地址（包含 domain 和 proxy_prefix）
    :param account: UserDictType - 账号信息
    :param cookies: str | dict | None - cookies
    :param route: str - 路由
    :return: dict - access token
    """

    # 构建请求头
    headers = {}
    # 处理并在请求标头中添加 cookie
    if cookies is not None:
        if isinstance(cookies, str):
            headers["Cookie"] = cookies
        if isinstance(cookies, dict):
            headers["Cookie"] = trans_dict2str(cookies)

    res = asyncio.run(fetch(url=url + route, data=account, headers=headers))
    return res


def get_share_token(
    url: str,
    access_token: str,
    cookies: str | dict | None = None,
    route: str = "/api/token/register",
    site_limit: str = "",
    expires_in: float = 0,
    show_conversations: bool = False,
    show_userinfo: bool = False,
) -> dict:
    """
    获取 share token

    :param url: str - api 地址（包含 domain 和 proxy_prefix）
    :param access_token: str - ak
    :param cookies: str | dict | None - cookies
    :param route: str - 路由
    :param site_limit: str - 限制的网站
    :param expires_in: float - 过期时间
    :param show_conversations: bool - 是否会话隔离
    :param show_userinfo: bool - 是否显示用户信息
    :return: dict - share token
    """

    # 构建请求头
    headers = {}
    # 处理并在请求标头中添加 cookie
    if cookies is not None:
        if isinstance(cookies, str):
            headers["Cookie"] = cookies
        if isinstance(cookies, dict):
            headers["Cookie"] = trans_dict2str(cookies)

    # 为 "unique_name "生成随机字符串
    rand_str = "".join(random.choices(ascii_letters_and_digits, k=8))
    params = {
        "unique_name": rand_str,
        "access_token": access_token,
        "site_limit": site_limit,
        "expires_in": expires_in,
        "show_conversations": show_conversations,
        "show_userinfo": show_userinfo,
    }

    res = asyncio.run(fetch(url=url + route, data=params, headers=headers))
    return res


def get_pool_token(
    url: str,
    token_list: list[str],
    pool_token: str = "",
    cookies: str | dict | None = None,
    route: str = "/api/pool/update",
) -> dict:

    # 构建请求头
    headers = {}
    # 处理并在请求标头中添加 cookie
    if cookies is not None:
        if isinstance(cookies, str):
            headers["Cookie"] = cookies
        if isinstance(cookies, dict):
            headers["Cookie"] = trans_dict2str(cookies)

    # 获取登录参数列表
    sk_str = '\n'.join(token_list)
    data = f"share_tokens={sk_str}&&pool_token={pool_token}"

    res = asyncio.run(fetch(url=url + route, data=data, headers=headers))
    return res
