QUESTIONS = {
    'ST_ML_1': {
        "title": "(EASY LEVEL) [통계] 중심 경향치 확인",
        "content": """
            -
            - **배경** : 주어진 데이터를 바탕으로 성별 Review Rating 에 대한 평균과 중앙값을 동시에 구해주세요.
            - **문제 의도** : 그룹별 기술통계를 집계하는 능력을 기릅니다.
            - **요구 사항**
                - 함수명: `get_agg`
                - `groupby` 함수 혹은 `pivot_table`을 사용 권장
                - 반올림해서 소수점 2자리까지 표시
                - 예시 결과의 행과 열 index에 주의해서 `DataFrame` 자료형으로 출력
            """,
        "model_answer": """
                        def get_agg(df):
                            # groupby를 사용하여 평균과 중앙값 계산
                            agg_df = df.groupby('Gender')['Review Rating'].agg(['mean', 'median'])

                            # 소수점 둘째 자리까지 반올림
                            agg_df = agg_df.round(2)

                            return agg_df

                        get_agg(data)
            """,
        "function_name": "get_agg",
        "test_cases":[
            {"input": "df_sample", "expected_type": "DataFrame",
             "expected": [
                {"Gender": "Female", "mean": 3.74, "median": 3.7},
                {"Gender": "Male", "mean": 3.75, "median": 3.8}
            ]}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_agg로 정확히 작성되었는가?"},
            {"id": "groupby_usage", "description": "groupby 함수 또는 pivot_table을 사용하여 성별로 그룹화했는가?"},
            {"id": "aggregation_methods", "description": "평균(mean)과 중앙값(median)을 모두 계산했는가?"},
            {"id": "rounding", "description": "결과를 소수점 2자리까지 반올림(round(2))했는가?"},
            {"id": "dataframe_output", "description": "DataFrame 자료형으로 올바르게 출력되었는가?"},
        ]},
    'ST_ML_2': {
        "title": "(MID LEVEL) [통계] 문제 2: 가설 설정",
        "content": """
            - **정답 처리 조건** : t-stat 부호가 반전되어도 정답 처리(양측검정)
            - **배경** : 두 집단의 평균 차이를 비교할 때는 정규성과 등분산성을 전제로 독립표본 t검정을 사용합니다. 해당 전제가 충족되었다고 가정하고 ‘성별에 따른 리뷰 평점 평균 차이’를 검정하세요.
            - **문제 의도**
                - `scipy.stats` 라이브러리를 사용해 두 집단 간 평균 비교를 위한 독립표본 t-검정을 수행한다.
                - 가설 설정 → t 통계량과 p-value 해석 → 귀무가설 채택/기각 과정을 연습한다.
            - **요구 사항**
                - 함수명: `get_ttest`
                - `scipy.stats` 내 함수를 사용해 성별에 따른 리뷰 평점 평균 차이를 검정
                - 정규성을 만족한다고 가정하고, 등분산 가정도 만족하므로 `equal_var=True`로 지정
                - t통계값(t_stat)과 p-value(p_value)는 소수점 4자리까지 표시
                - 함수 아래 주석으로 유의수준 0.05에서 귀무가설 기각/채택 여부 및 근거를 간략 서술
        """,
        "model_answer": """
                        import pandas as pd
                        from scipy.stats import ttest_ind

                        def get_ttest(df):
                            # 성별에 따른 평점 추출
                            female_rating = df[df['Gender'] == 'Female']['Review Rating']
                            male_rating = df[df['Gender'] == 'Male']['Review Rating']

                            # T-test 수행 (등분산 가정)
                            t_stat, p_value = ttest_ind(female_rating, male_rating, equal_var=True)
                            t_stat = round(t_stat, 4)
                            p_value = round(p_value, 4)

                            return t_stat, p_value

                        get_ttest(data)
                        # p-value가 0.05보다 훨씬 큰 0.61 값을 가지기 때문에 귀무가설을 기각할 수 없다.
        """,
        "function_name": "get_ttest",
        "test_cases":[
            {"input": "df_sample", "expected_type": "tuple",
             "expected": "(-0.5097, 0.6103)"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_ttest로 정확히 작성되었는가?"},
            {"id": "scipy_usage", "description": "scipy.stats의 ttest_ind 함수를 사용했는가?"},
            {"id": "rounding", "description": "t통계값(t_stat)과 p-value(p_value)를 소수점 4자리까지 반올림했는가?"},
            {"id": "return_type", "description": "함수에서 t_stat, p_value를 튜플 형태로 반환했는가?"},
            {"id": "hypothesis_comment", "description": "함수 아래 주석으로 유의수준 0.05에서 귀무가설 기각/채택 여부 및 근거를 간략히 서술했는가?"}
        ]
    },
    "ST_ML_3": {
        "title": "(EASY LEVEL) [머신러닝] 문제 3: 웹 사이트 방문자 예측 모델 만들기",
        "content": """
            - **배경** : 여러분은 현재 마케팅 부서의 데이터 분석가로서, 회사의 **주간 광고비 지출**이 **웹사이트 방문자 수**에 어떤 영향을 미치는지 분석하고 예측하는 업무를 맡았습니다. 아래 데이터는 최근 20주간의 데이터를 수집했으며, 이를 통해 광고비 지출과 웹사이트 방문자 수 사이에 어떤 경향이 있는지 파악하고 싶습니다. 특히, 선형적인 관계가 있다고 가정하고, 이를 기반으로 향후 광고비 투입 시 예상되는 웹사이트 방문자 수를 예측하는 모델을 만들 계획입니다.
            - **데이터 설명**
                - **X (독립 변수): 주간 광고비 지출**
                    - **단위:** 백만원 (예: 1.0은 100만원, 5.8은 580만원)
                    - 회사가 디지털 마케팅 플랫폼에 집행한 한 주간의 총 광고 비용입니다.
                - **Y (종속 변수): 주간 웹사이트 방문자 수**
                    - **단위:** 만 명 (예: 2.5는 25,000명
                    - 해당 주에 회사의 웹사이트를 방문한 순수 방문자(Unique Visitors)의 총합입니다.
            - **요구 사항**
                - 함수명: `get_lr`
                - 광고비 지출과 웹 사이트 방문자 데이터를 학습시켜 선형회귀 모델 수립
                    - **문제 의도**
                        - `scikit-learn` 의 `LinearRegression` 클래스를 사용할 수 있다.
                        - 모델을 가져와 학습 시킬 수 있다.
                - 선형회귀를 학습 시킨 모델을 반환
        """,
        "model_answer": """
                        import pandas as pd
                        from sklearn.linear_model import LinearRegression

                        def get_lr(df):
                            lr = LinearRegression()
                            lr.fit(df[['visitor']], df['expense'])
                            return lr
        """,
        "function_name" : "get_lr",
        "test_cases":[
            {"input": "df_sample", "expected_type": "LinearRegression"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_lr로 정확히 작성되었는가?"},
            {"id": "scikit_learn_usage", "description": "scikit-learn의 LinearRegression 클래스를 사용했는가?"},
            {"id": "model_fit", "description": "광고비 지출과 웹 사이트 방문자 데이터를 학습시켜 선형회귀 모델을 수립했는가?"},
            {"id": "model_return", "description": "학습 시킨 모델을 반환했는가?"}
        ]   
},
    'ST_ML_4': {
        "title": "(EASY LEVEL) [머신러닝] 문제 4: 회귀 모델링 평가하기 ",
        "content": """
            - **정답 처리 조건** : rmse 값이 0.1 이하일 경우 정답 처리
            - **배경** : 문제 3번에서 정의한 모델을 이용하여 평가해보세요
            - **문제 의도**
                - `scikit-learn` 의 평가지표 `root_mean_squared_error` 를 사용할 수 있다.
                - 평가 지표를 올바르게 해석할 수 있다.
            - **요구 사항**
                - 함수명: `get_rmse`
                - rmse에 대한 값을 함수로 반환
        """,
        "model_answer": """
                        import pandas as pd
                        from sklearn.linear_model import LinearRegression
                        from sklearn.metrics import root_mean_squared_error

                        def get_rmse(df):
                        #먼저 3번 문제의 코드를 작성
                            lr = LinearRegression()
                            lr.fit(df[['expense']], df['visitor'])
                            y_pred = lr.predict(df[['expense']])
                            answer = root_mean_squared_error(df['visitor'], y_pred)
                            return round(answer,2)
        """,
        "function_name":"get_rmse",
        "test_cases":[
            {"input": "df_sample", "expected_type": "float",
             "expected": "0.03"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_rmse로 정확히 작성되었는가?"},
            {"id": "model_fit", "description": "선형회귀 모델을 데이터에 맞게 학습시켰는가?"},
            {"id": "model_predict", "description": "학습된 모델로 예측값(y_pred)을 생성했는가?"},
            {"id": "rounding", "description": "RMSE 값을 소수점 2자리로 반올림했는가?"},
            {"id": "return_value", "description": "계산된 RMSE 값을 함수에서 반환했는가?"}
        ]
    },
    'ST_ML_5': {
        "title": "(MID LEVEL) [통계] 문제 5: 카이제곱 검정",
        "content": """
            - **배경** : 두 범주형 변수 간에 관계가 있는지 알고 싶을 때 카이제곱 독립성 검정을 사용합니다. 예를 들어, ‘색상과 계절’ 사이에 연관이 있다면, 특정 색상이 특정 계절에 더 많이 나타날 수 있습니다. 이러한 관계의 유의미성을 통계적으로 검정해봅시다.
            - **문제 의도**
                - 범주형 변수 간 관계를 검정할 수 있는 카이제곱 검정을 학습한다.
                - `pd.crosstab()`과 `scipy.stats` 내 함수를 사용하는 방법을 익힌다.
                - 검정 결과를 바탕으로 귀무가설의 채택/기각 여부를 판단하는 능력을 기른다.
            - **요구 사항**
                - 함수명: `get_chi2`
                - `Color`와 `Season` 변수의 관계를 확인하기 위한 **카이제곱 독립성 검정**을 수행
                - 카이제곱 통계값(chi)과 p-value(p_value)는 소수점 4자리까지 표시
                - 함수 아래 주석으로 유의수준 0.05에서 귀무가설 기각/채택 여부 및 근거를 간략 서술
        """,
        "model_answer": """
                        import pandas as pd
                        from scipy.stats import chi2_contingency

                        def get_chi2(df):
                            # 1. 빈도표 생성
                            contingency_table = pd.crosstab(df['Color'], df['Season'])

                            # 2. 카이제곱 검정
                            chi, p, dof, expected = chi2_contingency(contingency_table)

                            chi = round(chi, 4)
                            p = round(p, 4)

                            return chi, p

                        get_chi2(data)
                        # p-value가 0.05보다 큰 0.7186의 값을 가지기 때문에 귀무가설을 기각할 수 없다. 따라서 두 변수는 독립이다.
        """,
        "function_name": "get_chi2",
        "test_cases":[
            {"input": "df_sample", "expected_type": "tuple",
             "expected": "(64.6506, 0.7186)"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_chi2로 정확히 작성되었는가?"},
            {"id": "crosstab_usage", "description": "pd.crosstab 함수를 사용하여 빈도표를 생성했는가?"},
            {"id": "chi2_contingency", "description": "scipy.stats의 chi2_contingency 함수를 사용하여 카이제곱 검정을 수행했는가?"},
            {"id": "rounding", "description": "카이제곱 통계값(chi)과 p-value(p)를 소수점 4자리까지 반올림했는가?"},
            {"id": "return_type", "description": "함수에서 chi, p를 튜플 형태로 반환했는가?"},
            {"id": "hypothesis_comment", "description": "함수 아래 주석으로 유의수준 0.05에서 귀무가설 기각/채택 여부 및 근거를 간략히 서술했는가?"}
        ]
    },
    'ST_ML_6': {
        "title": "(HIGH LEVEL) [통계] 문제 6 : 다중선형회귀 분석 및 정확도 평가",
        "content": """
            - 배경 : 하나의 종속 변수가 여러 개의 독립 변수에 의해 영향을 받는 경우, 우리는 다중선형회귀를 사용합니다. 고객의 나이와 과거 구매 건수(Previous Purchases)가 구매 금액(Purchase Amount (USD))에 어떤 영향을 미쳤는지 분석하고, 이 모델이 데이터를 얼마나 잘 설명하는지를 평가해봅니다.
            - **문제 의도**
                - 2개 이상의 독립 변수를 활용한 다중 회귀 모델을 구현한다.
                - `sklearn.linear_model` 과 `sklearn.metrics`를 사용하여 회귀 모델의 설명력을 해석한다.
            - **요구 사항**
                - 함수명: `get_multi_reg`
                - Y (종속 변수): `Purchase Amount (USD)`
                - X (독립 변수): `Age`, `Previous Purchases`
                - 회귀 모델 학습 후 결정계수($R^2$)를 소수점 4자리까지 출력
                - 함수 아래 주석으로 해당 결정계수 값을 통해 알 수 있는 내용 간략 서술
            """,
        "model_answer": """
                        from sklearn.linear_model import LinearRegression
                        from sklearn.metrics import r2_score

                        def get_multi_reg(df):
                            # 설명 변수와 타깃 변수 정의
                            X = df[['Age', 'Previous Purchases']] # 2차원 배열
                            y = df['Purchase Amount (USD)']

                            # 회귀 모델 학습
                            model = LinearRegression()
                            model.fit(X, y)

                            # 예측 및 R^2 계산
                            y_pred = model.predict(X)
                            r2 = r2_score(y, y_pred)

                            r2 = round(r2, 4)

                            return r2

                        get_multi_reg(data)
        """,
        "function_name": "get_multi_reg",
        "test_cases":[
            {"input": "df_sample", "expected_type": "float",
             "expected": "0.0002"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_multi_reg로 정확히 작성되었는가?"},
            {"id": "linear_regression", "description": "LinearRegression 클래스를 사용하여 회귀 모델을 학습시켰는가?"},
            {"id": "rounding", "description": "결정계수를 소수점 4자리까지 반올림했는가?"},
            {"id": "return_value", "description": "계산된 결정계수를 함수에서 반환했는가?"},
            {"id": "comment", "description": "함수 아래 주석으로 결정계수 값을 통해 알 수 있는 내용을 간략히 서술했는가?"}
        ]
    },
    'ST_ML_7': {
        "title": "(MID LEVEL) [머신러닝] 문제 7 : 고 지출 고객 분류하기",
        "content": """
            - **정답 처리 조건** : 정확도 값이 0.5 이상일 경우 정답 처리
            - **배경**: 당신은 이커머스 데이터 분석가 입니다.  고객별 구매에 대한 데이터가 집계되어 있으며 충성 고객을 예측하기 위한 모델링을 진행하려합니다. 80달러 이상 지출한 고객을 Y 변수 1로 설정하여 모델링을 진행해 보세요.
            - **문제 의도**
                - 랜덤포레스트 모델을 이용하여 분류 모델링을 할 수 있다.
                - 정확도 지표를 계산할 수 있다.
            - **요구 사항**
                - 함수명: `get_acc`
                - 구매 금액이 80달러 이상인 사람을 Y = 1 로 예측하는 모델링을 랜덤포레스트 모델로 진행
                - X 변수는 다음 2가지 `['Age', 'Previous Purchases']`  만 사용하
                - 예측 모델링 한 결과의 정확도를 반환
        """,
        "model_answer": """
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.metrics import accuracy_score

            def get_acc(df):
                # 지정된 3가지 수치형 변수만 선택
                features = ['Age', 'Previous Purchases']
                X = df[features]
                y = df['y']

                # 랜덤 포레스트 모델 학습
                model_rf = RandomForestClassifier(random_state=42)
                model_rf.fit(X, y)
                # 예측 및 정확도 측정
                y_pred = model_rf.predict(X)
                accuracy = accuracy_score(df['y'], y_pred)
                return round(accuracy, 2)
        """,
        "function_name": "get_acc",
        "test_cases":[
            {"input": "df_sample", "expected_type": "float",
             "expected": "0.88"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_acc로 정확히 작성되었는가?"},
            {"id": "random_forest_usage", "description": "RandomForestClassifier 클래스를 사용하여 랜덤 포레스트 모델을 학습시켰는가?"},
            {"id": "accuracy_score", "description": "accuracy_score 함수를 사용하여 정확도를 계산했는가?"},
            {"id": "rounding", "description": "정확도를 소수점 2자리까지 반올림했는가?"},
            {"id": "return_value", "description": "계산된 정확도를 함수에서 반환했는가?"}
        ]
    },
    'ST_ML_8': {
        "title": "(HIGH LEVEL) [머신러닝] 문제 8 : 고 지출 고객 분류하기2",
        "content": """
            - **정답 처리 조건** : 학습 데이터의 f1 score가 0.5 이상, 평가 데이터의 f1 score가 소수점일 경우에 정답 처리
            - **문제 의도**
                - 데이터를 학습/평가 데이터로 나누어 학습할 수 있다.
            - **요구 사항**
                - 함수명: `get_vali`
                - 데이터를 `test_size = 0.2`로 학습(출처: [4. 데이터분석 프로세스](https://www.notion.so/4-fd3adfd57b424f518c533adc362aabee?pvs=21)  2.5 단원)
                - 독립 변수는 최소 다음 3가지를 포함 `['Age', 'Previous Purchases', 'Gender']`
                - `Gender` 변수는 1,0으로 인코딩
                - 함수는 train의 f1 score, test의 f1 score를 순서대로 반환
        """,
        "model_answer": """
                        import pandas as pd
                        from sklearn.model_selection import train_test_split
                        from sklearn.ensemble import RandomForestClassifier
                        from sklearn.metrics import f1_score, accuracy_score

                        def get_vali(df):
                            features_to_use = ['Age', 'Previous Purchases', 'Gender']
                            X = df[features_to_use]
                            y = df['y']

                            # 2. Train-Validation-Test 데이터 분할 (전처리 전에 분할)
                            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

                            # 3. 각 세트별 전처리 (수동, df.loc 방식)
                            # Gender 변수를 람다 식으로 직접 인코딩하여 새로운 컬럼에 할당 (기존 컬럼 덮어쓰기)
                            X_train.loc[:, 'Gender'] = X_train['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
                            X_test.loc[:, 'Gender'] = X_test['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

                            # 4. 랜덤 포레스트 모델 학습 (학습 세트로 직접 훈련)
                            model_rf = RandomForestClassifier(random_state=42)
                            model_rf.fit(X_train, y_train)

                            # 5. 최종 테스트 세트 평가
                            y_pred_train = model_rf.predict(X_train)
                            y_pred_test = model_rf.predict(X_test)

                            train_f1 = f1_score(y_train, y_pred_train)
                            test_f1 = f1_score(y_test, y_pred_test)
                            return round(train_f1, 2), round(test_f1, 2)
        """,
        "function_name": "get_vali",
        "test_cases":[
            {"input": "df_sample", "expected_type": "tuple",
             "expected": "(0.91, 0.67)"}
        ],
        "evaluation_criteria": [
            {"id": "function_name", "description": "함수명이 get_vali로 정확히 작성되었는가?"},
            {"id": "train_test_split", "description": "train_test_split 함수를 사용하여 데이터를 학습/평가 데이터로 나누었는가?"},
            {"id": "f1_score", "description": "f1_score 함수를 사용하여 학습/평가 데이터의 f1 score를 계산했는가?"},
            {"id": "rounding", "description": "f1 score를 소수점 2자리까지 반올림했는가?"},
            {"id": "return_value", "description": "계산된 f1 score를 함수에서 반환했는가?"}
        ]
    }
}