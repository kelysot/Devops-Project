FROM python:3.9-slim
WORKDIR /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5555
CMD ["python3", "app.py"]