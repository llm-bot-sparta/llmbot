import pandas as pd
import traceback
import streamlit as st
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from question import QUESTIONS
import numpy as np
# 문제7~10번은 문제 6번에서 불러온 데이터가 정상적이라고 가정하고 채점
# 한 번 불러온 df를 메모리에 저장하여 중복 다운로드를 방지 (캐싱)

@st.cache_data
def load_sample_dataframe(assignment_type, qid):
    """
    이 함수는 처음 호출될 때 단 한 번만 실행되고 캐싱됩니다.
    이후 호출에서는 캐시된 데이터를 반환합니다.
    """
    if assignment_type == '통계&머신러닝':
        if qid in ['ST_ML_3', 'ST_ML_4']:
            X = [1.0, 1.2, 1.5, 1.7, 2.0, 2.2, 2.5, 2.7, 3.0, 3.2, 3.5, 3.7, 4.0, 4.2, 4.5, 4.7, 5.0, 5.2, 5.5, 5.8]
            y = [2.5, 2.8, 3.2, 3.5, 4.0, 4.3, 4.8, 5.0, 5.5, 5.8, 6.2, 6.5, 7.0, 7.3, 7.8, 8.0, 8.5, 8.8, 9.2, 9.5]
            data = {'expense': X, 'visitor': y}
            df = pd.DataFrame(data)
        elif qid in ['ST_ML_1', 'ST_ML_2', 'ST_ML_5', 'ST_ML_6', 'ST_ML_7', 'ST_ML_8']:
            df = pd.read_csv(os.path.join(BASE_DIR, '../data/7th/statistics.csv'))
            df['y'] = (df['Purchase Amount (USD)'] >= 80).astype(int)
    elif assignment_type == 'Python기초':
        df = pd.read_csv(os.path.join(BASE_DIR, '../data/7th/flight_data.csv'), sep=';')
    return df

