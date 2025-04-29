import streamlit as st
from core.grader import grade_single_question

st.title("🧠 Gemini 자동 채점기")

st.markdown("### 📚 문항 추가하기")
num_questions = st.number_input("추가할 문항 개수", min_value=1, max_value=10, value=1, step=1)

questions = []

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

if st.button("📝 채점 시작하기"):
    for idx, q in enumerate(questions):
        with st.spinner(f"문항 {idx+1} 채점 중..."):
            try:
                result = grade_single_question(q['question'], q['model_answer'], q['student_answer'], idx)
                st.markdown(f"### ✅ 문항 {idx+1} 채점 결과")
                st.success(result)
            except Exception as e:
                st.error(f"문항 {idx+1} 채점 실패: {e}")
