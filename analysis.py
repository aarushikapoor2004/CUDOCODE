import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load Datasets
# -------------------------------

users = pd.read_csv("data/users.csv")
submissions = pd.read_csv("data/submissions.csv")
problems = pd.read_csv("data/problem.csv")
chatbot = pd.read_csv("data/chatbot.csv")

print("Users:", users.shape)
print("Submissions:", submissions.shape)
print("Problems:", problems.shape)
print("Chatbot:", chatbot.shape)

# -------------------------------
# Merge Datasets
# -------------------------------

merged = submissions.merge(
    users,
    on="user_id",
    how="left"
)

merged = merged.merge(
    problems,
    on="problem_id",
    how="left"
)

print("\nMerged Dataset Shape:", merged.shape)

print("\nMerged Dataset Preview:")
print(merged.head())

# -------------------------------
# Engagement Analysis
# -------------------------------

engagement = (
    merged.groupby("username")["submission_id"]
    .count()
    .sort_values(ascending=False)
)

print("\nTop Active Users:")
print(engagement.head())

# -------------------------------
# Success Rate Analysis
# -------------------------------

success_rate = (
    merged["status"]
    .value_counts(normalize=True) * 100
)

print("\nSuccess Rate (%):")
print(success_rate)

# -------------------------------
# Chatbot Impact Analysis
# -------------------------------

chatbot_merge = submissions.merge(
    chatbot,
    on=["user_id", "problem_id"],
    how="left"
)

chatbot_merge["chatbot_used"] = (
    chatbot_merge["chat_id"].notna()
)

impact = chatbot_merge.groupby(
    ["chatbot_used", "status"]
).size()

print("\nChatbot Impact:")
print(impact)

# -------------------------------
# Top Active Users Visualization
# -------------------------------

top_users = engagement.head(5)

plt.figure(figsize=(8, 5))

sns.barplot(
    x=top_users.index,
    y=top_users.values
)

plt.title("Top Active Users")
plt.xlabel("Username")
plt.ylabel("Number of Submissions")

plt.savefig("images/top_users.png")

plt.close()

# -------------------------------
# Success Rate Visualization
# -------------------------------

status_counts = merged["status"].value_counts()

plt.figure(figsize=(6, 6))

plt.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%"
)

plt.title("Success vs Failure Rate")

plt.savefig("images/success_rate.png")

plt.close()

# -------------------------------
# Difficulty Distribution
# -------------------------------

difficulty_counts = (
    merged["difficulty"]
    .value_counts()
)

plt.figure(figsize=(7, 5))

sns.barplot(
    x=difficulty_counts.index,
    y=difficulty_counts.values
)

plt.title("Problem Difficulty Distribution")
plt.xlabel("Difficulty")
plt.ylabel("Number of Submissions")

plt.savefig("images/difficulty_distribution.png")

plt.close()

# -------------------------------
# Export Dashboard Dataset
# -------------------------------

merged.to_csv(
    "dashboard_dataset.csv",
    index=False
)

print("\nDashboard dataset exported successfully!")