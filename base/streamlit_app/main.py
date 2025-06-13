import sys
import os
import pandas as pd
# 경로 추가 (모듈 import용)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.grader import grade_single_question
from service.mysql_engine import setup_database, check_query_result, mysql_engine
from sqlalchemy import text

import streamlit as st
import re
from datetime import datetime
from questions import QUESTIONS
import importlib  # 동적 import를 위해 추가

def get_grading_scheme(assignment_type):
    if assignment_type == "SQL":
        module = importlib.import_module("streamlit_app.grading_schemes.grading_sql")
        return getattr(module, "GRADING_SCHEME", [])
    elif assignment_type == "Python기초":
        module = importlib.import_module("streamlit_app.grading_schemes.grading_python_basic")
        return getattr(module, "GRADING_SCHEME", [])
    # 추후 다른 과제 유형 추가 가능
    return []

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

def load_student_data(round_str):
    """회차별 학생 데이터를 로드하는 함수"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    csv_path = os.path.join(project_root, f'data/{round_str}/data_{round_str}_student.csv')
    
    df = pd.read_csv(csv_path)
    return sorted(df['student'].dropna().tolist())

def load_tutor_data(round_str):
    """회차별 튜터 데이터를 로드하는 함수"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    csv_path = os.path.join(project_root, f'data/{round_str}/data_{round_str}_tutor.csv')
    
    df = pd.read_csv(csv_path)
    return sorted(df['tutor'].dropna().tolist())

