import streamlit as st
import pandas as pd
import google.generativeai as genai

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Cudocode AI Dashboard",
    layout="wide"
)

# -------------------------------
# GEMINI CONFIG
# -------------------------------

genai.configure(api_key="AIzaSyB-elql1XtZvTzaBJwQ_fOwRCmMW3lcHog")

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

# -------------------------------
# LOAD DATA
# -------------------------------

data = pd.read_csv("dashboard_dataset.csv")

# -------------------------------
# KPI CALCULATIONS
# -------------------------------

total_users = data["user_id"].nunique()

total_submissions = data["submission_id"].count()

success_rate = (
    (data["status"] == "Solved").mean() * 100
)

top_users = (
    data["username"]
    .value_counts()
    .head(5)
)

# -------------------------------
# TITLE
# -------------------------------

st.title("🤖 Cudocode AI Analytics Dashboard")

st.markdown("---")

# -------------------------------
# KPI CARDS
# -------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Users",
    total_users
)

col2.metric(
    "Total Submissions",
    total_submissions
)

col3.metric(
    "Success Rate",
    f"{success_rate:.2f}%"
)

st.markdown("---")

# -------------------------------
# TOP USERS CHART
# -------------------------------

st.subheader("📊 Top Active Users")

st.bar_chart(top_users)

st.markdown("---")

# -------------------------------
# AI CHATBOT
# -------------------------------

st.subheader("🤖 Ask AI Assistant")

question = st.text_input(
    "Ask a question about the dataset"
)

if question:

    dataset_context = f"""

    Cudocode Analytics Dataset

    Total Users: {total_users}

    Total Submissions: {total_submissions}

    Success Rate: {success_rate:.2f}%

    Top Active Users:
    {top_users.to_dict()}

    """

    prompt = f"""

    You are an AI analytics assistant.

    Use the following analytics data:

    {dataset_context}

    User Question:
    {question}

    Give a clear professional answer.
    """

    response = model.generate_content(prompt)

    st.write("### AI Response")

    st.write(response.text)