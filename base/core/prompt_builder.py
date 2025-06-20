import importlib

def build_grading_prompt(category, question, model_answer, student_answer, evaluation_criteria, query_status=None, error_message=None):
    grading_criteria_str = ""
    if category == "SQL":
        # core.grading_sql 모듈에서 GRADING_SCHEME 불러오기
        module = importlib.import_module("core.grading_sql")
        grading_scheme = module.GRADING_SCHEME
        grading_criteria_str = "[채점 기준]\n"
        for item in grading_scheme:
            grading_criteria_str += f"- {item['name']}({item['score']}점): {item['description']}\n"
        
        # 오류가 발생한 경우에도 채점 기준은 동일하게, 피드백 마지막에 쿼리 문법적 오류 분석 추가
        error_analysis_section = ""
        if query_status in ['error', 'empty', 'no_answer']:
            error_analysis_section = f"\n[쿼리 문법적 오류 분석]\n- 실제 오류 메시지: {error_message if error_message else '없음'}\n- 오류 원인 해설 및 수정 제안: (구체적으로 작성)"
        
        prompt = f"""
당신은 {category} 과제 채점 전문가입니다.

- 문제: {question}
- 모범답안: {model_answer}
- 학생답안: {student_answer}
- 평가기준: {evaluation_criteria}
- 쿼리 상태: {query_status}
{grading_criteria_str}
학생의 답안이 모범답안과 다르더라도, 논리적/문법적 오류가 없다면 높은 점수를 주세요.
아래 조건을 꼭 지켜서 평가해 주세요.

1. 각 평가기준(정확도, 가독성, 효율성, 분석력 등)에 대해 **5점 단위(0, 5, 10, ..., 100)로만** 부분 점수를 각각 매겨주세요. (예: 정확도 50점, 가독성 20점, 효율성 15점)
2. 각 기준별 점수의 합이 100점이 되도록 최종 점수도 함께 출력해 주세요.
3. 각 평가기준별로 '참고할 점'을 한두 문장으로 구체적으로 작성해 주세요. (예: 잘한 점, 부족한 점, 개선점 등)
4. 마지막 피드백은 평가자가 참고할 수 있도록, 학생에게 직접 전달하는 친근한 말투가 아니라 틀린 부분, 부족한 점, 개선점 등 객관적이고 구체적인 정보 위주로 작성해 주세요.

결과는 아래 형식으로 출력해 주세요.

[기준별 점수]
정확도: 45 / 50
가독성: 15 / 20
효율성: 10 / 15
분석력: 10 / 15

[기준별 참고사항]
정확도: WHERE 조건에서 'Attrited Customer' 필터가 누락됨.
가독성: 쿼리 구조는 명확함.
효율성: CTE 활용이 부족함.

[최종 점수] 80
[피드백] 전반적으로 쿼리 구조는 명확하나, 일부 필터 조건과 효율성에서 아쉬움{error_analysis_section}
"""
    elif category == "python_basic":
        # core.grading_python_basic 모듈에서 GRADING_SCHEME 불러오기
        module = importlib.import_module("core.grading_python_basic")
        grading_scheme = module.GRADING_SCHEME
        grading_criteria_str = "[채점 기준]\n"
        for item in grading_scheme:
            grading_criteria_str += f"- {item['name']}({item['score']}점): {item['description']}\n"
        prompt = f"""
당신은 Python 기초 과제 채점 전문가입니다.

- 문제: {question}
- 모범답안: {model_answer}
- 학생답안: {student_answer}
- 평가기준: {evaluation_criteria}
{grading_criteria_str}
학생의 답안이 모범답안과 다르더라도, 논리적 오류가 없다면 높은 점수를 주세요.
아래 조건을 꼭 지켜서 평가해 주세요.

1. 각 평가기준(정확도, 가독성, 효율성, 분석력 등)에 대해 **5점 단위(0, 5, 10, ..., 100)로만** 부분 점수를 각각 매겨주세요.
2. 각 기준별 점수의 합이 100점이 되도록 최종 점수도 함께 출력해 주세요.
3. 각 평가기준별로 '참고할 점'을 한두 문장으로 구체적으로 작성해 주세요. (예: 잘한 점, 부족한 점, 개선점 등)
4. 마지막 피드백은 평가자가 참고할 수 있도록, 학생에게 직접 전달하는 친근한 말투가 아니라 틀린 부분, 부족한 점, 개선점 등 객관적이고 구체적인 정보 위주로 작성해 주세요.

결과는 아래 형식으로 출력해 주세요.

[기준별 점수]
정확도: 45 / 50
가독성: 15 / 20
효율성: 10 / 15
분석력: 10 / 15

[기준별 참고사항]
정확도: sum, len 함수 활용이 적절함.
가독성: 함수 구조가 명확함.
효율성: 불필요한 반복문 없음.

[최종 점수] 80
[피드백] 전반적으로 함수 구조와 내장 함수 활용이 적절하나, 일부 예외 처리에서 아쉬움이 있음.
"""
    else:
        prompt = ""
        # 추후 다른 문제 유형의 프롬프트 추가 가능
    
    return prompt