def execute_python_code(student_code, assignment_type, qid, test_cases):
    """
    학생 코드를 실행하고 2단계 검증(타입, 형태)을 포함하여 테스트합니다.
    """
    try:
        import numpy as np
        import pandas as pd
        from scipy import stats
        from scipy.stats import ttest_ind, chi2_contingency
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_squared_error, root_mean_squared_error, r2_score, f1_score, accuracy_score
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        # 첫 번째 test_case에서 input_value를 가져와서 namespace에 사용
        first_input = test_cases[0]['input'] if test_cases else "df_sample"
        if first_input == "df_sample":
            input_value = load_sample_dataframe(assignment_type, qid)
        else:
            input_value = first_input
            
        namespace = {
            'pd': pd,
            'np': np,
            'round': round,  # round 함수 추가
            'ttest_ind': ttest_ind,
            'chi2_contingency': chi2_contingency,
            'stats': stats,  # scipy.stats 전체 모듈 추가
            'LinearRegression': LinearRegression,
            'mean_squared_error': mean_squared_error,
            'root_mean_squared_error': root_mean_squared_error,
            'r2_score': r2_score,
            'f1_score': f1_score,
            'accuracy_score': accuracy_score,
            'RandomForestClassifier': RandomForestClassifier,
            'train_test_split': train_test_split,
            'df': input_value  # 입력 데이터를 df로 사용 가능하도록 추가
        }
        
        test_results = []
        
        try:
            exec(student_code, namespace)
            function_name = QUESTIONS[assignment_type][qid].get('function_name', '')
            if function_name not in namespace:
                return {"error": f"함수 '{function_name}'이(가) 정의되지 않았습니다."}
            
            # print('execute 함수 for문 전')
            for i, test_case in enumerate(test_cases, 1):
                input_value = test_case['input']
                if input_value == "df_sample":
                    try:
                        # load_sample_dataframe()을 호출하면,
                        # Streamlit이 알아서 캐시된 데이터를 주거나 없으면 다운로드 후 줍니다.
                        df = load_sample_dataframe(assignment_type, qid)
                        input_value = df.copy()
                    except Exception as e:
                        return {"error": f"데이터를 불러오는 중 오류 발생: {e}"}

                # 문제2번 calculator의 경우 3가지 전달인자를 동시에 받기때문에 unpack 옵션 추가
                try:
                    # test_case 딕셔너리에서 'unpack_args' 키를 확인. 없으면 기본값 False.
                    should_unpack = test_case.get("unpack_args", False)

                    if should_unpack:
                        # unpack_args가 true일 때만 인자를 풀어서 전달 
                        # print(*input_value,'unpack')
                        result = namespace[function_name](*input_value)
                    else:
                        # 그 외의 모든 경우는 인자를 그대로 전달
                        
                        #6번 문제의 경우, input value가 url이기 때문에 코드 실행결과를 바로 할당
                        if function_name == 'get_csv':
                            result = input_value
                        else:
                            result = namespace[function_name](input_value)          
                    
                    passed = True
                    expected_parts = []
                    result_parts = []

                    # # --- 1. 타입 검증 ---
                    # if 'expected_type' in test_case:
                    #     expected_type = test_case['expected_type']
                    #     actual_type = type(result).__name__
                    #     expected_parts.append(f"Type: {expected_type}")
                    #     result_parts.append(f"Type: {actual_type}")
                    #     if qid == 'ST_ML_4':
                    #         print(f"ST_ML_4 타입 검증: expected_type={expected_type}, actual_type={actual_type}")
                    #     # ST_ML_4: 타입 검증 건너뛰기 (값 검증에서 조건부 정답 처리)
                    #     if qid == 'ST_ML_4':
                    #         print(f"ST_ML_4 타입 검증 건너뛰기: expected_type={expected_type}, actual_type={actual_type}")
                    #         # 타입 검증 건너뛰기 (값 검증에서 조건부 정답 처리)
                    #         pass
                    #     elif not (
                    #         (expected_type == 'DataFrame' and isinstance(result, pd.DataFrame)) or
                    #         (expected_type == 'Series' and isinstance(result, pd.Series)) or
                    #         (expected_type.lower() == actual_type.lower())
                    #     ):
                    #         if qid == 'ST_ML_4':
                    #             print(f"ST_ML_4 타입 검증 실패: expected_type={expected_type}, actual_type={actual_type}")
                    #         passed = False

                    # # --- 2. 형태(Shape) 검증 ---
                    # if 'expected_shape' in test_case:
                    #     expected_shape = tuple(test_case['expected_shape'])
                    #     expected_parts.append(f"Shape: {expected_shape}")
                    #     if hasattr(result, 'shape') and result.shape == expected_shape:
                    #         result_parts.append(f"Shape: {result.shape}")
                    #     else:
                    #         result_parts.append(f"Shape: {getattr(result, 'shape', 'N/A')}")
                    #         passed = False

                    # --- 3. 값(Value) 검증 ---
                    if 'expected' in test_case:
                        expected = test_case['expected']
                        # ST_ML_3: 반환값이 LinearRegression 타입이기만 하면 정답
                        if qid == 'ST_ML_3':
                            value_match = isinstance(result, LinearRegression)
                            if not value_match:
                                passed = False
                        else:
                            expected_parts.append(f"Value: {str(expected)[:50]}...") # 너무 길면 잘라서 표시
                            result_parts.append(f"Value: {str(result)[:50]}...")
                            value_match = False  # 기본값 설정
                            if isinstance(result, pd.Series):
                                value_match = result.to_dict() == expected
                                if not value_match:
                                    passed = False
                            elif isinstance(result, pd.DataFrame) and hasattr(result, 'columns'):
                                if qid == 'ST_ML_1':
                                    if isinstance(expected, list):
                                        expected_df = pd.DataFrame(expected)
                                        expected_df = expected_df.set_index("Gender")
                                    else:
                                        expected_df = expected
                                    # ST_ML_1: MultiIndex DataFrame을 일반 DataFrame으로 변환
                                    if hasattr(result.columns, 'levels'):
                                        # MultiIndex 컬럼을 평면화
                                        result = result.droplevel(0, axis=1)  # 첫 번째 레벨 제거
                                        # Gender를 인덱스로 설정
                                        if 'Gender' in result.columns:
                                            result = result.set_index('Gender')
                                    else:
                                        result.columns = [col.lower() for col in result.columns]
                                else:
                                    if isinstance(expected, dict):
                                        expected_df = pd.DataFrame(expected)
                                    else:
                                        expected_df = expected
                                    expected_df.columns = [col.lower() for col in expected_df.columns]
                                    # result가 실제로 DataFrame인지 확인
                                    if hasattr(result, 'columns'):
                                        # MultiIndex DataFrame 처리
                                        if hasattr(result.columns, 'levels'):
                                            # MultiIndex인 경우 컬럼명을 문자열로 변환
                                            result.columns = [str(col) for col in result.columns]
                                        else:
                                            result.columns = [col.lower() for col in result.columns]
                                    else:
                                        value_match = False
                                        if not value_match:
                                            passed = False
                                        continue
                                
                                value_match = result.equals(expected_df)
                                if not value_match:
                                    passed = False
                            elif isinstance(result, tuple):
                                # expected가 str이면 튜플로 변환
                                if isinstance(expected, str):
                                    expected = eval(expected)
                                try:
                                    float_results = [float(r) for r in result]
                                    float_expected = [float(e) for e in expected]
                                    if qid == 'ST_ML_2' and len(float_results) == 2:
                                        # ST_ML_2: tstat(첫 번째 값)은 부호 반전 허용, p-value(두 번째 값)는 기존대로 비교
                                        tstat_match = abs(float_results[0]) == abs(float_expected[0])
                                        pval_match = float_results[1] == float_expected[1]
                                        value_match = tstat_match and pval_match
                                    elif qid == 'ST_ML_8' and len(float_results) == 2:
                                        # ST_ML_8: train_f1은 0.5 이상, test_f1은 소수점이기만 하면 정답 처리
                                        train_f1 = float_results[0]
                                        test_f1 = float_results[1]
                                        train_condition = train_f1 >= 0.5
                                        test_condition = 0 < test_f1 < 1  # 소수점이기만 하면 정답
                                        value_match = train_condition and test_condition
                                    else:
                                        value_match = all(float(r) == float(e) for r, e in zip(result, expected))
                                except Exception as ex:
                                    value_match = result == expected
                                if not value_match:
                                    passed = False
                            elif isinstance(result, (float, int, np.floating)) or isinstance(expected, (float, int, np.floating)) or (isinstance(result, str) and result.replace('.', '').replace('-', '').isdigit()) or (isinstance(expected, str) and expected.replace('.', '').replace('-', '').isdigit()):
                                # ST_ML_4: 학생 결과값이 0.1 이하면 정답 처리
                                if qid == 'ST_ML_4':
                                    print(f"ST_ML_4 조건부 정답 처리: result={result}, type(result)={type(result)}")
                                    try:
                                        result_float = float(result)
                                        value_match = result_float <= 0.1
                                        print(f"ST_ML_4: result_float={result_float}, value_match={value_match}")
                                    except Exception as e:
                                        print(f"ST_ML_4 float 변환 에러: {e}")
                                        value_match = False
                                # ST_ML_7: 학생 결과값이 0.5 이상이면 정답 처리
                                elif qid == 'ST_ML_7':
                                    value_match = float(result) >= 0.5
                                else:
                                    value_match = float(result) == float(expected)
                                if not value_match:
                                    print(f"ST_ML_4 value_match 실패: value_match={value_match}")
                                    passed = False
                            elif result != expected:
                                passed = False
                            
                            print()
                
                    # --- 최종 결과 취합 ---
                    expected_str = ", ".join(expected_parts)

                    test_results.append({
                        'test_case': i,
                        'input': str(input_value)[:100],
                        # 'expected' 관련 정보를 상세히 전달
                        'expected_str_header': expected_str,  # expander 제목 등에 사용할 간단한 문자열
                        'expected_obj': test_case.get('expected'), # 원본 expected 데이터 (dict, list 등)
                        'expected_type': test_case.get('expected_type'), # 'Series', 'DataFrame' 등 타입 정보
                        'result_obj': result, 
                        'passed': passed
                    })

                except Exception as e:
                    print(f"에러 발생: {e}")
                    print(traceback.format_exc())
                    # 에러 발생 시의 정보 구성
                    expected_info_list = []
                    if 'expected' in test_case: expected_info_list.append(f"Value: {test_case['expected']}")
                    if 'expected_type' in test_case: expected_info_list.append(f"Type: {test_case['expected_type']}")
                    if 'expected_shape' in test_case: expected_info_list.append(f"Shape: {test_case['expected_shape']}")
                    
                    test_results.append({
                        'test_case': i,
                        'input': str(input_value)[:100],
                        'expected': ", ".join(expected_info_list),
                        'result': f'에러 발생: \n {traceback.format_exc()}',
                        'passed': False
                    })

            return {"output": test_results}

        except Exception as e:
            # 함수 실행 중 에러가 발생한 경우
            error_message = f"코드 실행 중 오류 발생: {traceback.format_exc()}"
            test_results.append({
                'test_case': 1,
                'input': "함수 실행 중 에러 발생",
                'expected': "정상 실행",
                'result': error_message,
                'passed': False
            })
            return {"output": test_results}

    except Exception as e:
        # 전체 함수 실행 중 에러가 발생한 경우
        error_message = f"코드 실행 중 오류 발생: {traceback.format_exc()}"
        test_results = [{
            'test_case': 1,
            'input': "전체 함수 실행 중 에러 발생",
            'expected': "정상 실행",
            'result': error_message,
            'passed': False
        }]
        return {"output": test_results}

