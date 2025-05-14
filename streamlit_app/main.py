import sys
import os
import pandas as pd
# 경로 추가 (모듈 import용)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.grader import grade_single_question

import streamlit as st
import re



st.set_page_config(page_title="Gemini 자동 채점기", layout="wide")
st.title("🔥 과제 자동 채점기")

# ✅ 과제명 / 학생명 입력
assignment_title = st.text_input("📘 과제명")
student_name = st.text_input("👤 학생 이름")

# ✅ 문항 개수
st.markdown("### 📚 문항 추가하기")
num_questions = st.number_input("문항 개수", min_value=1, max_value=10, value=1)

questions = []
results = []

# ✅ 문항 입력
for i in range(num_questions):
    st.markdown(f"---\n### 문항 {i+1}")
    question = st.text_area(f"문제 {i+1}", key=f"question_{i}")
    model_answer = st.text_area(f"모범 답안 {i+1}", key=f"model_answer_{i}")
    student_answer = st.text_area(f"학생 답안 {i+1}", key=f"student_answer_{i}")
    questions.append({
        "question": question,
        "model_answer": model_answer,
        "student_answer": student_answer
    })

# ✅ 채점 버튼
if st.button("📝 채점 시작하기"):
    if not assignment_title or not student_name:
        st.warning("⚠️ 과제명과 학생명을 모두 입력해주세요.")
    else:
        for idx, q in enumerate(questions):
            with st.spinner(f"문항 {idx+1} 채점 중..."):
                try:
                    result_text = grade_single_question(q['question'], q['model_answer'], q['student_answer'], idx)
                    st.markdown(f"### ✅ 문항 {idx+1} 채점 결과")
                    st.success(result_text)

                    # 결과 파싱
                    match_understanding = re.search(r"\[이해도 평가\]\s*(상|중|하)", result_text)
                    match_feedback = re.search(r"\[피드백\](.*)", result_text, re.DOTALL)

                    understanding = match_understanding.group(1) if match_understanding else "정보 없음"
                    feedback = match_feedback.group(1).strip() if match_feedback else "피드백 없음"

                    results.append({
                        "과제명": assignment_title,
                        "학생명": student_name,
                        "문항 번호": f"문항 {idx+1}",
                        "이해도 평가": understanding,
                        "피드백": feedback
                    })

                except Exception as e:
                    st.error(f"문항 {idx+1} 채점 실패: {e}")

# ✅ CSV 다운로드
if results:
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.markdown("---")
    st.download_button(
        label="📥 채점 결과 CSV 다운로드",
        data=csv,
        file_name=f"{assignment_title}_{student_name}_grading_results.csv",
        mime="text/csv"
    )
