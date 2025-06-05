# MySQL 연결 및 데이터 업로드

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import json
import numpy as np
from typing import List, Tuple, Optional, Union

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

def setup_database(answer_dir: str) -> bool:
    """
    데이터베이스 초기 설정 및 데이터 업로드를 수행하는 함수
    Args:
        answer_dir (str): 데이터 파일이 들어있는 디렉토리 경로 (루트 기준 상대경로)
    """
    # 프로젝트 루트 경로 계산
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    answer_path = os.path.join(project_root, answer_dir)
    csv_path = os.path.join(answer_path, 'BankChurners.csv')
    print(csv_path)
    # 테이블 생성 SQL
    create_credit_table= """
    CREATE TABLE BankChurners (
    CLIENTNUM BIGINT PRIMARY KEY,
    Attrition_Flag VARCHAR(30),
    Customer_Age TINYINT,
    Gender VARCHAR(10),
    Dependent_count TINYINT,
    Education_Level VARCHAR(30),
    Marital_Status VARCHAR(30),
    Income_Category VARCHAR(30),
    Card_Category VARCHAR(20),
    Months_on_book TINYINT,
    Total_Relationship_Count TINYINT,
    Months_Inactive_12_mon TINYINT,
    Contacts_Count_12_mon TINYINT,
    Credit_Limit DECIMAL(10, 2),
    Total_Revolving_Bal INT,
    Avg_Open_To_Buy DECIMAL(10, 2),
    Total_Amt_Chng_Q4_Q1 FLOAT,
    Total_Trans_Amt INT,
    Total_Trans_Ct INT,
    Total_Ct_Chng_Q4_Q1 FLOAT,
    Avg_Utilization_Ratio FLOAT
   )
    """

    try:
        # CSV 파일 읽기 (절대경로)
        credit_df = pd.read_csv(csv_path)

        with mysql_engine.connect() as conn:
            # 테이블 삭제
            conn.execute(text("DROP TABLE IF EXISTS BankChurners"))
                    
            # 테이블 생성
            conn.execute(text(create_credit_table))
            
            # 데이터 삽입
            credit_df.to_sql('BankChurners', con=mysql_engine, if_exists='replace', index=False)
            
            conn.commit()

        print("데이터베이스 설정이 완료되었습니다.")
        return True
        
    except Exception as e:
        print(os.getcwd())
        print(f"데이터베이스 설정 중 에러가 발생했습니다: {str(e)}")
        return False

def is_close(a: float, b: float, rtol: float = 1e-5, atol: float = 1e-8) -> bool:
    """
    두 숫자가 주어진 허용 오차 내에서 동일한지 확인하는 함수
    """
    return abs(a - b) <= (atol + rtol * abs(b))

def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[bool, str]:
    """
    두 DataFrame을 비교하여 결과와 상태를 반환하는 함수
    Returns:
        Tuple[bool, str]: (일치 여부, 상태 메시지)
        - 일치 여부: True(완전 일치), False(불일치)
        - 상태 메시지: 'exact_match', 'close_match', 'exact_match_colname_warning', 'close_match_colname_warning', 'mismatch'
    """
    # 컬럼명 소문자로 변환
    df1 = df1.copy()
    df2 = df2.copy()
    df1.columns = [c.lower() for c in df1.columns]
    df2.columns = [c.lower() for c in df2.columns]

    # 컬럼 개수와 순서가 다르면 mismatch
    if len(df1.columns) != len(df2.columns):
        return False, 'mismatch'

    # 컬럼명 기준이 아니라 순서대로 비교
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    # 행 개수가 다르면 mismatch
    if len(df1) != len(df2):
        return False, 'mismatch'

    # 컬럼명이 모두 같은지 확인 (공백, 대소문자 무시)
    colname_warning = [c.strip().lower() for c in df1.columns] != [c.strip().lower() for c in df2.columns]

    # 완전 일치 확인 (값만)
    if df1.values.tolist() == df2.values.tolist():
        if colname_warning:
            return True, 'exact_match_colname_warning'
        else:
            return True, 'exact_match'

    # 값이 거의 같은 경우 (순서대로)
    try:
        for col1, col2 in zip(df1.columns, df2.columns):
            s1 = df1[col1]
            s2 = df2[col2]
            if pd.api.types.is_numeric_dtype(s1) and pd.api.types.is_numeric_dtype(s2):
                if not np.allclose(s1, s2, rtol=1e-2, atol=1e-2):
                    return False, 'mismatch'
            elif not s1.equals(s2):
                return False, 'mismatch'
        if colname_warning:
            return False, 'close_match_colname_warning'
        else:
            return False, 'close_match'
    except:
        return False, 'mismatch'

def check_query_result(queries: list, answer_dir: str):
    """
    학생의 쿼리들을 실행하고 정답과 비교하는 함수
    Args:
        queries (list): 학생이 작성한 SQL 쿼리 리스트 (문제 순서와 동일)
        answer_dir (str): 정답 파일이 들어있는 디렉토리 경로 (루트 기준 상대경로)
    Returns:
        list: (question_id, is_correct, result_df, answer_df, status, error_message) 튜플의 리스트
    """
    # 프로젝트 루트 경로
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # answer_path: 항상 절대경로
    answer_path = os.path.join(project_root, answer_dir)
    # answer_map.json 불러오기
    with open(os.path.join(answer_path, 'answer_map.json'), 'r') as f:
        answer_map = json.load(f)
        
    question_ids = list(answer_map.keys())
    try:
        results = []
        for question_id, query in zip(question_ids, queries):
            if not query or query.strip() == "":
                results.append((question_id, False, None, None, 'empty', None))
                continue
            try:
                with mysql_engine.connect() as conn:
                    result_df = pd.read_sql_query(text(query), conn)
                answer_file = os.path.join(answer_path, answer_map[question_id])
                if not os.path.exists(answer_file):
                    results.append((question_id, False, None, None, 'no_answer', None))
                    continue
                answer_df = pd.read_csv(answer_file)
                is_correct, status = compare_dataframes(result_df, answer_df)
                results.append((question_id, is_correct, result_df, answer_df, status, None))
            except Exception as e:
                # 쿼리 실행 중 오류 발생 시
                results.append((question_id, False, None, None, 'error', str(e)))
        return results
    except Exception as e:
        # 전체 프로세스 오류 (예외적으로)
        return [(None, False, None, None, 'error', str(e))]

        
