# Chọn base image Python 3.10 nhẹ
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy tất cả file vào container
COPY . /app

# Cập nhật pip và cài requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port mà Render sẽ dùng
EXPOSE 10000

# Command chạy app bằng gunicorn
CMD ["gunicorn", "apptest:app", "--bind=0.0.0.0:10000"]