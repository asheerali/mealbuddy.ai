import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from tools.recipe_generator import generate_recipe
from tools.email_sender import send_email

load_dotenv()

# Initialize graph
builder = StateGraph(MessagesState)

# Tool nodes
recipe_node = ToolNode([generate_recipe])
email_node = ToolNode([send_email])

builder.add_node("generate_recipes", recipe_node)
builder.add_node("send_email", email_node)

builder.set_entry_point("generate_recipes")
builder.add_edge("generate_recipes", "send_email")
builder.set_finish_point("send_email")

graph = builder.compile()

# Function to trigger flow
def run_daily_recipes(mode="dieting"):
    meals = ["breakfast", "lunch", "dinner"]
    recipes = []

    for meal in meals:
        recipe = generate_recipe.invoke({"meal": meal, "mode": mode})
        recipes.append(f"**{meal.capitalize()}**\n{recipe}\n")

    full_email_body = "\n\n".join(recipes)

    send_email.invoke({
        "subject": f"Your {mode.capitalize()} Recipes for Today 🍽️",
        "body": full_email_body
    })

if __name__ == "__main__":
    # Change 'dieting' to 'not dieting' if you want
    run_daily_recipes(mode="dieting")
