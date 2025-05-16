import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.bq_engine import execute_query
import json

class AnswerGenerator:
    def __init__(self):
        self.base_dir = 'answer'
        os.makedirs(self.base_dir, exist_ok=True)
        self.all_results = {}
        
    def save_sql_result(self, query: str, query_number: int):
        """
        SQL 쿼리 결과를 저장하는 함수
        
        Args:
            query (str): 실행할 SQL 쿼리
            query_number (int): 쿼리 번호
        """
        # 쿼리 실행 및 결과 가져오기
        result = execute_query(query)
        
        # 결과를 딕셔너리에 저장
        self.all_results[f"query_{query_number}"] = {
            "query": query,
            "result": result
        }
            
    def save_python_result(self, result: dict):
        """
        Python 코드 실행 결과를 저장하는 함수
        
        Args:
            result (dict): 저장할 결과 데이터
        """
        filepath = os.path.join(self.base_dir, 'python_result.txt')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
    def save_all_results(self):
        """
        모든 SQL 쿼리 결과를 하나의 JSON 파일로 저장하는 함수
        """
        filepath = os.path.join(self.base_dir, 'all_sql_results.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.all_results, f, indent=2, ensure_ascii=False)

def main():
    # AnswerGenerator 인스턴스 생성
    generator = AnswerGenerator()
    
    # SQL 쿼리 예시
    queries = {
        1: """
        SELECT 
            o.customer_id,
            COUNT(o.order_id) AS total_orders
        FROM orders o
        WHERE order_estimated_delivery_date < order_delivered_customer_date
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 1;
        """,
        2: """
        SELECT 
        payment_type,
        SUM(payment_value) AS total_payment_value,
        ROUND(SUM(payment_value) * 100.0 / (SELECT SUM(payment_value) FROM payments), 2) AS payment_percentage
        FROM payments
        GROUP BY 1
        ORDER BY 2 DESC;
        """,
        3: """
        SELECT 
        COUNT(DISTINCT o.customer_id) AS cnt_users,
        COUNT(o.order_id) AS cnt_orders,
        SUM(p.payment_value) AS sum_payment,
        CASE
            WHEN COUNT(DISTINCT o.customer_id) = 0 THEN 0
            ELSE SUM(p.payment_value) / COUNT(DISTINCT o.customer_id)
        END AS arppu 
        FROM orders o
        INNER JOIN payments p ON o.order_id = p.order_id
        WHERE o.order_status = 'delivered';
        """,
        4: """
        WITH payment_summary AS (
        SELECT 
            payment_type,
            AVG(payment_value) AS avg_payment_value,
            SUM(payment_value) AS total_payment_value
        FROM payments
        GROUP BY payment_type
        )
        SELECT 
            p.order_id,
            p.payment_type,
            p.payment_value,
            ROUND(p.payment_value / ps.total_payment_value * 100, 2) AS payment_ratio
        FROM payments p
        JOIN payment_summary ps ON p.payment_type = ps.payment_type
        WHERE p.payment_value > ps.avg_payment_value
        AND p.payment_value / ps.total_payment_value >= 0.2;
        """,
        # 5: """
        # WITH RECURSIVE all_months AS (
        # SELECT FORMAT_DATE('%Y-%m', MIN(order_purchase_timestamp)) AS months
        # FROM orders
        # UNION ALL
        # SELECT FORMAT_DATE('%Y-%m', DATE_ADD(PARSE_DATE('%Y-%m', months), INTERVAL 1 MONTH))
        # FROM all_months
        # WHERE DATE_ADD(PARSE_DATE('%Y-%m', months), INTERVAL 1 MONTH) <= (
        #     SELECT MAX(order_purchase_timestamp) FROM orders
        # )
        # ),
        # monthly_orders AS (
        #     SELECT 
        #         m.months,
        #         COALESCE(COUNT(o.order_id), 0) AS cur_orders
        #     FROM all_months m
        #     LEFT JOIN orders o ON FORMAT_DATE('%Y-%m', o.order_purchase_timestamp) = m.months
        #     GROUP BY m.months
        # )
        # SELECT 
        #     months,
        #     cur_orders,
        #     prev_orders,
        #     ROUND(
        #         CASE 
        #             WHEN prev_orders IS NULL THEN NULL
        #             WHEN prev_orders = 0 THEN cur_orders * 100
        #             ELSE (cur_orders - prev_orders) / prev_orders * 100
        #         END, 
        #         2
        #     ) AS growth_rate
        # FROM (
        #     SELECT 
        #         months,
        #         cur_orders,
        #         LAG(cur_orders) OVER (ORDER BY months) AS prev_orders
        #     FROM monthly_orders
        # ) sub
        # ORDER BY 1;
        # """,
        # 6: """
        # SELECT
        # p.order_id,
        # p.payment_type,
        # p.payment_value,
        # CASE
        #     WHEN p.payment_value < ps.avg_payment - 3 * ps.stddev_payment
        #     OR p.payment_value > ps.avg_payment + 3 * ps.stddev_payment THEN 'Yes'
        #     ELSE 'No'
        # END AS is_outlier
        # FROM payments p
        # JOIN (
        #     SELECT
        #         payment_type,
        #         AVG(payment_value) AS avg_payment,
        #         STDDEV(payment_value) AS stddev_payment
        #     FROM payments
        #     GROUP BY 1) AS ps 
        # ON p.payment_type = ps.payment_type
        # ORDER BY 3 desc;
        # """
    }
    
    # 모든 쿼리 실행 및 결과 저장
    for query_num, query in queries.items():
        print(f"Executing query {query_num}...")
        generator.save_sql_result(query, query_num)
        print(f"Query {query_num} completed.")
    
    # 모든 결과를 하나의 JSON 파일로 저장
    generator.save_all_results()
    print("All results have been saved to all_sql_results.json")
    
    # Python 결과 저장 예시
    python_result = {
        "task": "data_analysis",
        "result": {
            "mean": 10.5,
            "median": 9.8,
            "std": 2.3
        }
    }
    generator.save_python_result(python_result)

if __name__ == "__main__":
    main()
