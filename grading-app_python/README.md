## 중요
- exec 내장함수로 파이썬내 파이썬 코드 실행 기능이 확인 됨에 따라 cloud run function은 deprecated

## Python 과제 채점을 위한 파이썬 스크립트

- cloud run function에 적재되어 필요할 때마다(ondemand)하여 구동
- functions_framework 프레임워크를 사용하여 gcp와 연동
- 제출한 코드를 채점하는 식으로 기능

## 디렉토리 설명
- main.py: cloud run function의 진입점이자 백엔드 서버
- app.py: 로컬에서 테스트 할 수 있도록 streamlit 으로 구현되어있는 프론트 서버

## 실행방법(cloud run function에 배포된 경우)
- bash shell에서
``` 
curl -X POST "`{cloudrun function url}" -H "Content-Type: application/json" -d '{"code": "def calculate_stock(numbers):\n    if not numbers: return 0\n    return sum(numbers) / len(numbers)", "function_name": "calculate_stock", "test_cases": [{"input": [[10, 20, 30, 40, 50]], "output": 30.0}]}'
```
## 실행방법(로컬)

1. python 3.12 및 requirments.txt 실행
2. 백엔드 서버실행 
- `functions_framework --target=grade_code --debug`
3-1 bash에서 curl 명령어로 테스트
```
curl -X POST "http://localhost:8080" \
-H "Content-Type: application/json" \
-d '{
    "code": "def get_square(x):\n    return x * x",
    "function_name": "get_square",
    "test_cases": [
        {"input": [3], "output": 9},
        {"input": [-2], "output": 4}
    ]
}'
```
3-2 (선택, 로컬에서 테스트 시) 프론트 서버 실행
- `streamlit run app.py` 
- 로컬에서 테스트 시 pandas, streamlit 추가 설치 필요함
