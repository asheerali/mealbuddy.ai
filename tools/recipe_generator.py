import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@tool
def generate_recipe(meal: str, mode: str) -> str:
    """Generates a recipe for the given meal and diet mode using Gemini."""
    prompt = f"Suggest a {meal} recipe for {'someone dieting' if mode == 'dieting' else 'someone not dieting'}. Provide a short recipe title and ingredients."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print("response:" , response.text)
    return response.text
