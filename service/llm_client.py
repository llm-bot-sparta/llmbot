import google.generativeai as genai
from service.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_content(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text