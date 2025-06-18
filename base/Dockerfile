FROM python:3.12-slim

WORKDIR /app

# 인증서 설치
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates && \
    pip install --upgrade certifi

# base 디렉토리 전체를 복사
COPY . .

# 의존성 설치
RUN pip install -r requirements.txt

# 포트 설정
EXPOSE 8080

# 실행 명령
CMD ["streamlit", "run", "streamlit_app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]