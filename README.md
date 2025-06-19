# LLM 채점 서비스
```
- 독자를 위한 Heading 머릿말
    - [For Eveyrone, E]: 채점 자동화가 궁금한 분, forked해서 쓰고 싶은 분
    - [For User, U]: 서비스를 이용하는 이용자(튜터/매니저)
    - [For Architect, A]: 과제를 만들고 앱서비스를 런칭하려는 개발자
```

# [E] 일반 개요
- 목적: 프로그래밍/데이터분석/통계 과제 자동채점
- 구조: Cloud run -> Gemini -> Streamlit  -> Cloud SQL
- 환경: Python 3.12.3 

# [U] 사용 방식
- 웹사이트에 진입. 채점할 기수, 과목 등을 선택
- 채점을 할당 받은 과제의 학생 코드를 복-붙
- 채점 버튼 클릭
- 각 문제의 ⭕️, ❌ 결과 / 점수 / LLM 피드백을 확인 하여 채점

# [E] 작동 방식

![채점자동화](/채점서비스scheme.png)
- 웹 사이트에는 특정 과제에 대한 모범답안, 채점가이드 등이 사전 Prompting 되어있음
- LLM 은 모범답안과 제출코드를 비교하며 채점 가이드 에 따라 결과를 출력 출력
- (SQL) 학생 쿼리가 Cloud SQL에 있는 데이터에 실행되어 결과 채점
- (Python) Cloud run 내부 exec 내장함수를 이용하여 serveless에 실행되어 채점

# [A] 서비스 준비
- 문제 (`/question`) 사전에 생성
- (SQL, Python) 정답을 미리 실행하여 answer/{과제명}.txt에 문제 갯 수 만큼(ex 6개) 정답 (`answer`)업로드
  - 향후 채점 실행 시 학생들의 제출 코드를 실행하여 그 결과가 answer/{과제명}.txt와 일치하는 지 확인
- `core/grading_{}.py` 형식으로 각 과제 채점 기준 생성 추후 LLM prompting을 위한 기준(정확도,가독성 등)

# [A] How to run in Local
- `.env` 정보 획득
- 가상환경 생성(Python 3.12)
- `pip install -r requirements.txt`
- `pip install --upgrade google-api-python-client`  # google 모듈 업그레이드가 필요한 경우가 있음
- 메인 진입점 base/streamtlit_app/main.py 실행

# [A] how to run in Local Docker
- bash 혹은 cmd 사용
```bash
# base 디렉토리로 이동
cd base

# Docker 이미지 빌드 (Cloud Run 배포용과 동일)
docker build --platform linux/amd64 -t {서비스명} .

# 빌드된 이미지로 Docker 컨테이너 실행하기
docker run -d -p 8501:8080 -m 1g --name {개발 이미지명} {서비스명}
```

# [A] how to deploy on cloud run
```sh
#!/bin/bash
# 스크립트 실행 중 오류 발생 시 즉시 중단
set -e

# 2. Docker 이미지 빌드 (linux/amd64 플랫폼)
echo "Building Docker image..."
docker build --platform linux/amd64 -t {서비스명} .

# 3. Artifact Registry에 맞게 이미지 태그 지정
echo "Tagging image for Artifact Registry..."
docker tag {서비스명} {이미지명}.pkg.dev/{프로젝트}/cloud-run-source-deploy/{서비스명}

# 4. Artifact Registry로 이미지 푸시
echo "Pushing image to Artifact Registry..."
docker push {이미지명}.pkg.dev/{프로젝트}/cloud-run-source-deploy/{서비스명}

# 5. Cloud Run에 배포 (us-central1)
echo "Deploying to Cloud Run..."
gcloud run deploy grading-app \
  --image={이미지명}.pkg.dev/{프로젝트명}/cloud-run-source-deploy/{서비스명} \
  --region=us-central1 \
  --platform=managed \
  --vpc-connector={vpc 커넥터} \
  --vpc-egress=all
echo "Deployment complete! 🚀"
```

