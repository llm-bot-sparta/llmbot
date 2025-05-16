# MySQL 연결 및 데이터 업로드

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MySQL 연결 정보
# Notion 혹은 임정에게 문의(bigquery - cloud sql로 연동)
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')  # 공개 IP 주소
MYSQL_PORT = os.getenv('MYSQL_PORT')  # 기본 TCP 포트
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')  # 데이터베이스 이름

# MySQL 연결
mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
# print(mysql_url)
mysql_engine = create_engine(mysql_url)

def setup_database():
    """
    데이터베이스 초기 설정 및 데이터 업로드를 수행하는 함수
    """
    # 테이블 생성 SQL
    # 기존 SQL 과제에 맞춘 형식이며 과제가 달라진다면 수정 필요
    # 외래키 설정하게 된다면 추후 테이블 삭제 옵션에서 외래키 설정을 off해야지 의존성 걸리지 않고 정상 삭제됨
    create_customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(32) PRIMARY KEY,
        customer_unique_id VARCHAR(32),
        customer_zip_code_prefix VARCHAR(5),
        customer_city VARCHAR(50),
        customer_state CHAR(2)
    )
    """

    create_orders_table = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id VARCHAR(32) PRIMARY KEY,
        customer_id VARCHAR(32),
        order_status VARCHAR(10),
        order_purchase_timestamp DATETIME,
        order_approved_at DATETIME,
        order_delivered_carrier_date DATETIME, 
        order_delivered_customer_date DATETIME,
        order_estimated_delivery_date DATETIME
    )
    """

    create_payments_table = """
    CREATE TABLE IF NOT EXISTS payments (
        order_id VARCHAR(32),
        payment_sequential INT,
        payment_type VARCHAR(20),
        payment_installments INT, 
        payment_value DECIMAL(10,2)
    )
    """

    try:
        # CSV 파일 읽기
        customers_df = pd.read_csv('answer/customers.csv')
        orders_df = pd.read_csv('answer/orders.csv')
        payments_df = pd.read_csv('answer/payments.csv')

        with mysql_engine.connect() as conn:
            # 테이블 삭제
            conn.execute(text("DROP TABLE IF EXISTS payments"))
            conn.execute(text("DROP TABLE IF EXISTS orders"))
            conn.execute(text("DROP TABLE IF EXISTS customers"))
                    
            # 테이블 생성
            conn.execute(text(create_customers_table))
            conn.execute(text(create_orders_table))
            conn.execute(text(create_payments_table))
            
            # 데이터 삽입
            customers_df.to_sql('customers', con=mysql_engine, if_exists='replace', index=False)
            orders_df.to_sql('orders', con=mysql_engine, if_exists='replace', index=False)
            payments_df.to_sql('payments', con=mysql_engine, if_exists='replace', index=False)
            
            conn.commit()

        print("데이터베이스 설정이 완료되었습니다.")
        return True
        
    except Exception as e:
        print(f"데이터베이스 설정 중 에러가 발생했습니다: {str(e)}")
        return False

def check_query_result(queries: list) -> None:
    """
    학생의 쿼리들을 실행하고 정답과 비교하는 함수
    
    Args:
        queries (list): 학생이 작성한 SQL 쿼리 리스트 (6개)
    """
    results = []
    
    for i, query in enumerate(queries, 1):
        try:
            # 쿼리가 비어있거나 None인 경우 처리
            if not query or query.strip() == "":
                print(f"문제 {i}의 쿼리가 비어있습니다.")
                results.append((i, False, None, None))
                continue
                
            # 학생 쿼리 실행
            with mysql_engine.connect() as conn:
                result_df = pd.read_sql_query(text(query), conn)
            
            # 정답 파일 읽기
            answer_file = os.path.join('answer', f'sql_q{i}.csv')
            if not os.path.exists(answer_file):
                print(f"정답 파일을 찾을 수 없습니다: {answer_file}")
                results.append((i, False, None, None))
                continue
                
            answer_df = pd.read_csv(answer_file)
            
            # 데이터프레임 비교
            result_sorted = result_df.sort_values(by=result_df.columns.tolist()).reset_index(drop=True)
            answer_sorted = answer_df.sort_values(by=answer_df.columns.tolist()).reset_index(drop=True)
            
            # 데이터 값 비교
            is_correct = result_sorted.equals(answer_sorted)
            results.append((i, is_correct, result_df, answer_df))
            
        except Exception as e:
            print(f"문제 {i} 실행 중 에러 발생: {str(e)}")
            results.append((i, False, None, None))
    
    # 결과 출력
    print("\n=== 채점 결과 ===")
    for i, is_correct, result_df, answer_df in results:
        print(f"문제{i}: {'O' if is_correct else 'X'}")
        
        if result_df is not None and answer_df is not None:
            print(f"\n문제{i} - 학생 쿼리 결과:")
            print(result_df)
            print(f"\n문제{i} - 정답:")
            print(answer_df)
            print("\n" + "="*50 + "\n")
