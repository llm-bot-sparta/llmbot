FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "streamlit_app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]