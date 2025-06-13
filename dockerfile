FROM python:3.12.10-alpine3.22

# 设置工作目录
WORKDIR /app

# 复制项目
COPY . /app

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用端口
EXPOSE 8888

# 设置启动命令
CMD ["python", "app/__init__.py"]
