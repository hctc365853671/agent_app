FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# 声明streamlit端口（仅文档提示，不会自动开放端口）
EXPOSE 8501

# Streamlit启动命令，关闭自动打开浏览器，允许外部访问
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]