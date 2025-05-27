# LLM 스코 채점자동화 & 질문 답변

## 일반 개요
- 목적: 코딩 과제에 대한 답변에 대한 템플릿과 가이드라인을 제공하는 서비스
- 구조: Cloud run -> Gemini -> Streamlit
- 환경: Python 3.12.3 
- 작동방식
    - 웹 사이트에는 특정 과제에 대한 모범답안, 채점가이드 등이 사전 Prompting 되어있음
    - 튜터들은 각 학생의 제출코드를 제출하여 채점하기를 클릭
    - LLM 봇은 모범답안과 제출코드를 비교하여 채점가이드를 출력
    - (SQL) 학생들의 제출코드는 빅쿼리에 있는 데이터에 실행되어 결과가 출력되며 이는 정답과 비교하여 True/False를 반환

---
## 세팅 방법
- `pip install -r requirements.txt`
- `pip install --upgrade google-api-python-client`  # google 모듈 업그레이드가 필요한 경우가 있음

## 실행 방법
- 가상환경 진입
- main.py 실행 `streamlit run streamlit_app/main.py`


## 채점 사전 준비(승예, 정)
- 정답코드를 사전에 생성
- 정답 코드를 미리 실행하여 answer/{과제명}.txt에 문제 갯 수 만큼(ex 6개) 정답 업로드
- 향후 채점 실행 시 학생들의 제출 코드를 실행하여 그 결과가 answer/{과제명}.txt와 일치하는 지 확인

## Docker 배포 방법
- 승예님 작성 필요

## 🗂️ 폴더별 설명

### 루트 디렉토리

| 항목 | 설명 |
|------|------|
| `.gitignore` | Git 추적 제외 대상 (venv, .env 등) |
| `README.md` | 프로젝트 소개 및 실행 가이드 |
| `Dockerfile` | 배포용 Docker 설정 파일 |
| `requirements.txt` | 필요한 Python 패키지 목록 |
| `.env.example` | 환경 변수 샘플 |
| `credentials` | Bigquery 연결을 위한 서비스 계정의 json key 저장소, 파일은 노션 확인|
---

### `streamlit_app/` – 채점 웹앱

| 항목 | 설명 |
|------|------|
| `main.py` | Streamlit 앱 실행 진입점 |
| `question.py` |   |

---

###  `core/` – 채점 및 응답 핵심 로직

| 항목 | 설명 |
|------|------|
| `__init__py` | 처음 실행되는 스크립트로, 디렉토리 안의 코드가 실행되는 작업디렉토리를 루트로 설정 |
| `grader.py` | 과제 채점 로직 |

| `prompt_builder.py` | 프롬프트 생성 유틸 (프롬프트 변경시 수정) |

---

### `service/` – 외부 API 및 설정 관리

| 항목 | 설명 |
|------|------|
| `llm_client.py` | LLM API 호출 래퍼 (Gemini/OpenAI) |
| `config.py` | 환경 변수 로딩 |
| `mysql_engine.py` | mysql 연결하고 채점하는 스크립트, 추후 main.py가 참조하여 사용 |

---

### `experiments/` – 실험 공간

| 항목 | 설명 |
|------|------|
| `prompt_tests.ipynb` | 프롬프트 테스트용 노트북 |

---

### `scripts/` – 보조 스크립트

| 항목 | 설명 |
|------|------|
| `format_converter.py` | 제출 파일 포맷 변환 도구 등 |

---

### `tests/` – 테스트 코드

| 항목 | 설명 |
|------|------|
| `test_grader.py` | 핵심 모듈 유닛 테스트 (채점 중심) |

---

### `deprecated/` – 당장은 필요없는 코드

| 항목 | 설명 |
|------|------|
| `bq_engine` | SQL 과제 채점을 위해 BigQuery에 SQL을 날리는 코드였으나, MySQL 환경이여서 deprecated됨 |
| `generate_answer.py` | SQL 과제 채점을 위해서 정답 테이블을 bg_engine을 이용해 만드는 코드입니다. |