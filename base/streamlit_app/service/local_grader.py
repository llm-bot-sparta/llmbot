import sys
import io
import pandas as pd
from contextlib import redirect_stdout
import ast

def execute_python_code(student_code, function_name, test_cases):
    """
    학생이 작성한 Python 코드를 로컬에서 실행하고 테스트합니다.
    
    Args:
        student_code (str): 학생이 작성한 Python 코드
        function_name (str): 테스트할 함수 이름
        test_cases (list): 테스트 케이스 목록. 각 케이스는 input과 expected를 포함한 딕셔너리
        
    Returns:
        dict: 실행 결과를 포함한 딕셔너리
    """
    try:
        # 코드 실행을 위한 네임스페이스
        namespace = {}
        
        # 필요한 모듈 import
        namespace['pd'] = pd
        
        # 학생 코드 실행
        exec(student_code, namespace)
        
        # 함수가 정의되었는지 확인
        if function_name not in namespace:
            return {
                "error": f"함수 '{function_name}'이(가) 정의되지 않았습니다."
            }
        
        # 테스트 결과를 저장할 리스트
        test_results = []
        
        # 각 테스트 케이스 실행
        for i, test_case in enumerate(test_cases, 1):
            input_value = test_case['input']
            expected = test_case['expected']
            
            # DataFrame 테스트를 위한 샘플 데이터 생성
            if input_value == "df_sample":
                input_value = pd.DataFrame({
                    'Date_of_Journey': ['01-01-2024', '02-01-2024', '03-01-2024'],
                    'Airline': ['A', 'B', 'C'],
                    'Price': [100, 200, 300],
                    'Dep_Time': ['10:00', '11:00', '12:00']
                })
            
            # 함수 실행 결과 캡처
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    if isinstance(input_value, list) and function_name == "simple_calculator":
                        # simple_calculator 함수는 리스트를 개별 인자로 전달
                        result = namespace[function_name](*input_value)
                    else:
                        # 다른 함수들은 입력값을 그대로 전달
                        result = namespace[function_name](input_value)
                except Exception as e:
                    test_results.append({
                        'test_case': i,
                        'input': str(input_value),
                        'expected': str(expected),
                        'result': f'에러: {str(e)}',
                        'passed': False
                    })
                    continue
            
            # 결과 비교
            if 'expected_type' in test_case:
                # 타입 체크
                expected_type = test_case['expected_type']
                actual_type = type(result).__name__
                passed = (
                    (expected_type == 'DataFrame' and isinstance(result, pd.DataFrame)) or
                    (expected_type == 'Series' and isinstance(result, pd.Series)) or
                    (expected_type == 'float' and isinstance(result, (int, float)))
                )
            elif 'expected_shape' in test_case:
                # DataFrame 형태 체크
                passed = (
                    isinstance(result, pd.DataFrame) and
                    result.shape == tuple(test_case['expected_shape'])
                )
            else:
                # 일반적인 값 비교
                passed = result == expected
            
            test_results.append({
                'test_case': i,
                'input': str(input_value),
                'expected': str(expected),
                'result': str(result),
                'passed': passed
            })
        
        return {
            "output": test_results
        }
        
    except Exception as e:
        return {
            "error": f"코드 실행 중 오류 발생: {str(e)}"
        }

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