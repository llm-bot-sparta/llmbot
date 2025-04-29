def build_grading_prompt(question: str, model_answer: str, student_answer: str, idx: int) -> str:
    return f"""
다음은 문항 {idx+1}입니다.

문제:
{question}

모범 답안:
{model_answer}

학생 답안:
{student_answer}

학생 답안이 문제 요구사항과 모범 답안을 얼마나 잘 충족하는지 평가해주세요.

- 10점 만점 기준으로 점수를 매겨주세요.
- 간단하고 명확한 피드백을 작성해주세요.

형식:
점수: /10
피드백:
"""