# [A] 디렉토리 설명

## 🗂️ base 디렉토리 설명
- 기본 cloud run 디렉토리

| 항목 | 설명 |
|------|------|
| `answer` | 과제 **정답 코드**를 `{기수}_{과제명}` 형식으로 저장 |
| `core` | 프로젝트의 **핵심 비즈니스 로직** (채점, 프롬프트 생성 등) |
| `data` | 분석 및 앱을 위한 **데이터 파일** (예: 학생/튜터 정보)을 보관 |
| `deprecated` | 더 이상 사용하지 않지만, 기록을 위해 보존하는 **임시 파일** |
| `experiments` | **Jupyter 노트북** 등 실험적인 코드 및 분석 자료를 위한 공간 |
|`external_service`| Gemini, MySQL 등 **외부 서비스 연동 및 설정 모듈** |
|`question`| 과제 정보 |
|`streamlit_app`| **Streamlit 기반의 웹 애플리케이션 모듈** |
|`.dockerignore`| docker에 올릴때 필요하지 않은 파일을 명시(예: 가상환경) |
|`.env.example`| **환경 변수 설정을 위한 샘플 파일**로, 실제 `.env` 파일 생성 시 참고 |
|`.gitignore`| Git 버전 관리에서 **추적을 제외할 파일/폴더** (예: 가상 환경 `venv/`, 환경 변수 파일 `.env`)를 
|`Dockerfile`| Cloud Run 배포를 위한 **Docker 이미지 빌드 설정** 파일입|
|`README.md`| 현재 프로젝트에 대한 **소개 및 초기 설정/실행 가이드** 문서|
|`requirements.txt`| 프로젝트 실행에 필요한 **Python 패키지 의존성 목록**을 정의|
명시합니다. |
|`credentials/`| Google BigQuery 연결을 위한 **서비스 계정의 JSON 키**를 저장하는 보안 디렉토리입니다. (파일 내용은 별도 문서 참조) |

## 🚀 `streamlit_app/` – Streamlit 애플리케이션 모듈 상세
- 웹 기반 인터페이스를 제공하는 Streamlit 앱 관련 파일입니다.

| 항목 | 설명 |
|------|------|
| `main.py` | Streamlit 앱 실행 진입점 |
| `service.py` |  Streamlit 앱 내 서비스 디렉토리 |
 |

---

###  `core/` – 채점 및 응답 핵심 로직

| 항목 | 설명 |
|------|------|
| `__init__py` | **작업 디렉토리를 프로젝트 루트로 설정** |
| `grader.py` | 학생 과제에 대한 Gemini **실제 채점 로직** |
| `grading_python_basic` | 파이썬 채점 기준 |
| `grading_sql` | sql 채점 기준|
| `local_grader.py` |  exec 내장 함수를 이용한 파이썬 채점 코드|
| `prompt_builder.py` | LLM(대규모 언어 모델) **프롬프트를 동적으로 생성** |
---

### `external_service/` – 외부 API 및 설정 관리

| 항목 | 설명 |
|------|------|
| `config.py` | 프로젝트의 **환경 변수를 안전하게 로딩하고 관리**하는 모듈 |
| `llm_client.py` | Gemini/OpenAI 등 다양한 LLM **API 호출을 추상화하고 래핑** |
| `mysql_engine.py` | **MySQL 데이터베이스 연결 및 채점 관련 스크립트**를 포함 |


### `deprecated/` – 당장은 필요없는 코드

| 항목 | 설명 |
|------|------|
|`bq_engine` | SQL 과제 채점을 위해 BigQuery에 SQL을 날리는 코드였으나, MySQL 환경이여서 deprecated |
|`generate_answer.py` | SQL 과제 채점을 위해서 정답 테이블을 bg_engine을 이용해 만드는 코드 |
|`cloud_function_client` | cloud function 실행시키는 코드|

### ` grading-app-python`
- cloud run function에 배포하는 코드. deprecated
- https://github.com/llm-bot-sparta/llmbot/tree/main/grading-app_python