def display_test_results(test_results):
    """
    테스트 결과를 Streamlit에 표시합니다.
    
    Args:
        test_results (list): 테스트 결과 목록
    """
    for i, r in enumerate(test_results, 1):
        status = "✅ 통과" if r['passed'] else "❌ 실패"
        
        # expander 제목에는 간단한 문자열 정보를 사용
        expander_title = f"Test Case {i}: {status}"
        
        with st.expander(expander_title, expanded=not r['passed']):
            st.markdown("**- 실행 정보**")
            st.text(f"입력 (Input)")
            st.code(r['input'], language='python')

            # 에러가 발생한 경우 전체 공간 사용
            result_obj = r.get('result_obj')
            result_str = r.get('result', '')  # result 필드도 확인
            
            if isinstance(result_str, str) and ('에러 발생' in result_str or 'Traceback' in result_str):
                st.error("🚨 코드 실행 중 에러가 발생했습니다:")
                st.code(result_str, language='python')
            elif isinstance(result_obj, str) and ('에러 발생' in result_obj or 'Traceback' in result_obj):
                st.error("🚨 코드 실행 중 에러가 발생했습니다:")
                st.code(result_obj, language='python')
            else:
                # 정상적인 경우 2열 레이아웃 사용
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**- 기대 결과 (Expected)**")
                    expected_obj = r.get('expected_obj')
                    expected_type = r.get('expected_type')
                    
                    # 기대 결과(expected)의 타입에 따라 다르게 표시
                    if expected_type == 'Series' and isinstance(expected_obj, dict):
                        st.write(pd.Series(expected_obj, name="Expected"))
                    elif expected_type == 'DataFrame' and expected_obj is not None:
                        st.write(pd.DataFrame(expected_obj))
                    else:
                        st.code(str(expected_obj), language='python')

                with col2:
                    st.markdown("**- 학생 결과 (Result)**")
                    if isinstance(result_obj, (pd.DataFrame, pd.Series)):
                        st.write(result_obj)
                    elif result_obj is not None:
                        st.code(str(result_obj), language='python')
                    else:
                        st.info("결과가 없습니다.")