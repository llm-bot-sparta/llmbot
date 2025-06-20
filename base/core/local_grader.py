import pandas as pd
import traceback
import streamlit as st
# 문제7~10번은 문제 6번에서 불러온 데이터가 정상적이라고 가정하고 채점
# 한 번 불러온 df를 메모리에 저장하여 중복 다운로드를 방지 (캐싱)

@st.cache_data
def load_sample_dataframe():
    """
    이 함수는 처음 호출될 때 단 한 번만 실행되고 캐싱됩니다.
    이후 호출에서는 캐시된 데이터를 반환합니다.
    """
    # print('데이터로드 시작')
    import os
    # print(os.getcwd())
    df = pd.read_csv('./data/7th/flight_data.csv', sep=';')
    # print(df.head(3))
    # print('데이터로드 종료')
    return df

def execute_python_code(student_code, function_name, test_cases):
    """
    학생 코드를 실행하고 2단계 검증(타입, 형태)을 포함하여 테스트합니다.
    """
    try:
        namespace = {'pd': pd}
        exec(student_code, namespace)
        
        if function_name not in namespace:
            return {"error": f"함수 '{function_name}'이(가) 정의되지 않았습니다."}
        
        test_results = []
        # print('execute 함수 for문 전')
        for i, test_case in enumerate(test_cases, 1):
            input_value = test_case['input']
            # 문제 7 ~ 10의 경우 'df_sample' 신호를 감지하고 데이터 불러오기
            if input_value == "df_sample":
                try:
                    # load_sample_dataframe()을 호출하면,
                    # Streamlit이 알아서 캐시된 데이터를 주거나 없으면 다운로드 후 줍니다.
                    # print('데이터 로드 함수 콜')
                    df = load_sample_dataframe()
                    # print('정상적으로 수신')
                    input_value = df.copy()
                    # print('복제완료')
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

                #Case 1: 타입 검증
                if 'expected_type' in test_case:
                    expected_type = test_case['expected_type']
                    actual_type = type(result).__name__
                    expected_parts.append(f"Type: {expected_type}")
                    result_parts.append(f"Type: {actual_type}")
                    if not (
                        (expected_type == 'DataFrame' and isinstance(result, pd.DataFrame)) or
                        (expected_type == 'Series' and isinstance(result, pd.Series)) or
                        (expected_type.lower() == actual_type.lower())
                    ):
                        passed = False

                # --- 2. 형태(Shape) 검증 ---
                if 'expected_shape' in test_case:
                    expected_shape = tuple(test_case['expected_shape'])
                    expected_parts.append(f"Shape: {expected_shape}")
                    if hasattr(result, 'shape') and result.shape == expected_shape:
                        result_parts.append(f"Shape: {result.shape}")
                    else:
                        result_parts.append(f"Shape: {getattr(result, 'shape', 'N/A')}")
                        passed = False

                # --- 3. 값(Value) 검증 ---
                if 'expected' in test_case:
                    expected = test_case['expected']
                    expected_parts.append(f"Value: {str(expected)[:50]}...") # 너무 길면 잘라서 표시
                    result_parts.append(f"Value: {str(result)[:50]}...")
                    
                    # Series/DataFrame은 .equals()나 .to_dict()로 비교
                    if isinstance(result, pd.Series):
                        if not result.to_dict() == expected:
                            passed = False
                    elif isinstance(result, pd.DataFrame):
                        if not result.equals(pd.DataFrame(expected)):
                            passed = False
                    # 일반 값 비교
                    elif result != expected:
                        passed = False
            
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
        return {"error": f"코드 실행 중 오류 발생: {traceback.format_exc()}"}

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

            # --- 👇 기대 결과와 학생 결과를 나란히 표시 ---
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
                result_obj = r.get('result_obj')
                
                if isinstance(result_obj, (pd.DataFrame, pd.Series)):
                    st.write(result_obj)
                else:
                    st.code(str(result_obj), language='python')
