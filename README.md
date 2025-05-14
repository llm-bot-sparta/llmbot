# LLM 스코 채점자동화 & 질문 답변
- 목적: 코딩 과제에 대한 답변에 대한 템플릿과 가이드라인을 제공하는 서비스
- 구조: Cloud run -> Gemini -> Streamlit 

## 환경
- Python 3.12.3

---
## 세팅 방법
- `pip install -r requirements.txt`
- `pip install --upgrade google-api-python-client`  # google 모듈 업그레이드가 필요한 경우가 있음

## 실행 방법
- 가상환경 진입
- main.py 실행 `streamlit run streamlit_app/main.py`

## Docker 배포 방법

- 

## 🗂️ 폴더별 설명

### 루트 디렉토리

| 항목 | 설명 |
|------|------|
| `.gitignore` | Git 추적 제외 대상 (venv, .env 등) |
| `README.md` | 프로젝트 소개 및 실행 가이드 |
| `Dockerfile` | 배포용 Docker 설정 파일 |
| `requirements.txt` | 필요한 Python 패키지 목록 |
| `.env.example` | 환경 변수 샘플 |

---

### `streamlit_app/` – 채점 웹앱

| 항목 | 설명 |
|------|------|
| `main.py` | Streamlit 앱 실행 진입점 |

---

###  `core/` – 채점 및 응답 핵심 로직

| 항목 | 설명 |
|------|------|
| `grader.py` | 과제 채점 로직 |
| `prompt_builder.py` | 프롬프트 생성 유틸 (프롬프트 변경시 수정) |

---

### `service/` – 외부 API 및 설정 관리

| 항목 | 설명 |
|------|------|
| `llm_client.py` | LLM API 호출 래퍼 (Gemini/OpenAI) |
| `config.py` | 환경 변수 로딩 |

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
