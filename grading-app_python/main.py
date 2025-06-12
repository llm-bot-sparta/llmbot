import functions_framework
import traceback

@functions_framework.http
def grade_code(request):
    """
    학생의 파이썬 코드를 받아 테스트 케이스와 비교하여 채점합니다.
    요청 시 JSON에 'function_name'을 포함하여 문제별로 다른 함수 이름을 처리합니다.
    """
    # 1. 요청(Request) 분석 및 유효성 검사
    try:
        request_json = request.get_json(silent=True)
        # 'function_name' 필드가 요청에 포함되어 있는지 확인합니다.
        if not all(k in request_json for k in ["code", "function_name", "test_cases"]):
            return {"error": "Request body must contain 'code', 'function_name', and 'test_cases'."}, 400
        
        student_code_str = request_json["code"]
        # 함수 이름을 요청에서 동적으로 받아옵니다.
        function_name = request_json["function_name"] 
        test_cases = request_json["test_cases"]

    except Exception as e:
        return {"error": f"Invalid JSON format: {e}"}, 400

    # 2. 학생 코드 실행 및 함수 확보
    local_scope = {}
    try:
        exec(student_code_str, {}, local_scope)
    except Exception:
        return {
            "overall_result": "X",
            "reason": "Syntax Error",
            "details": traceback.format_exc()
        }, 200

    # 동적으로 받은 함수 이름으로 학생이 정의한 함수를 찾습니다.
    student_function = local_scope.get(function_name) 

    if not callable(student_function):
        # 함수를 찾지 못했다는 에러 메시지도 동적으로 생성합니다.
        return {
            "overall_result": "X",
            "reason": f"Function '{function_name}' not found in the submitted code."
        }, 200

    # 3. 테스트 케이스별로 채점 수행
    results = []
    all_correct = True
    for i, case in enumerate(test_cases):
        case_input = case["input"]
        expected_output = case["output"]
        case_result = {
            "case": i + 1,
            "input": case_input,
            "expected": expected_output
        }

        try:
            actual_output = student_function(*case_input)
            case_result["actual"] = actual_output

            if actual_output == expected_output:
                case_result["result"] = "O"
            else:
                case_result["result"] = "X"
                all_correct = False
        except Exception:
            case_result["result"] = "X"
            case_result["reason"] = "Runtime Error"
            case_result["details"] = traceback.format_exc()
            all_correct = False
            
        results.append(case_result)

    # 4. 최종 결과 종합하여 반환
    return {
        "overall_result": "O" if all_correct else "X",
        "results": results
    }
    
'''
테스트하는법
1. functions-framework --target=grade_code --debug: 로컬 환경에 임시적으로 서버를 여는것
2. 다음 코드를 bash 쉘에 넣어 실행. 
curl -X POST "http://localhost:8080" \
-H "Content-Type: application/json" \
-d '{
    "code": "def get_square(x):\n    return x * x",
    "function_name": "get_square",
    "test_cases": [
        {"input": [3], "output": 9},
        {"input": [-2], "output": 4}
    ]
}'

'''