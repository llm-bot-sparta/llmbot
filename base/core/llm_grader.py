import re
from core.prompt_builder import build_grading_prompt
from external_service.llm_client import generate_content

def parse_gemini_response(response: str):
    """
    Gemini 응답에서 [점수], [최종 점수], [피드백]을 파싱하여 dict로 반환
    """
    score_match = re.search(r"\[(?:점수|최종 점수)\]\s*(\d+)", response)
    score = int(score_match.group(1)) if score_match else None

    feedback_match = re.search(r"\[피드백\](.*)", response, re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else response.strip()

    return {
        "score": score,
        "feedback": feedback
    }

def grade_single_question(category, question, model_answer, student_answer, evaluation_criteria, query_status=None, error_message=None):
    """
    Gemini(Google LLM)로 학생 답안을 평가하는 함수.
    프롬프트는 prompt_builder.py에서 관리하며, LLM의 응답을 dict(점수, 피드백 등)로 반환.
    """
    prompt = build_grading_prompt(category, question, model_answer, student_answer, evaluation_criteria, query_status=query_status, error_message=error_message)
    response = generate_content(prompt)
    return parse_gemini_response(response)
    # # 임시 예시
    # return {
    #     "score": 95,
    #     "feedback": "쿼리 작성이 전반적으로 매우 훌륭해요! WHERE 조건과 GROUP BY 사용도 잘했고, 결과 정렬까지 신경 쓴 점이 인상적입니다. 다음에는 쿼리 최적화도 한 번 더 고민해보면 더 좋을 것 같아요. 수고 많았어요!"
    # }