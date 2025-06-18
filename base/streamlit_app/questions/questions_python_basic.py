QUESTIONS = {
    "PYTHON_1": {
        "title": "숫자 리스트의 평균 계산하기",
        "content": """
- **배경**: 한 소매점에서 재고를 계산해야 합니다. 주어진 재고의 평균을 계산해보세요.
- **문제 의도**
    - 리스트의 자료형을 이해
    - 내장 함수의 활용
- **요구 사항**
    - 함수명: `calculate_stock`
    - 해당 함수는 리스트의 전달 인자를 받음
""",
        "model_answer": """
def calculate_stock(numbers):
    return sum(numbers) / len(numbers)
""",
        "function_name": "calculate_stock",
        "test_cases": [
            {"input": [10, 20, 30, 40, 50], "expected": 30.0},
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "리스트의 합과 길이를 이용해 평균을 계산한다."},
            {"id": "P2", "description": "내장 함수(sum, len) 사용"}
        ]
    },
    "PYTHON_2": {
        "title": "간단한 사칙연산 계산기 함수 만들기",
        "content": """
        - **배경**: 컴퓨터 과학 수업에서 학생들은 기본적인 프로그래밍 원리를 익히고, 실제 생활에 적용할 수 있는 간단한 프로그램을 만드는 연습을 합니다. 이를 간단한 형태로 변환하여 함수형으로 만들어 보겠습니다.
        - **문제 의도**
            - 전달 인자의 입력에 대한 이해
            - 조건문에 대한 이해
        - **요구 사항**
            - 함수명: `simple_calculator`
            - `num1`, `num2` : 숫자 입력 값
            - `operator` : 문자열 형태의 사칙 연산자 (+, -, *, /)
            - 나누려는 숫자 `num2`가 0인 경우 다음 문자를 반환: "**Cannot divide by zero**"
        """,
        "model_answer": """
        def simple_calculator(num1, num2, operator):
            if operator == '+':
                return num1 + num2
            elif operator == '-':
                return num1 - num2
            elif operator == '*':
                return num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return 'Cannot divide by zero'
                else:
                    return num1 / num2
            else:
                return 'Invalid operator'
""",
        "function_name": "simple_calculator",
        # "unpack_args": True을 통해 전달인자를 여러개를 넣을 수 있는 로직 구현
        "test_cases": [
            {"input": [10, 5, "+"], "expected": 15, "unpack_args": True},
            {"input": [10, 5, "-"], "expected": 5,  "unpack_args": True},
            {"input": [10, 5, "*"], "expected": 50, "unpack_args": True},
            {"input": [10, 0, "/"], "expected": "Cannot divide by zero", "unpack_args": True}
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "전달 인자(num1, num2, operator)를 올바르게 사용한다."},
            {"id": "P2", "description": "조건문(if/elif/else)으로 연산을 분기한다."},
            {"id": "P3", "description": "0으로 나눌 때 'Cannot divide by zero'를 반환한다."}
        ]
    },
    "PYTHON_3": {
        "title": "가장 많은 제품 찾기",
        "content": """
    - **배경**: 한 소매점에서 가장 많은 제품을 가지고 있는 상품을 찾아야 합니다. 딕셔너리 형태로 저장된 재고 현황을 전달하면 가장 많이 있는 상품과 해당 상품의 수량을 반환하세요.
    - **문제 의도**
        - 딕셔너리 자료형의 이해
        - 딕셔너리 자료형과 내장 함수의 조합 혹은 **최대 값 찾기** 알고리즘 구현
    - **요구 사항**
        - 함수명: `find_top_seller`
        - 해당 함수는 딕셔너리의 전달 인자를 받음
    """,
        "model_answer": """
def find_top_seller(data):
    top_product = ""
    max_sales = -1
    for product, sales in data.items():
        if sales > max_sales:
            max_sales = sales
            top_product = product
    return top_product, max_sales
""",
        "function_name": "find_top_seller",
        "test_cases": [
            {"input": {"apple": 50, "orange": 2, "banana": 30}, "expected": ("apple", 50)},
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "딕셔너리의 key, value를 올바르게 순회한다."},
            {"id": "P2", "description": "최대값을 찾는 알고리즘 또는 내장함수(max 등)를 활용한다."},
            {"id": "P3", "description": "가장 많은 상품명과 수량을 튜플로 반환한다."}
        ]
    },
    "PYTHON_4": {
        "title": "중복 문자 제거 및 빈도수 계산",
        "content": """
- **배경**: 당신은 대규모 텍스트 데이터를 분석하는 프로젝트를 진행하고 있습니다. 텍스트 데이터에서 특정 패턴을 찾아내는 작업을 수행해야 합니다. 이번 작업에서는 중복된 문자를 제거하고 각 문자가 한 번씩만 나타나게 하는 프로그램을 작성하는 것이 목표입니다. 하지만 각 문자는 처음 등장한 순서를 유지해야 하며, 추가적으로 각 문자가 등장하는 빈도를 함께 계산해야 합니다.
- **문제 의도**
    - 딕셔너리의 자료형의 이해
    - 중첩된 자료형에 대한 이해
- **요구 사항**
    - 함수명: `remove_duplicates_and_count`
    - 해당 함수는 문자열의 답을 받음
    - 주어진 문자열에서 중복된 문자를 제거
    - 각 문자가 처음 등장한 순서를 유지
    - 각 문자가 등장하는 빈도를 함께 출력하며 결과는 (문자, 빈도수) 형태의 튜플로 반환
""",
        "model_answer": """
def remove_duplicates_and_count(s):
    frequency = {}
    for char in s:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return list(frequency.items())
""",
        "function_name": "remove_duplicates_and_count",
        "test_cases": [
            {"input": "abracadabra123321", "expected": [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1), ('1', 2), ('2', 2), ('3', 2)]}
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "딕셔너리를 사용해 각 문자의 빈도수를 계산한다."},
            {"id": "P2", "description": "중복 문자를 제거하고, 처음 등장한 순서를 유지한다."},
            {"id": "P3", "description": "결과를 (문자, 빈도수) 형태의 튜플 리스트로 반환한다."}
        ]
    },
    "PYTHON_5": {
        "title": "이동 거리 구하기",
        "content": """
- **배경**: 축구 경기 데이터 분석가로서, 선수들의 위치 데이터를 활용하여 그들의 활동 범위와 이동 효율성을 계산하고자 합니다. 선수들의 이동 패턴을 분석하고 이를 통해 그들의 총 누적 이동 거리를 계산하여 선수의 활동량을 평가해보겠습니다.
- **문제 의도**
    - 수학적 공식을 파이썬으로 구현
    - 튜플 자료형의 이해
    - 중첩된 자료형에 대한 이해
- **요구 사항**
    - 함수명: `calculate_total_distances`
    - 유클리드 거리 공식을 사용하여 각 위치 간 이동 거리를 계산
        - 유클리드 거리 공식  
          $d = \\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$
    - 각 선수별로 경기 동안 이동 총 누적거리를 반환
    - (선수 이름, 누적 거리) 형태의 튜플로 리스트에 담아 반환. 누적 거리는 소수점 2째 자리까지 반올림
""",
        "model_answer": """
def calculate_total_distances(player_positions):
    records = []
    for player, positions in player_positions.items():
        total_distance = 0.0
        for i in range(0, len(positions)-1):
            x1, y1 = positions[i]
            x2, y2 = positions[i+1]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            total_distance += distance
        records.append((player, round(total_distance, 2)))
    return records
""",
        "function_name": "calculate_total_distances",
        "test_cases": [
            {
                "input": {
                    "John Doe": [(0, 0), (1, 1), (2, 2), (5, 5)],
                    "Jane Smith": [(2, 2), (3, 8), (6, 8)],
                    "Mike Brown": [(0, 0), (3, 4), (6, 8)]
                },
                "expected": [
                    ("John Doe", 7.07),
                    ("Jane Smith", 9.08),
                    ("Mike Brown", 10.0)
                ]
            }
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "유클리드 거리 공식을 올바르게 구현한다."},
            {"id": "P2", "description": "각 선수별로 누적 이동 거리를 계산한다."},
            {"id": "P3", "description": "결과를 (선수 이름, 누적 거리) 튜플의 리스트로 반환한다."},
            {"id": "P4", "description": "누적 거리를 소수점 2째 자리까지 반올림한다."}
        ]
    },
    "PYTHON_6": {
        "title": "Github에 있는 데이터 불러오기",
        "content": """
        - **배경**: Pandas의 read_csv 함수는 로컬에 저장된 자료 이외에도 인터넷에 있는 자료를 바로 불러올 수 있는 기능을 지원합니다. 또한 구분자가 쉼표(,)가 아니더라도 받아올 수 있습니다.
        - **문제 의도**
            - pandas의 read_csv 함수의 이해
            - 'sep' 전달 인자의 이해
        - **요구 사항**
            - 함수명: `get_csv`
            - 다음 Github 에 대한 데이터를 pd.read_csv를 이용하여 데이터를 불러오세요
            - Hint) url은 다음과 같습니다.
            - [`https://raw.githubusercontent.com/llm-bot-sparta/sparta_coding/refs/heads/main/flight_data.csv`](https://raw.githubusercontent.com/llm-bot-sparta/sparta_coding/refs/heads/main/flight_data.csv)
        """,
        "model_answer": """
        import pandas as pd
        def get_csv(url):
            df = pd.read_csv(filepath_or_buffer=url, sep=';')
            return df
        """,
        "function_name": "get_csv",
        "test_cases": [
        {
            "input": "df_sample",
            "expected_type": "DataFrame",   # 1차: 타입이 DataFrame인지 검증
            "expected_shape": [10683, 11] # 2차: 형태(shape)가 맞는지 검증
        }
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "pd.read_csv로 인터넷 상의 csv 파일을 불러온다."},
            {"id": "P2", "description": "sep 인자를 올바르게 사용한다."}
        ]
        },
    "PYTHON_7": {
        "title": "결측치 확인",
        "content": """
        - **배경:** 데이터를 불러 왔을 때 각 컬럼에 결측치 유무를 확인하는 것은 중요합니다. 컬럼의 결측치를 확인해보세요.
        - **문제 의도**
            - DataFrame의 함수를 활용
        - **요구 사항**
            - 함수명: `get_missing`
            - 컬럼별 결측치 수를 예시 결과와 같이 출력
        """,
                "model_answer": """
        def get_missing(df):
            return df.isnull().sum()
        """,
        "function_name": "get_missing",
        "test_cases": [ {"input": "df_sample",
           "expected_type": 'Series',
           "expected": {  
                "Route": 1,
                "Total_Stops": 1,
                "Airline": 0, "Date_of_Journey": 0, "Source": 0, 
                "Destination": 0, "Dep_Time": 0, "Arrival_Time": 0,
                "Duration": 0, "Additional_Info": 0, "Price": 0
            }}
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "DataFrame의 isnull().sum()을 활용한다."}
        ]
    },
    "PYTHON_8": {
        "title": "조건에 맞는 데이터 출력하기",
        "content": """
- **배경:** Destination 기준으로 price에 대한 평균과 중앙 값을 동시에 구해주세요. 단, 값은 소수점 첫 번째 자리까지 표현해주세요.
- **문제 의도**
    - DataFrame의 집계 함수를 사용
- **요구 사항**
    - 함수명: `get_price`
    - Destination 을 인덱스로, 평균과 중앙값을 컬럼으로하는 데이터프레임 반환
    - 소수점 첫 번째 짜리까지 반올림
    - 정렬은 필수사항 아님
""",
        "model_answer": """
def get_price(df):
    result = df.groupby('Destination')['Price'].agg(['mean', 'median']).round(1)
    return result
""",
        "function_name": "get_price",
        "test_cases": [
            {"input": "df_sample", "expected_type": "DataFrame",
            "expected": {
                "mean": {
                    "Banglore": 9158.4,
                    "Cochin": 10539.4,
                    "Delhi": 5143.9,
                    "Hyderabad": 5059.7,
                    "Kolkata": 4789.9,
                    "New Delhi": 11917.7
                },
                "median": {
                    "Banglore": 9345.0,
                    "Cochin": 10262.0,
                    "Delhi": 4823.0,
                    "Hyderabad": 3342.0,
                    "Kolkata": 3850.0,
                    "New Delhi": 10898.5
                }
            }
            }
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "groupby, agg, round를 활용해 집계한다."},
            {"id": "P2", "description": "Destination을 인덱스로, 평균과 중앙값을 컬럼으로 반환한다."}
        ]
    },
    "PYTHON_9": {
        "title": "수요일에 예약된 비행기 표 값 평균 구하기",
        "content": """
    - **배경:** 특정한 날짜(Ex 수요일) 에 대한 평균 예약 금액을 조회하겠습니다.
    - **문제 의도**
        - 날짜형 자료형 이해
        - 불리언 인덱싱 활용
        - Hint
            1. 기존 날짜형 자료형을 바꿀 함수 찾기
            2. [**Series의 dt**](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html)의 함수 알아보기
        - 문제의 푸는 방법은 단 1개가 아니며 여러가지가 나올 수 있음
    - **요구 사항**
        - 함수명: `get_wed_price`
        - 결과 값은 소수 값 1개가 나와야합니다.
        - 소수점 첫 번째 짜리까지 반올림
    """,
            "model_answer": """
    def get_wed_price(df):
        df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], format = '%d/%m/%Y')
        df['Day_of_Week'] = df['Date_of_Journey'].dt.day_name()
        wednesday_avg_price = df[df['Day_of_Week'] == 'Wednesday']['Price'].mean()
        return wednesday_avg_price.round(1)
    """,
        "function_name": "get_wed_price",
        "test_cases": [
            {"input": "df_sample", "expected_type": "float64", 'expected' :9277.5}
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "날짜형 변환 및 요일 추출을 올바르게 한다."},
            {"id": "P2", "description": "수요일만 필터링하여 평균을 구한다."},
            {"id": "P3", "description": "결과를 소수점 첫째자리까지 반올림한다."}
        ]
    },
    "PYTHON_10": {
        "title": "출발 시간 기준 비행기 수 집계하기",
        "content": """
- **배경:** 출발 시간마차 비행기 출발의 편차가 있는지 확인해보려합니다. 요구사항에 맞춰 아침,밤,오후,저녁으로 분류하여 수를 세보세요.
- **문제 의도**
    - 날짜형 자료형의 이해
    - .apply  함수를 통한 기존 자료 재정의
    - lambda 혹은 함수를 DataFrame에 적용하기
- **요구 사항**
    - 함수명: `get_cat`
    - Dep_Time 컬럼 기준 아침(5시 이상 12시 미만), 오후(12시 이상 18시 미만), 저녁(18시 이상 24시 미만), 그 외시간 밤
    - Airline 수 기준으로 내림차순 정렬 해주세요.
    - 최종 결과물은 예시 결과와 같이 `reset_index()` 를 적용해주세요.
""",
        "model_answer": """
def get_cat(df):
    df['Dep_Time'] = pd.to_datetime(df['Dep_Time'], format='%H:%M')
    df['Time_Of_Day'] = df['Dep_Time'].apply(
        lambda x: '아침' if 5 <= x.hour < 12 else
                  '오후' if 12 <= x.hour < 18 else
                  '저녁' if 18 <= x.hour < 24 else
                  '밤'
    )
    return df.groupby(['Time_Of_Day'])[['Airline']].count().sort_values(by='Airline', ascending= False).reset_index()
""",
        "function_name": "get_cat",
        "test_cases": [
            {"input": "df_sample", "expected_type": "DataFrame",
             "expected": [
                {"Time_Of_Day": "아침", "Airline": 4912},
                {"Time_Of_Day": "저녁", "Airline": 2702},
                {"Time_Of_Day": "오후", "Airline": 2604},
                {"Time_Of_Day": "밤", "Airline": 465}
            ]}
        ],
        "evaluation_criteria": [
            {"id": "P1", "description": "Dep_Time을 시간대로 분류한다."},
            {"id": "P2", "description": "Airline 수 기준 내림차순 정렬한다."},
            {"id": "P3", "description": "reset_index()를 적용한다."}
        ]
    }
}
