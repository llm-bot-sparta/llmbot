from core.prompt_builder import build_grading_prompt
from service.llm_client import generate_content

def grade_single_question(question: str, model_answer: str, student_answer: str, idx: int) -> str:
    prompt = build_grading_prompt(question, model_answer, student_answer, idx)
    return generate_content(prompt)