def main():
    st.title("🔥 과제 자동 채점기")
    
    # 사이드바: 회차 선택, 과제 선택, 학생명 직접 입력
    with st.sidebar:
        # 과제 회차 선택
        round_options = ['7th']  # 필요시 확장
        selected_round = st.selectbox("과제 회차 선택", round_options, index=0)
        
        # 변수 초기화
        assignment_type = "(선택)"
        student_name = None
        tutor_name = None
        
        # 회차에 따른 학생/튜터 데이터 로드
        student_list = load_student_data(selected_round)
        tutor_list = load_tutor_data(selected_round)
        
        # 과제 선택 (SQL을 기본값으로)
        assignment_options = ["(선택)"] + list(QUESTIONS.keys())
        sql_index = assignment_options.index('SQL') if 'SQL' in assignment_options else 1
        assignment_type = st.selectbox("과제 선택", assignment_options, index=sql_index)
        
        # 과제가 선택된 경우에만 학생/튜터 선택 표시
        if assignment_type != "(선택)":
            # 학생 선택 드롭다운 (기타 옵션 추가)
            student_list_with_other = ["(선택)"] + student_list + ["기타"]
            selected_student = st.selectbox("학생 선택", student_list_with_other, index=0)
            
            # 기타 선택 시 학생 이름 직접 입력
            if selected_student == "기타":
                student_name = st.text_input("학생 이름을 직접 입력하세요")
            elif selected_student == "(선택)":
                student_name = None
            else:
                student_name = selected_student
            
            # 튜터 선택 드롭다운
            tutor_list_with_other = ["(선택)"] + tutor_list + ["기타"]
            selected_tutor = st.selectbox("튜터 선택", tutor_list_with_other, index=0)
            
            # 기타 선택 시 직접 입력
            if selected_tutor == "기타":
                tutor_name = st.text_input("튜터 이름을 직접 입력하세요")
            elif selected_tutor == "(선택)":
                tutor_name = None
            else:
                tutor_name = selected_tutor
                
            # 선택된 학생-튜터 정보 표시
            if student_name and tutor_name:
                st.info(f"📌 {student_name} 학생의 담당 튜터: {tutor_name}")
    
    # 메인 화면: 과제가 선택된 경우에만 문제 표시
    if assignment_type != "(선택)":
        if len(QUESTIONS[assignment_type]) == 0:
            st.info(f"'{assignment_type}' 카테고리에는 아직 등록된 문제가 없습니다.")
        else:
            st.header(f"[{assignment_type}] 전체 문항 답안 입력 및 채점")
            answer_inputs = {}
            for qid, q in QUESTIONS[assignment_type].items():
                st.markdown(f"---\n#### {qid}. {q['title']}")
                st.markdown(q['content'], unsafe_allow_html=True)
                answer_inputs[qid] = st.text_area(
                    f"학생 답변 입력 ({qid})",
                    key=f"answer_{qid}",
                    height=240  # 기존 120에서 2배로 증가
                )
                with st.expander(f"평가 기준 보기 ({qid})"):
                    st.markdown("**문제별 요구 체크리스트**")
                    for criteria in q["evaluation_criteria"]:
                        st.write(f"- {criteria['description']}")
                    grading_scheme = get_grading_scheme(assignment_type)
                    if grading_scheme:
                        st.markdown("**공통 채점 기준 (총 100점)**")
                        for scheme in grading_scheme:
                            st.write(f"- {scheme['name']} ({scheme['score']}점): {scheme['description']}")
                    # 정답 코드도 함께 표시
                    st.markdown("**정답 코드**")
                    st.code(q["model_answer"], language="python")
            
            # 채점 버튼
            if st.button("전체 문항 채점하기"):
                if not student_name:
                    st.warning("학생을 선택해주세요.")
                    return
                
                if not tutor_name:
                    st.warning("튜터를 선택해주세요.")
                    return
                
                st.subheader("채점 결과")
                results = []

                if assignment_type == "SQL":
                    # SQL 과제인 경우 MySQL 엔진을 통한 채점
                    # answer_dir을 회차+과제유형 조합으로 생성
                    answer_dir = f"answer/{selected_round}_{assignment_type}/"
                    print(answer_dir)
                    
                    # 데이터베이스 초기화
                    if not setup_database(answer_dir):
                        st.error("데이터베이스 초기화에 실패했습니다.")
                        return
                    
                    # 데이터베이스 연결 확인
                    try:
                        with mysql_engine.connect() as conn:
                            conn.execute(text("SELECT 1"))
                    except Exception as e:
                        st.error("데이터베이스 연결에 실패했습니다.")
                        return
                    
                    # 학생 답변 수집
                    student_queries = [answer_inputs[qid].strip().replace('BankChurners', 'bankchurners') for qid in sorted(answer_inputs.keys())]
                    # 전체 쿼리 한 번에 채점
                    check_results = check_query_result(student_queries, answer_dir)
                    # 디버깅용 출력 추가
                    print('check_results:', check_results)
                    print('각 튜플 길이:', [len(x) for x in check_results])
                    print('answer_inputs.keys:', list(answer_inputs.keys()))
                    print('student_queries:', student_queries)
                    # 결과 표시
                    st.markdown("### SQL 쿼리 채점 결과")
                    grading_scheme = get_grading_scheme(assignment_type)
                    for idx, qid in enumerate(sorted(answer_inputs.keys())):
                        query = answer_inputs[qid].strip()
                        q = QUESTIONS[assignment_type][qid]
                        # check_query_result의 반환값이 리스트라고 가정 (question_id, is_correct, result_df, answer_df, status, error_message)
                        if check_results and idx < len(check_results):
                            question_id, is_correct, result_df, answer_df, status, error_message = check_results[idx]
                        else:
                            question_id, is_correct, result_df, answer_df, status, error_message = None, False, None, None, 'mismatch', None
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
                                st.markdown(f"**{qid}. {q['title']}**")
                                # 상태에 따른 아이콘과 메시지 표시
                                status_icon = {
                                    'exact_match': '⭕',
                                    'close_match': '❗️',
                                    'exact_match_colname_warning': '⭕',
                                    'close_match_colname_warning': '❗️',
                                    'mismatch': '❌',
                                    'empty': '❌',
                                    'no_answer': '❌',
                                    'error': '❌'
                                }
                                status_message = {
                                    'exact_match': '정답',
                                    'close_match': '확인 필요 (근사치 일치)',
                                    'exact_match_colname_warning': '정답 (컬럼명 다름)',
                                    'close_match_colname_warning': '확인 필요 (컬럼명 다름, 값은 근사치 일치)',
                                    'mismatch': '오답',
                                    'empty': '답변 없음',
                                    'no_answer': '정답 파일 없음',
                                    'error': '에러 발생'
                                }
                                status = check_results[idx][4] if check_results and idx < len(check_results) else 'mismatch'
                                st.markdown(f"**SQL 채점 결과**: {status_icon[status]} ({status_message[status]})")
                                if result_df is not None:
                                    st.markdown("**학생 쿼리 결과**")
                                    st.dataframe(result_df)
                                if answer_df is not None:
                                    st.markdown("**정답**")
                                    st.dataframe(answer_df)
                                # 쿼리 실행 결과에 따른 피드백 분기
                                if status in ['error', 'empty', 'no_answer']:
                                    # LLM 호출 없이 오류 메시지만 피드백으로 사용
                                    score = 0
                                    fb_text = f"[SQL 오류]\n{error_message if error_message else '쿼리 실행에 실패했습니다.'}"
                                else:
                                    # 정상 실행 시 LLM 호출
                                    feedback = grade_single_question(
                                        assignment_type,
                                        q['content'],
                                        q['model_answer'],
                                        query,
                                        q['evaluation_criteria'],
                                        query_status=status
                                    )
                                    score = feedback.get('score') if isinstance(feedback, dict) else 0
                                    fb_text = feedback.get('feedback', '') if isinstance(feedback, dict) else str(feedback)
                                st.write(f"**점수:** {score}")
                                st.write(f"**피드백:** {fb_text}")
                                # SQL_결과 상태 결정
                                if status.startswith('exact_match'):
                                    sql_result = 'O'
                                elif status.startswith('close_match'):
                                    sql_result = '△'
                                else:
                                    sql_result = 'X'
                                results.append({
                                    '과제카테고리': assignment_type,
                                    '학생명': student_name,
                                    '튜터명': tutor_name,
                                    '질문번호': qid,
                                    '질문제목': q['title'],
                                    '학생답안': query,
                                    'SQL_결과': sql_result,
                                    '점수': score,
                                    '피드백': fb_text,
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
                elif assignment_type == "Python기초":
                    from service.cloud_function_client import call_python_grader
                    from service.local_grader import execute_python_code, display_test_results
                    from core.grader import grade_single_question
                    
                    # 로컬 개발 환경인지 확인
                    is_local = "streamlit" in sys.modules and not os.getenv("K_SERVICE")
                    if is_local:
                        st.info("로컬 환경에서 실행 중입니다.")
                    
                    # 문제별 채점 결과를 저장할 딕셔너리
                    grading_results = {}
                    
                    for qid, q in QUESTIONS[assignment_type].items():
                        student_code = answer_inputs[qid]
                        function_name = q.get("function_name")
                        test_cases = q.get("test_cases")
                        
                        if not student_code:
                            st.warning(f"문제 {qid}에 대한 답변이 입력되지 않았습니다.")
                            grading_results[qid] = {
                                "score": 0,
                                "feedback": "답변이 입력되지 않았습니다.",
                                "status": "empty"
                            }
                            continue
                        
                        try:
                            # 코드 실행 및 결과 받기
                            grading_result = execute_python_code(student_code, function_name, test_cases) if is_local else \
                                            call_python_grader(student_code, function_name, test_cases)
                            
                            if "error" in grading_result:
                                st.error(grading_result["error"])
                                grading_results[qid] = {
                                    "score": 0,
                                    "feedback": f"실행 오류: {grading_result['error']}",
                                    "status": "error"
                                }
                            else:
                                # 실행 결과 표시
                                if "output" in grading_result:
                                    st.markdown(f"### 문제 {qid} 실행 결과")
                                    if is_local:
                                        display_test_results(grading_result["output"])
                                    else:
                                        st.code(str(grading_result["output"]))
                                
                                # LLM을 통한 피드백 생성
                                llm_feedback = grade_single_question(
                                    category="python_basic",
                                    question=q.get("question"),
                                    model_answer=q.get("model_answer"),
                                    student_answer=student_code,
                                    evaluation_criteria=q.get("evaluation_criteria"),
                                    query_status="success" if "output" in grading_result else "error",
                                    error_message=grading_result.get("error")
                                )
                                
                                # LLM 피드백 표시
                                st.write(f"**점수**: {llm_feedback.get('score')}점")
                                st.write(f"**피드백**: {llm_feedback.get('feedback')}")
                                st.markdown("---")
                                
                                # 채점 결과 저장
                                grading_results[qid] = {
                                    "score": llm_feedback.get('score', 0),
                                    "feedback": llm_feedback.get('feedback', ''),
                                    "status": "success"
                                }
                                
                                # 결과 저장
                                results.append({
                                    '과제카테고리': assignment_type,
                                    '학생명': student_name,
                                    '튜터명': tutor_name,
                                    '질문번호': qid,
                                    '질문제목': q['title'],
                                    '학생답안': student_code,
                                    '점수': str(llm_feedback.get('score', 0)),
                                    '피드백': llm_feedback.get('feedback', ''),
                                    '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                })
                                
                        except Exception as e:
                            st.error(f"문제 {qid} 채점 중 오류 발생: {str(e)}")
                            st.exception(e)  # 전체 에러 트레이스백 표시
                            grading_results[qid] = {
                                "score": 0,
                                "feedback": f"채점 중 오류 발생: {str(e)}",
                                "status": "error"
                            }
                            results.append({
                                '과제카테고리': assignment_type,
                                '학생명': student_name,
                                '튜터명': tutor_name,
                                '질문번호': qid,
                                '질문제목': q['title'],
                                '학생답안': student_code,
                                '점수': '0',
                                '피드백': f'채점 중 오류 발생: {str(e)}',
                                '채점시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                    
                    # 문제별 상세 결과 표시
                    st.markdown("---")
                    st.markdown("## 채점 결과 요약")
                    for qid, result in grading_results.items():
                        with st.expander(f"문제 {qid} ({result['score']}점)"):
                            st.write(f"상태: {'성공' if result['status'] == 'success' else '오류'}")
                            st.write("피드백:")
                            st.write(result['feedback'])
                    
                    # 결과 저장
                    if st.button("채점 결과 저장"):
                        try:
                            # 결과 저장 로직 (예: DB에 저장)
                            st.success("채점 결과가 저장되었습니다.")
                        except Exception as e:
                            st.error(f"결과 저장 중 오류 발생: {str(e)}")
                else:
                    # (필요하다면 다른 과제 유형 처리)
                    pass
                
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