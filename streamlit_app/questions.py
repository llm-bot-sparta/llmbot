QUESTIONS = {
    "SQL": {
        "SQL_001": {
            "title": "배송 지연 고객 분석",
            "content": """
            예상 배송일보다 실제 배송을 늦게 받은 고객 중에서 가장 많은 주문을 한 고객의 ID와 총 주문 수를 조회하세요.
            - 결과 컬럼: customer_id, total_orders
            """,
            "model_answer": """
            SELECT 
                o.customer_id,
                COUNT(o.order_id) AS total_orders
            FROM orders o
            WHERE order_estimated_delivery_date < order_delivered_customer_date
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT 1;
            """,
            "evaluation_criteria": [
                {
                    "id": "C1",
                    "description": "WHERE 절의 조건 정확성",
                    "weight": 0.3,
                    "check_points": [
                        "order_estimated_delivery_date < order_delivered_customer_date 조건 포함",
                        "날짜 비교 연산자 사용 정확성"
                    ]
                },
                {
                    "id": "C2",
                    "description": "GROUP BY와 집계 함수 사용",
                    "weight": 0.3,
                    "check_points": [
                        "customer_id로 그룹화",
                        "COUNT 함수 사용"
                    ]
                },
                {
                    "id": "C3",
                    "description": "결과 정렬 및 제한",
                    "weight": 0.2,
                    "check_points": [
                        "ORDER BY DESC 사용",
                        "LIMIT 1 사용"
                    ]
                },
                {
                    "id": "C4",
                    "description": "쿼리 최적화",
                    "weight": 0.2,
                    "check_points": [
                        "불필요한 JOIN 없음",
                        "적절한 인덱스 사용 가능성"
                    ]
                }
            ]
        },
        "SQL_002": {
            "title": "결제 방식별 분석",
            "content": """
            payments 테이블에서 각 결제 방식(payment_type)별 결제 금액의 합계와 해당 결제 방식이 전체 결제 금액에서 차지하는 비율을 계산하세요.
            - 결과 컬럼: payment_type, total_payment_value, payment_percentage
            """,
            "model_answer": """
            SELECT 
                payment_type,
                SUM(payment_value) AS total_payment_value,
                ROUND(SUM(payment_value) * 100.0 / (SELECT SUM(payment_value) FROM payments), 2) AS payment_percentage
            FROM payments
            GROUP BY 1
            ORDER BY 2 DESC;
            """,
            "evaluation_criteria": [
                {
                    "id": "C1",
                    "description": "집계 함수 사용",
                    "weight": 0.3,
                    "check_points": [
                        "SUM 함수 사용",
                        "서브쿼리를 통한 전체 합계 계산"
                    ]
                },
                {
                    "id": "C2",
                    "description": "비율 계산 정확성",
                    "weight": 0.3,
                    "check_points": [
                        "비율 계산 로직 정확성",
                        "ROUND 함수 사용"
                    ]
                },
                {
                    "id": "C3",
                    "description": "GROUP BY 사용",
                    "weight": 0.2,
                    "check_points": [
                        "payment_type으로 그룹화",
                        "집계 함수와 GROUP BY 조합"
                    ]
                },
                {
                    "id": "C4",
                    "description": "결과 정렬",
                    "weight": 0.2,
                    "check_points": [
                        "ORDER BY DESC 사용",
                        "적절한 정렬 기준 선택"
                    ]
                }
            ]
        },
        "SQL_003": {
            "title": "배송된 주문 기준 통계",
            "content": """
            배송된(delivered) 주문을 기준으로 고유 고객 수, 총 주문 수, 총 결제 금액, 그리고 고객 1명당 평균 결제액을 계산하세요.\n- 결과 컬럼: cnt_users, cnt_orders, sum_payment, arppu
            """,
            "model_answer": """
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
            "evaluation_criteria": [
                {"id": "C1", "description": "JOIN 및 WHERE 조건 사용", "weight": 0.3, "check_points": ["INNER JOIN 사용", "order_status = 'delivered' 조건 포함"]},
                {"id": "C2", "description": "고유 고객 수, 주문 수, 결제 금액 집계", "weight": 0.3, "check_points": ["COUNT(DISTINCT o.customer_id) 사용", "COUNT(o.order_id) 사용", "SUM(p.payment_value) 사용"]},
                {"id": "C3", "description": "평균 결제액 계산", "weight": 0.2, "check_points": ["CASE WHEN 구문 사용", "고객 수 0명일 때 0 반환"]},
                {"id": "C4", "description": "결과 컬럼명 및 가독성", "weight": 0.2, "check_points": ["컬럼명 일치", "가독성 있는 쿼리"]}
            ]
        },
        "SQL_004": {
            "title": "결제수단별 이상 결제 탐지",
            "content": """
            동일한 결제수단(payment_type)에서 이루어진 다른 결제의 평균 금액보다 높은 결제들 중에서, 해당 결제가 해당 결제수단의 총 결제 금액 대비 20% 이상을 차지하는 주문을 조회하세요.\npayment_ratio는 결제 금액이 총 결제 금액에서 차지하는 비율을 소수점 둘째 자리까지 계산해주세요.\n- 결과 컬럼: order_id, payment_type, payment_value, payment_ratio
            """,
            "model_answer": """
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
            "evaluation_criteria": [
                {"id": "C1", "description": "WITH 및 JOIN 사용", "weight": 0.3, "check_points": ["WITH 구문 사용", "JOIN으로 결제수단별 집계 연결"]},
                {"id": "C2", "description": "평균 및 비율 계산", "weight": 0.3, "check_points": ["AVG, SUM 함수 사용", "ROUND 함수로 소수점 둘째 자리"]},
                {"id": "C3", "description": "조건문 정확성", "weight": 0.2, "check_points": ["평균보다 큰 결제만 필터", "20% 이상 비율 조건"]},
                {"id": "C4", "description": "결과 컬럼명 및 정렬", "weight": 0.2, "check_points": ["컬럼명 일치", "가독성 있는 쿼리"]}
            ]
        },
        "SQL_005": {
            "title": "월별 주문 건수 및 증감율",
            "content": """
            orders 테이블에서 월별(년-월) 주문 건수를 계산하되, **주문이 없는 달도 0건으로 포함**하고, 지난달 대비 주문 건수 증감율(growth_rate)을 계산하세요.\n결과는 년-월(month) 순서대로 정렬하며, 증감율은 소수점 둘째 자리까지 반올림 해주세요.\n- 결과 컬럼: month, cnt_orders, growth_rate
            """,
            "model_answer": """
            WITH RECURSIVE all_months AS (
                SELECT DATE_FORMAT(MIN(order_purchase_timestamp), '%Y-%m') AS months
                FROM orders
                UNION ALL
                SELECT DATE_FORMAT(DATE_ADD(CONCAT(months, '-01'), INTERVAL 1 MONTH), '%Y-%m')
                FROM all_months
                WHERE DATE_ADD(CONCAT(months, '-01'), INTERVAL 1 MONTH) <= (
                    SELECT DATE_FORMAT(MAX(order_purchase_timestamp), '%Y-%m-01') FROM orders
                )
            ),
            monthly_orders AS (
                SELECT 
                    m.months,
                    COALESCE(COUNT(o.order_id), 0) AS cur_orders
                FROM all_months m
                LEFT JOIN orders o ON DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') = m.months
                GROUP BY m.months
            )
            SELECT 
                months,
                cur_orders,
                prev_orders,
                ROUND(
                    CASE 
                        WHEN prev_orders IS NULL THEN NULL
                        WHEN prev_orders = 0 THEN cur_orders * 100
                        ELSE (cur_orders - prev_orders) / prev_orders * 100
                    END, 
                    2
                ) AS growth_rate
            FROM (
                SELECT 
                    months,
                    cur_orders,
                    LAG(cur_orders) OVER (ORDER BY months) AS prev_orders
                FROM monthly_orders
            ) sub
            ORDER BY 1;
            """,
            "evaluation_criteria": [
                {"id": "C1", "description": "재귀 CTE 및 LEFT JOIN 사용", "weight": 0.3, "check_points": ["WITH RECURSIVE 사용", "LEFT JOIN으로 월별 0건 포함"]},
                {"id": "C2", "description": "월별 집계 및 정렬", "weight": 0.3, "check_points": ["COUNT(o.order_id) 사용", "ORDER BY month"]},
                {"id": "C3", "description": "증감율 계산 로직", "weight": 0.2, "check_points": ["LAG 함수 사용", "CASE WHEN으로 0 또는 NULL 처리"]},
                {"id": "C4", "description": "결과 컬럼명 및 반올림", "weight": 0.2, "check_points": ["컬럼명 일치", "ROUND 함수로 소수점 둘째 자리"]}
            ]
        },
        "SQL_006": {
            "title": "결제 금액 이상치 탐지",
            "content": """
            각 결제 방식(payment_type)별 결제 금액의 평균 ± 3 표준편차(standard deviation)를 기준으로 이상치를 **`'Yes'/'No'`**로 탐지하세요. 결제 금액이 이 범위를 벗어나면 이상치로 간주합니다.\n결제 금액이 큰 순으로 정렬해주세요.\n- 결과 컬럼: order_id, payment_type, payment_value, is_outlier
            """,
            "model_answer": """
            SELECT
            	p.order_id,
            	p.payment_type,
            	p.payment_value,
            	CASE
            		WHEN p.payment_value < ps.avg_payment - 3 * ps.stddev_payment
            		OR p.payment_value > ps.avg_payment + 3 * ps.stddev_payment THEN 'Yes'
            		ELSE 'No'
            	END AS is_outlier
            FROM payments p
            JOIN (
            	SELECT
            		payment_type,
            		AVG(payment_value) AS avg_payment,
            		STDDEV(payment_value) AS stddev_payment
            	FROM payments
            	GROUP BY 1) AS ps 
            ON p.payment_type = ps.payment_type
            ORDER BY 3 desc;
            """,
            "evaluation_criteria": [
                {"id": "C1", "description": "평균 및 표준편차 계산", "weight": 0.3, "check_points": ["AVG, STDDEV 함수 사용", "GROUP BY payment_type"]},
                {"id": "C2", "description": "이상치 조건문 작성", "weight": 0.3, "check_points": ["평균 ± 3*표준편차 조건", "CASE WHEN 구문"]},
                {"id": "C3", "description": "결과 컬럼명 및 Yes/No 반환", "weight": 0.2, "check_points": ["is_outlier 컬럼명", "'Yes'/'No' 반환"]},
                {"id": "C4", "description": "정렬 및 가독성", "weight": 0.2, "check_points": ["ORDER BY payment_value DESC", "가독성 있는 쿼리"]}
            ]
        }
    },
    "Python기초": {}
} 