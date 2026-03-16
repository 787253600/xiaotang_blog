# ---- 基础镜像 ----
FROM python:3.12-slim AS base

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- 开发环境 ----
FROM base AS development

# 开发模式挂载源码，无需复制
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---- 生产环境 ----
FROM base AS production

COPY . .

# 创建非 root 用户
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
