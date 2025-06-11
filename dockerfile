FROM txharbor.xaminim.com/minimax-pub/python3.12.5-ffmpeg7.1.1:v0.0.2

# 设置工作目录
WORKDIR /app

# 复制项目
COPY . .

# # 首先复制
# COPY pyproject.toml .
ENV UV_HTTP_TIMEOUT=240

# 安装依赖
RUN uv sync

# 运行项目
CMD ["uv", "run", "app/__init__.py"]
