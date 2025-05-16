import sys
import os
import pandas as pd
# 경로 추가 (모듈 import용)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.grader import grade_single_question
from core.mysql_engine import setup_database, check_query_result, mysql_engine
from sqlalchemy import text

import streamlit as st
import re
from datetime import datetime
from questions import QUESTIONS

def save_feedback_to_csv(assignment_type, student_name, tutor_name, results):
    """
    모든 문제의 피드백을 하나의 CSV 파일로 저장하는 함수
    
    Args:
        assignment_type (str): 과제 카테고리 (예: SQL, Python기초)
        student_name (str): 학생 이름
        tutor_name (str): 튜터 이름
        results (list): 각 문제별 결과를 담은 리스트
    """
    # 피드백 저장 디렉토리 생성
    os.makedirs('data/feedback', exist_ok=True)
    
    # CSV 파일명 생성 (과제카테고리_학생명_날짜.csv)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'data/feedback/{assignment_type}_{student_name}_{timestamp}.csv'
    
    # DataFrame 생성 및 CSV 저장
    df = pd.DataFrame(results)
    df['튜터명'] = tutor_name  # 튜터 이름 컬럼 추가
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    return csv_filename

def main():
    st.title("🔥 과제 자동 채점기")
    
    # 사이드바: 과제 선택, 학생명 직접 입력
    with st.sidebar:
        assignment_type = st.selectbox("과제 선택", list(QUESTIONS.keys()), index=0)
        student_name = st.text_input("학생 이름을 입력하세요")
        
        # 튜터 선택 드롭다운
        tutor_list = ["임정", "곽승예", "신한결", "원유선", "김대명", "허진성", "권현진", "김연준", "기타"]
        selected_tutor = st.selectbox("튜터 선택", tutor_list)
        
        # 기타 선택 시 직접 입력
        if selected_tutor == "기타":
            tutor_name = st.text_input("튜터 이름을 직접 입력하세요")
        else:
            tutor_name = selected_tutor
    
    # 메인 화면: 카테고리별 전체 문제 한 번에 표시
    if assignment_type:
        if len(QUESTIONS[assignment_type]) == 0:
            st.info(f"'{assignment_type}' 카테고리에는 아직 등록된 문제가 없습니다.")
        else:
            st.header(f"[{assignment_type}] 전체 문항 답안 입력 및 채점")
            answer_inputs = {}
            for qid, q in QUESTIONS[assignment_type].items():
                st.markdown(f"---\n#### {qid}. {q['title']}")
                st.markdown(q['content'])
                answer_inputs[qid] = st.text_area(f"학생 답변 입력 ({qid})", key=f"answer_{qid}", height=120)
                with st.expander(f"평가 기준 보기 ({qid})"):
                    for criteria in q["evaluation_criteria"]:
                        st.write(f"**{criteria['description']}** (가중치: {criteria['weight']})")
                        for check_point in criteria["check_points"]:
                            st.write(f"- {check_point}")
            
            # 채점 버튼
            if st.button("전체 문항 채점하기"):
                if not student_name:
                    st.warning("학생 이름을 입력해야 채점할 수 있습니다.")
                    return
                
                if not tutor_name:
                    st.warning("튜터 이름을 입력해야 채점할 수 있습니다.")
                    return
                
                st.subheader("채점 결과")
                results = []  # 모든 문제의 결과를 저장할 리스트
                
                # SQL 과제인 경우 MySQL 엔진을 통한 채점
                if assignment_type == "SQL":
                    # 데이터베이스 설정
                    if not setup_database():
                        st.error("데이터베이스 설정에 실패했습니다.")
                        return
                    
                    # 학생 답변 수집
                    student_queries = []
                    for qid in sorted(answer_inputs.keys()):
                        query = answer_inputs[qid].strip()
                        student_queries.append(query)
                    
                    # 쿼리 실행 및 결과 확인
                    check_query_result(student_queries)
                    
                    # 결과 표시
                    st.markdown("### SQL 쿼리 채점 결과")
                    for qid, query in enumerate(student_queries, 1):
                        question_key = f'SQL_{qid:03d}'
                        q = QUESTIONS[assignment_type][question_key]
                        
                        if not query:
                            st.markdown(f"**{qid}. {q['title']}**: ❌ (답변 없음)")
                            results.append({
                                '과제카테고리': assignment_type,
                                '학생명': student_name,
                                '튜터명': tutor_name,
                                '질문번호': qid,
                                '질문제목': q['title'],
                                '학생답안': query,
                                '점수': '0',
                                '피드백': '답변이 입력되지 않았습니다.',
                                '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                        else:
                            try:
                                with mysql_engine.connect() as conn:
                                    result_df = pd.read_sql_query(text(query), conn)
                                answer_file = os.path.join('answer', f'sql_q{qid}.csv')
                                if os.path.exists(answer_file):
                                    answer_df = pd.read_csv(answer_file)
                                    result_sorted = result_df.sort_values(by=result_df.columns.tolist()).reset_index(drop=True)
                                    answer_sorted = answer_df.sort_values(by=answer_df.columns.tolist()).reset_index(drop=True)
                                    is_correct = result_sorted.equals(answer_sorted)
                                    
                                    # Gemini LLM을 통한 평가
                                    feedback = grade_single_question(
                                        assignment_type,
                                        q['content'],
                                        q['model_answer'],
                                        query,
                                        q['evaluation_criteria']
                                    )
                                    
                                    st.markdown(f"**{qid}. {q['title']}**")
                                    # SQL 엔진 채점 결과 표시
                                    st.markdown(f"**SQL 채점 결과**: {'⭕' if is_correct else '❌'}")
                                    
                                    # 학생 쿼리 결과와 정답을 세로로 표시
                                    st.markdown("**학생 쿼리 결과**")
                                    st.dataframe(result_df)
                                    
                                    st.markdown("**정답**")
                                    st.dataframe(answer_df)
                                    
                                    # LLM 평가 결과 표시
                                    if isinstance(feedback, dict):
                                        st.write(f"**점수:** {feedback.get('score', 'N/A')}")
                                        st.write(f"**피드백:** {feedback.get('feedback', '')}")
                                        
                                        results.append({
                                            '과제카테고리': assignment_type,
                                            '학생명': student_name,
                                            '튜터명': tutor_name,
                                            '질문번호': qid,
                                            '질문제목': q['title'],
                                            '학생답안': query,
                                            'SQL_결과': 'O' if is_correct else 'X',
                                            '점수': feedback.get('score', 'N/A'),
                                            '피드백': feedback.get('feedback', ''),
                                            '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        })
                                    else:
                                        st.write(feedback)
                                        results.append({
                                            '과제카테고리': assignment_type,
                                            '학생명': student_name,
                                            '튜터명': tutor_name,
                                            '질문번호': qid,
                                            '질문제목': q['title'],
                                            '학생답안': query,
                                            'SQL_결과': 'O' if is_correct else 'X',
                                            '점수': '0',
                                            '피드백': str(feedback),
                                            '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        })
                            except Exception as e:
                                st.markdown(f"**{qid}. {q['title']}**: ❌ (에러: {str(e)})")
                                st.write(f"**SQL 채점 결과**: ❌")
                                st.write(f"**점수**: 0")
                                st.write(f"**피드백**: 에러가 발생했습니다: {str(e)}")
                                results.append({
                                    '과제카테고리': assignment_type,
                                    '학생명': student_name,
                                    '튜터명': tutor_name,
                                    '질문번호': qid,
                                    '질문제목': q['title'],
                                    '학생답안': query,
                                    'SQL_결과': 'X',
                                    '점수': '0',
                                    '피드백': f'에러 발생: {str(e)}',
                                    '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                })
                else:
                    # 기존 Gemini LLM을 통한 평가
                    for qid, q in QUESTIONS[assignment_type].items():
                        answer = answer_inputs[qid]
                        if not answer:
                            st.markdown(f"**{qid}. {q['title']}**: ❌ (답변 없음)")
                            st.write(f"**SQL 채점 결과**: ❌")
                            st.write(f"**점수**: 0")
                            st.write(f"**피드백**: 답변이 입력되지 않았습니다.")
                            results.append({
                                '과제카테고리': assignment_type,
                                '학생명': student_name,
                                '튜터명': tutor_name,
                                '질문번호': qid,
                                '질문제목': q['title'],
                                '학생답안': answer,
                                'SQL_결과': 'X',
                                '점수': '0',
                                '피드백': '답변이 입력되지 않았습니다.',
                                '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            continue
                            
                        feedback = grade_single_question(
                            assignment_type,
                            q['content'],
                            q['model_answer'],
                            answer,
                            q['evaluation_criteria']
                        )
                        
                        st.markdown(f"**{qid}. {q['title']}**")
                        st.write(f"**SQL 채점 결과**: ❌")  # SQL이 아닌 과제는 항상 X
                        
                        if isinstance(feedback, dict):
                            st.write(f"**점수:** {feedback.get('score', 'N/A')}")
                            st.write(f"**피드백:** {feedback.get('feedback', '')}")
                            
                            results.append({
                                '과제카테고리': assignment_type,
                                '학생명': student_name,
                                '튜터명': tutor_name,
                                '질문번호': qid,
                                '질문제목': q['title'],
                                '학생답안': answer,
                                'SQL_결과': 'X',
                                '점수': feedback.get('score', 'N/A'),
                                '피드백': feedback.get('feedback', ''),
                                '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                        else:
                            st.write(feedback)
                            results.append({
                                '과제카테고리': assignment_type,
                                '학생명': student_name,
                                '튜터명': tutor_name,
                                '질문번호': qid,
                                '질문제목': q['title'],
                                '학생답안': answer,
                                'SQL_결과': 'X',
                                '점수': '0',
                                '피드백': str(feedback),
                                '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                
                # 모든 결과를 하나의 CSV 파일로 저장
                if results:
                    csv_filename = save_feedback_to_csv(assignment_type, student_name, tutor_name, results)
                    st.success(f"모든 평가 결과가 저장되었습니다! (파일: {csv_filename})")
                    
                    # CSV 파일 다운로드 버튼
                    with open(csv_filename, 'rb') as f:
                        st.download_button(
                            label="📥 CSV 파일 다운로드",
                            data=f,
                            file_name=os.path.basename(csv_filename),
                            mime="text/csv"
                        )

if __name__ == "__main__":
    main()
