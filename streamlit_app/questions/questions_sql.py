QUESTIONS = {
    "SQL_1": {
        "title": "(초심자~중급자) 고객 성별 비율 구하기",
        "content": """
            고객의 성별 비율을 구하세요.
            - 성별 비율은 소수점 둘째 자리까지 반올림
            - 결과 컬럼명: Gender, gender_percentage
            """,
        "model_answer": """
SELECT 
  Gender, 
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sparta.BankChurners), 2) AS gender_percentage
FROM sparta.BankChurners
GROUP BY Gender;
""",
        "evaluation_criteria": [
            {"id": "C1", "description": "Gender별 비율 산출(GROUP BY, ROUND)"},
            {"id": "C3", "description": "GROUP BY, COUNT, ROUND 등 요구 함수/절 사용"}
        ]
    },
    "SQL_2": {
        "title": "(초심자~중급자) 이탈 고객의 평균 신용한도 구하기",
        "content": """
            이탈 고객(Attrition_Flag = 'Attrited Customer')의 평균 Credit_Limit을 구하세요.
            - 소수점 둘째 자리까지 반올림
            - 결과 컬럼명: avg_credit_limit
            """,
        "model_answer": """
SELECT 
  ROUND(AVG(Credit_Limit), 2) AS avg_credit_limit
FROM sparta.BankChurners
WHERE Attrition_Flag = 'Attrited Customer';
""",
        "evaluation_criteria": [
            {"id": "C2", "description": "Attrition_Flag = 'Attrited Customer' 평균 Credit_Limit 산출(WHERE, AVG)"},
            {"id": "C3", "description": "WHERE, AVG 등 요구 함수/절 사용"}
        ]
    },
    "SQL_3": {
        "title": "(상급자) 카드 활동이 많은 고객군 분석",
        "content": """
            카드 활동이 많은 고객군을 정의하고, 그 특성을 분석해보세요.
            - 월별 거래량(Total_Trans_Ct / Months_on_book)을 기준으로 NTILE 또는 PERCENT_RANK를 사용하여 상위 10%인 고객군 선정
            - 이들의 평균 나이, 총 거래액(Total_Trans_Amt), 활동 개월 수(Months_on_book) 등 요약
            """,
        "model_answer": """
-- NTILE 사용
WITH activity_ranked AS (
  SELECT *,
         NTILE(10) OVER (ORDER BY Total_Trans_Ct * 1.0 / Months_on_book DESC) AS activity_rank
  FROM sparta.BankChurners
)
SELECT 
  ROUND(AVG(Customer_Age), 2) AS avg_age,
  ROUND(AVG(Total_Trans_Amt), 2) AS avg_trans_amt,
  ROUND(AVG(Months_on_book), 2) AS avg_months
FROM activity_ranked
WHERE activity_rank = 1;
""",
        "evaluation_criteria": [
            {"id": "C1", "description": "월별 거래량(Total_Trans_Ct / Months_on_book) 계산"},
            {"id": "C2", "description": "NTILE로 상위 10% 필터링"},
            {"id": "C3", "description": "평균 나이, 총 거래액, 활동 개월 수 요약"},
            {"id": "C4", "description": "CTE 또는 서브쿼리, 윈도우 함수 등 요구 문법 사용"}
        ]
    },
    "SQL_4": {
        "title": "(EASY LEVEL) 고객 나이와 거래액 기준 분석",
        "content": """
            고객 나이(Customer_Age)가 40세 이상이며 카드 거래액(Total_Trans_Amt)이 5000 이상인 고객 수는?
            """,
        "model_answer": """
SELECT COUNT(*) AS customer_count
FROM sparta.BankChurners
WHERE Customer_Age >= 40
  AND Total_Trans_Amt >= 5000;
""",
        "evaluation_criteria": [
            {"id": "C1", "description": "Customer_Age ≥ 40 AND Total_Trans_Amt ≥ 5000 조건 필터"},
            {"id": "C2", "description": "해당 고객 수 집계(WHERE, COUNT(*))"}
        ]
    },
    "SQL_5": {
        "title": "(MID LEVEL) 고객 유형별 신용한도 분석 (최고 평균)",
        "content": """
Attrition_Flag별로 평균 Credit_Limit을 계산하고, 그 중에서 가장 평균이 높은 고객 유형을 구하세요.
- GROUP BY, ORDER BY, LIMIT, ROUND 등 사용
""",
        "model_answer": """
SELECT Attrition_Flag, ROUND(AVG(Credit_Limit), 2) AS avg_credit_limit
FROM sparta.BankChurners
GROUP BY Attrition_Flag
ORDER BY avg_credit_limit DESC
LIMIT 1;
""",
        "evaluation_criteria": [
            {"id": "C1", "description": "Attrition_Flag별 AVG(Credit_Limit) 계산 및 최대값 선택"},
            {"id": "C2", "description": "GROUP BY, ORDER BY, LIMIT, ROUND 등 요구 문법 사용"}
        ]
    },
    "SQL_6": {
        "title": "(MID LEVEL) 평균 신용한도 초과 고객의 이탈 여부별 거래액/이용률 분석",
        "content": """
전체 평균보다 Credit_Limit이 높은 고객만 대상으로, 이탈 여부(Attrition_Flag)에 따라 평균 거래액(Total_Trans_Amt)과 평균 이용률(Avg_Utilization_Ratio)을 구하세요.
- CTE, WHERE, GROUP BY, ROUND 등 사용
""",
        "model_answer": """
WITH HighLimitCustomers AS (
    SELECT *
    FROM sparta.BankChurners
    WHERE Credit_Limit > (
        SELECT AVG(Credit_Limit)
        FROM sparta.BankChurners
        WHERE Credit_Limit IS NOT NULL
    )
)
SELECT 
    Attrition_Flag,
    ROUND(AVG(Total_Trans_Amt), 2) AS Avg_Trans_Amt,
    ROUND(AVG(Avg_Utilization_Ratio), 2) AS Avg_Utilization_Ratio
FROM HighLimitCustomers
GROUP BY Attrition_Flag;
""",
        "evaluation_criteria": [
            {"id": "C1", "description": "전체 평균보다 Credit_Limit이 높은 고객 필터"},
            {"id": "C2", "description": "이탈 여부별 AVG(Total_Trans_Amt), AVG(Avg_Utilization_Ratio) 비교"},
            {"id": "C3", "description": "CTE, GROUP BY, ROUND 등 요구 문법 사용"}
        ]
    },
    "SQL_7": {
        "title": "(HARD LEVEL) 연령대별 고객 충성도 분석",
        "content": """
고객 나이를 기준으로 다음과 같이 연령대를 나누세요:
- 20대 이하: '20s or less'
- 30대: '30s'
- 40대: '40s'
- 50대 이상: '50s or more'

이후 연령대별로 다음의 통계를 구하세요:
1. 고객 수
2. 이탈률 (전체 고객 중 Attrited Customer 비율, 소수점 3자리까지)
- 이탈률 = Attrited 수 / 전체 수 * 100

서브쿼리를 사용해 연령대를 구분하고 이탈률을 계산할 것
""",
        "model_answer": """
SELECT 
    Age_Group,
    COUNT(*) AS Total_Customers,
    ROUND(SUM(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 3) AS Attrition_Rate
FROM (
    SELECT *,
        CASE 
            WHEN Customer_Age < 30 THEN '20s or less'
            WHEN Customer_Age BETWEEN 30 AND 39 THEN '30s'
            WHEN Customer_Age BETWEEN 40 AND 49 THEN '40s'
            ELSE '50s or more'
        END AS Age_Group
    FROM sparta.BankChurners
) AS grouped
GROUP BY Age_Group
ORDER BY Age_Group;
""",
        "evaluation_criteria": [
            {"id": "C1", "description": "Customer_Age 기반 연령대 구분(CASE, 서브쿼리/CTE)"},
            {"id": "C2", "description": "연령대별 고객 수 및 이탈률 산출(GROUP BY, COUNT, ROUND)"},
            {"id": "C3", "description": "이탈률 계산식(Attrited 수 / 전체 수 * 100) 적용"}
        ]
    }
} 