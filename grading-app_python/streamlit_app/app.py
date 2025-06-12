import streamlit as st
import requests
import pandas as pd # pandas 라이브러리 추가

# -----------------------------------------------------
# 문제 정보 및 채점 서버 설정
# -----------------------------------------------------

# 로컬에서 실행 중인 Cloud Function(채점 서버)의 주소
API_URL = "http://localhost:8080"

# 문제 1: 숫자 리스트의 평균 계산하기
PROBLEM_INFO = {
    "title": "문제 1: 숫자 리스트의 평균 계산하기",
    "description": """
    한 소매점에서 재고를 계산해야 합니다. 주어진 재고 리스트의 평균을 계산해보세요.
    - 함수명은 반드시 `calculate_stock` 이어야 합니다.
    - 숫자(int 또는 float)로 이루어진 리스트(list)를 인자로 받습니다.
    - 평균값(float)을 반환해야 합니다.
    """,
    "function_name": "calculate_stock",
    "test_cases": [
        {"input": [[10, 20, 30, 40, 50]], "output": 30.0}
    ],
    "placeholder_code": "def calculate_stock(numbers):\n    # 이 곳에 코드를 작성하세요\n    # 예: return sum(numbers) / len(numbers)\n    return"
}


# -----------------------------------------------------
# Streamlit UI 구성
# -----------------------------------------------------

st.title(PROBLEM_INFO["title"])
st.markdown(PROBLEM_INFO["description"])
st.code(f"함수 이름: {PROBLEM_INFO['function_name']}\n테스트 케이스 개수: {len(PROBLEM_INFO['test_cases'])}개", language="text")

student_code = st.text_area(
    "코드를 여기에 입력하세요:",
    height=200,
    placeholder=PROBLEM_INFO["placeholder_code"]
)

if st.button("코드 제출 및 채점하기"):
    if not student_code.strip():
        st.warning("코드를 입력해주세요.")
    else:
        with st.spinner("채점 중입니다..."):
            try:
                payload = {
                    "code": student_code,
                    "function_name": PROBLEM_INFO["function_name"],
                    "test_cases": PROBLEM_INFO["test_cases"]
                }
                
                response = requests.post(API_URL, json=payload, timeout=15)
                response.raise_for_status()
                
                result = response.json()

                if result.get("overall_result") == "O":
                    st.success("🎉 정답입니다! 모든 테스트 케이스를 통과했습니다.")
                else:
                    st.error("😥 오답입니다. 아래 상세 결과를 확인하세요.")

                # ----- [결과 표시 로직 변경] -----
                st.subheader("채점 상세 결과")
                
                # 1. API 응답에서 'results' 리스트를 가져와 DataFrame으로 변환
                results_list = result.get('results', [])
                if results_list:
                    df = pd.DataFrame(results_list)

                    # 2. 'result' 열의 값을 O, X 이모지로 변환하여 '결과' 열 생성
                    df['결과'] = df['result'].apply(lambda x: '⭕' if x == 'O' else '❌')
                    
                    # 런타임 에러가 발생했을 때 'actual' 값이 없을 수 있으므로 처리
                    if 'actual' not in df.columns:
                        df['actual'] = "Error"
                    
                    # 3. 사용자에게 보여줄 열만 선택하고, 보기 좋게 이름 변경
                    display_df = df[['결과', 'case', 'input', 'expected', 'actual']].rename(
                        columns={
                            'case': '테스트 케이스',
                            'input': '입력값',
                            'expected': '기댓값',
                            'actual': '실제 반환값'
                        }
                    )
                    
                    # 4. st.dataframe으로 깔끔한 표 표시
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.write("채점 결과를 표시할 수 없습니다.")
                # ----- [여기까지 변경] -----

            except requests.exceptions.RequestException as e:
                st.error(f"채점 서버에 연결할 수 없습니다. 로컬 서버(main.py)가 실행 중인지 확인해주세요.\n오류: {e}")