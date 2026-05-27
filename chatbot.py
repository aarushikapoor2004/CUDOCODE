import pandas as pd
import google.generativeai as genai

# -------------------------------
# Configure Gemini API
# -------------------------------

genai.configure(api_key="AIzaSyB-elql1XtZvTzaBJwQ_fOwRCmMW3lcHog")

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

# -------------------------------
# Load Dataset
# -------------------------------

data = pd.read_csv("dashboard_dataset.csv")

# -------------------------------
# Generate Insights
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
    .to_dict()
)

difficulty_distribution = (
    data["difficulty"]
    .value_counts()
    .to_dict()
)

# -------------------------------
# Create Dataset Context
# -------------------------------

dataset_context = f"""

Cudocode Analytics Dataset

Total Users: {total_users}

Total Submissions: {total_submissions}

Success Rate: {success_rate:.2f}%

Top Active Users:
{top_users}

Difficulty Distribution:
{difficulty_distribution}

"""

print("Cudocode AI Analytics Assistant Started!")

# -------------------------------
# Chat Loop
# -------------------------------

while True:

    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    prompt = f"""

You are an AI analytics assistant for the Cudocode coding platform.

Use the following analytics data to answer user questions.

{dataset_context}

User Question:
{question}

Answer clearly and professionally.
"""

    try:

        response = model.generate_content(prompt)

        print("\nAI Response:\n")
        print(response.text)

    except Exception as e:

        print("\nError:")
        print(e)