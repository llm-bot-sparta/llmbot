from .questions_sql import QUESTIONS as SQL_QUESTIONS         # . (점)을 사용하여 같은 패키지 내 모듈임을 명시
from .questions_python_basic import QUESTIONS as PYTHON_QUESTIONS # . (점)을 사용하여 같은 패키지 내 모듈임을 명시

QUESTIONS = {
    "SQL": SQL_QUESTIONS,
    "Python기초": PYTHON_QUESTIONS
}