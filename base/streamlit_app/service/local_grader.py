import sys
import io
import pandas as pd
from contextlib import redirect_stdout
import traceback
# 문제7~10번은 문제 6번에서 불러온 데이터가 정상적이라고 가정하고 채점
# 한 번 불러온 df를 메모리에 저장하여 중복 다운로드를 방지 (캐싱)
CACHED_DF_SAMPLE = None

def execute_python_code(student_code, function_name, test_cases):
    """
    학생 코드를 실행하고 2단계 검증(타입, 형태)을 포함하여 테스트합니다.
    """
    global CACHED_DF_SAMPLE
    try:
        namespace = {'pd': pd}
        exec(student_code, namespace)
        
        if function_name not in namespace:
            return {"error": f"함수 '{function_name}'이(가) 정의되지 않았습니다."}
        
        test_results = []
        
        for i, test_case in enumerate(test_cases, 1):
            input_value = test_case['input']
            # 문제 7 ~ 10의 경우
            # 'df_sample' 신호를 감지하고 GitHub에서 데이터 불러오기
            if input_value == "df_sample":
                try:
                    if CACHED_DF_SAMPLE is None:
                        print("Downloading and caching df_sample from GitHub...")
                        # GitHub에 업로드된 샘플 CSV 파일의 'Raw' URL
                        sample_url = "https://raw.githubusercontent.com/llm-bot-sparta/sparta_coding/refs/heads/main/flight_data.csv"
                        # 6번 문제와 동일한 데이터, 동일한 옵션으로 불러오기
                        CACHED_DF_SAMPLE = pd.read_csv(sample_url, sep=';')
                    
                    # 원본이 수정되지 않도록 복사본을 입력값으로 사용
                    input_value = CACHED_DF_SAMPLE.copy()

                except Exception as e:
                    return {"error": f"GitHub에서 샘플 데이터를 불러오는 중 오류 발생: {e}"}

            # 문제2번 calculator의 경우 3가지 전달인자를 동시에 받기때문에 unpack 옵션 추가
            try:
                # test_case 딕셔너리에서 'unpack_args' 키를 확인. 없으면 기본값 False.
                should_unpack = test_case.get("unpack_args", False)

                if should_unpack:
                    # unpack_args가 true일 때만 인자를 풀어서 전달 
                    print(*input_value,'unpack')
                    result = namespace[function_name](*input_value)
                else:
                    # 그 외의 모든 경우는 인자를 그대로 전달
                    print(input_value,'not unpack')
                    result = namespace[function_name](input_value)          
                
                passed = False
                expected_str = ""
                result_str = ""

                # Case 1: 'expected' 키가 있으면 일반 값 비교
                if 'expected' in test_case:
                    expected = test_case['expected']
                    expected_str = str(expected)
                    result_str = str(result)
                    passed = (result == expected)

                # Case 2: 'expected' 키가 없으면 타입/형태 2단계 검증
                else:
                    type_check_passed = True
                    shape_check_passed = True
                    
                    expected_parts = []
                    result_parts = []

                    # 1단계: 타입 검증 (expected_type이 있는 경우)
                    if 'expected_type' in test_case:
                        expected_type = test_case['expected_type']
                        actual_type = type(result).__name__
                        expected_parts.append(f"Type: {expected_type}")
                        result_parts.append(f"Type: {actual_type}")

                        if not (
                            (expected_type == 'DataFrame' and isinstance(result, pd.DataFrame)) or
                            (expected_type == 'Series' and isinstance(result, pd.Series)) or
                            (expected_type == 'float' and isinstance(result, (int, float))) or
                            (expected_type.lower() == actual_type.lower())
                        ):
                            type_check_passed = False

                    # 2단계: 형태 검증 (expected_shape가 있고, 1단계 통과 시)
                    if 'expected_shape' in test_case:
                        expected_shape = tuple(test_case['expected_shape'])
                        expected_parts.append(f"Shape: {expected_shape}")

                        if isinstance(result, (pd.DataFrame, pd.Series)):
                            actual_shape = result.shape
                            result_parts.append(f"Shape: {actual_shape}")
                            if actual_shape != expected_shape:
                                shape_check_passed = False
                        else:
                            result_parts.append("Shape: N/A (대상이 DataFrame/Series 아님)")
                            shape_check_passed = False
                    
                    # 최종 통과 여부: 모든 검증을 통과해야 함
                    passed = type_check_passed and shape_check_passed
                    expected_str = ", ".join(expected_parts)
                    result_str = ", ".join(result_parts)

                test_results.append({
                    'test_case': i,
                    'input': str(input_value)[:100],
                    'expected': expected_str,
                    'result': result_str,
                    'passed': passed
                })

            except Exception as e:
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
    import streamlit as st
    
    for result in test_results:
        status = "✅" if result['passed'] else "❌"
        st.write(f"**테스트 케이스 {result['test_case']}**: {status}")
        st.write(f"입력값: `{result['input']}`")
        st.write(f"기대값: `{result['expected']}`")
        st.write(f"실행 결과: `{result['result']}`")
        st.write("---") 