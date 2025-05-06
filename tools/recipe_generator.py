import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# @tool
# def generate_recipe(meal: str, mode: str) -> str:
#     """Generates a recipe for the given meal and diet mode using Gemini."""
#     prompt = f"Suggest a {meal} recipe for {'someone dieting' if mode == 'dieting' else 'someone not dieting'}. Provide a short recipe title and ingredients."
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(prompt)
#     print("response:" , response.text)
#     return response.text

@tool
def generate_recipe(meal: str, mode: str, custom_prompt: str = "") -> str:
    """Generates a clearly structured recipe for a given meal and diet mode using Gemini."""
    base_prompt = (
        f"Suggest a {meal} recipe for {'someone dieting' if mode == 'dieting' else 'someone not dieting'}."
    )

    if custom_prompt:
        base_prompt += f" The user wants: {custom_prompt}."

    base_prompt += (
        " Return your response in the following exact format:\n\n"
        "Name: <Recipe Name>\n"
        "Ingredients:\n- item 1\n- item 2\n...\n"
        "Recipe:\nStep-by-step cooking instructions.\n"
        "Make sure the name does NOT include calories.\n"
        "Do NOT use markdown or bold formatting.\n"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(base_prompt)
    print("response:", response.text)
    return response.text
