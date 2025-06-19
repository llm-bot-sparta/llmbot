import requests
import os
from dotenv import load_dotenv

load_dotenv()
CLOUD_FUNCTION_URL = os.getenv('CLOUD_FUNCTION')

def call_python_grader(code, function_name, test_cases):
    payload = {
        "code": code,
        "function_name": function_name,
        "test_cases": test_cases
    }
    try:
        response = requests.post(CLOUD_FUNCTION_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"채점 서버 호출 실패: {str(e)}"} 