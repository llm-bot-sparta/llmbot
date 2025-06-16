'''
참조 흐름
main.py 입장에서 from questions(디렉토리) import QUESTIONS(__init__.py에 정의된 딕셔너리)
│
├─▶ from questions import QUESTIONS
       ↓
   questions/__init__.py
       ↓
   from .questions_sql import QUESTIONS as SQL_QUESTIONS
   from .questions_python_basic import QUESTIONS as PYTHON_QUESTIONS
       ↓
   questions/questions_sql.py  → QUESTIONS
   questions/questions_python_basic.py  → QUESTIONS

'''

from .questions_sql import QUESTIONS as SQL_QUESTIONS
from .questions_python_basic import QUESTIONS as PYTHON_QUESTIONS

QUESTIONS = {
    "SQL": SQL_QUESTIONS,
    "Python기초": PYTHON_QUESTIONS
}
