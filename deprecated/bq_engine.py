from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import pandas as pd
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# BigQuery 연결 정보
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
DATASET_ID = os.getenv('BIGQUERY_DATASET_ID')
CREDENTIALS_PATH = os.getenv('LLM_CREDENTIALS')


# BigQuery URL 생성 (credentials_path를 URL에 포함)
DATABASE_URL = f"bigquery://{PROJECT_ID}/{DATASET_ID}?credentials_path={CREDENTIALS_PATH}"

# print(DATABASE_URL)
# 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

def get_db():
    """
    데이터베이스 세션을 생성하고 반환하는 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def execute_query(query: str, params: dict = None):
    """
    BigQuery 쿼리를 실행하는 함수
    
    Args:
        query (str): 실행할 SQL 쿼리
        params (dict, optional): 쿼리 파라미터
    
    Returns:
        list: 쿼리 결과
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        return [dict(zip(result.keys(), row)) for row in result]

# 사용 예시
if __name__ == "__main__":
    # 단일 쿼리 실행 예시
    result = execute_query(f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.customers` limit 10
    """)
    # display(pd.DataFrame(result))
