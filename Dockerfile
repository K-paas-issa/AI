# 베이스 이미지
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# 요구 사항 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출 (다른 곳에서 접속 가능)
EXPOSE 8002

# 애플리케이션 실행
CMD ["uvicorn", "ai-server:app", "--host", "0.0.0.0", "--port", "8002"]