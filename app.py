import streamlit as st
from tools.recipe_generator import generate_recipe
from tools.email_sender import send_email
from main import parse_recipe
import os

# ---------------------------- Styling ----------------------------
st.set_page_config(page_title="MealBuddy.ai", layout="centered")
st.markdown("""
    <style>
        .stTextInput > div > input, .stNumberInput input {
            background-color: #f4f6fa;
            padding: 10px;
            border-radius: 8px;
        }
        .stRadio > div {
            display: flex;
            gap: 10px;
        }
        .stForm button {
            background-color: #6c63ff;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 10px;
        }
        .stForm button:hover {
            background-color: #4e47d0;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------- Title ----------------------------
st.markdown(
    "<h1 style='text-align: center;'>🍽️ <span style='color:#6c63ff;'>MealBuddy.ai</span></h1>",
    unsafe_allow_html=True
)

# ---------------------------- Form ----------------------------
with st.form("recipe_form"):
    st.markdown("### 🧠 Preferences")

    col1, col2 = st.columns([1, 2])
    with col1:
        mode = st.radio("Are you dieting?", ["Yes", "No"], index=0, horizontal=True)
    with col2:
        custom_prompt = st.text_input("Meal Preference", placeholder="e.g., High protein vegan pasta")

    user_email = st.text_input("Recipient Email", placeholder="Please enter your email")
    email = user_email if user_email else os.getenv("RECEIVER_EMAIL", "")

    st.markdown("### 🔥 Calories")
    c1, c2, c3 = st.columns(3)
    with c1:
        calories_breakfast = st.number_input("Breakfast", value=300, step=50)
    with c2:
        calories_lunch = st.number_input("Lunch", value=500, step=50)
    with c3:
        calories_dinner = st.number_input("Dinner", value=600, step=50)

    submitted = st.form_submit_button("🍳 Generate & Send Recipes")

# ---------------------------- Recipe Generation ----------------------------
if submitted:
    mode_flag = "dieting" if mode.lower() == "yes" else "not dieting"
    calorie_dict = {
        "breakfast": str(calories_breakfast),
        "lunch": str(calories_lunch),
        "dinner": str(calories_dinner),
    }

    meals = ["breakfast", "lunch", "dinner"]
    recipes = []

    with st.spinner("Generating recipes..."):
        for meal in meals:
            prompt = f"{custom_prompt} for {meal}, around {calorie_dict[meal]} calories. Dieting: {mode_flag == 'dieting'}"
            raw_response = generate_recipe.invoke({
                "meal": meal,
                "mode": mode_flag,
                "custom_prompt": prompt
            })

            name, ingredients, recipe = parse_recipe(raw_response)

            formatted = (
                f"### {meal.capitalize()} ({calorie_dict[meal]} calories)\n"
                f"**Name:** {name}\n\n"
                f"**Ingredients:**\n{ingredients}\n\n"
                f"**Recipe:**\n{recipe}"
            )
            st.markdown(formatted)
            recipes.append(formatted)

    full_body = "\n\n".join(recipes)

    send_email.invoke({
        "subject": f"Your {mode_flag.capitalize()} Recipes for Today 🍽️",
        "body": full_body,
        "recipient_override": email
    })

    st.success("✅ Recipes sent via email!")
