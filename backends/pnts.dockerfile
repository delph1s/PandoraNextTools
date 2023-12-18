### 第一阶段：构建
FROM python:3.10.13 AS builder

# 设置工作目录
WORKDIR /source/

## 设置环境变量
ARG PIP_SOURCE=https://pypi.tuna.tsinghua.edu.cn/simple/
    # 超时时间
ENV PIP_DEFAULT_TIMEOUT=100 \
    # Python 解释器不生成字节码 pyc 文件
    PYTHONDONTWRITEBYTECODE=1 \
    # 允许立即显示语句和日志信息
    PYTHONUNBUFFERED=1 \
    # 禁用 pip 版本检查以减少运行时间和日志垃圾邮件
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # 缓存在 docker 镜像中毫无用处，因此禁用缓存以减小镜像大小
    PIP_NO_CACHE_DIR=1 \
    # 使用国内源加速 Python 包安装
    PIP_INDEX_URL=$PIP_SOURCE

# 复制 apt 仓库信息
#COPY ./src/docker/sources.list /etc/apt/sources.list
# 拷贝项目信息
COPY ./src/requirements.txt /source
# 安装必要包
RUN --mount=type=cache,target=/root/.cache/pip \
    # pip install -U pip setuptools && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /source/wheels -r requirements.txt

### 第二阶段：运行
FROM python:3.10.13-slim

# 镜像信息
ARG VERSION="2023.0.0"
ARG BUILD_DATE="2023-12-27"
LABEL build_version="delph1s.com version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="delph1s <admin@delph1s.com>"

# 设置工作目录
WORKDIR /app

## 配置参数
    # 应用用户组
ENV APP_USER_GROUP=pnts \
    # 应用用户
    APP_USER=pnts \
    # 应用路径
    APP_SOURCE_DIR=pnts

# 复制执行文件
COPY ./src/docker/docker-entrypoint.sh /

    # 移除\r in windows
RUN sed -i 's/\r//' /docker-entrypoint.sh && \
    # 赋予 docker-entrypoint.sh 执行权限
    chmod +x /docker-entrypoint.sh && \
    # 创建非 root 用户和用户组
    addgroup --system --gid 1000 $APP_USER_GROUP && \
    adduser --system --shell /bin/false --no-create-home --uid 1000 --ingroup $APP_USER_GROUP --disabled-password $APP_USER && \
    chown -R $APP_USER:$APP_USER_GROUP /app && \
    chown $APP_USER:$APP_USER_GROUP /docker-entrypoint.sh

## 复制从 builder 阶段安装的包
# 复制安装的包
COPY --from=builder /source/wheels /wheels
# 复制包的二进制文件
COPY --from=builder /source/requirements.txt .

    # 安装包
RUN pip install --no-cache /wheels/*

# 复制应用代码
COPY --chown=$APP_USER:$APP_USER_GROUP ./src/$APP_SOURCE_DIR /app

# 切换到
USER $APP_USER

ENV PYTHONPATH=$PYTHONPATH:/app

EXPOSE 8888

# 执行
ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]
