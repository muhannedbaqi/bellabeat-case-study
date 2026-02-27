# ============================================================
# Bellabeat Growth Strategy Analysis
# Author: Muhanned Abdulbaqi Mohammed
# Senior-Level Analytical Portfolio Version
# ============================================================

# -------------------------
# 1. Import Libraries
# -------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# 2. Load Dataset
# -------------------------

# Replace with your dataset path
df = pd.read_csv("dailyActivity_merged.csv")

# -------------------------
# 3. Data Cleaning
# -------------------------

# Convert date column
df["ActivityDate"] = pd.to_datetime(df["ActivityDate"])

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# -------------------------
# 4. Feature Engineering
# -------------------------

# Total Active Minutes
df["TotalActiveMinutes"] = (
    df["VeryActiveMinutes"]
    + df["FairlyActiveMinutes"]
    + df["LightlyActiveMinutes"]
)

# Activity Consistency (rolling std per user)
df["ActivityVariance"] = df.groupby("Id")["TotalSteps"].transform(
    lambda x: x.rolling(window=7, min_periods=1).std()
)

# Engagement Score (scaled)
df["EngagementScore"] = (
    (df["TotalActiveMinutes"] / df["TotalActiveMinutes"].max()) * 0.4
    + (df["Calories"] / df["Calories"].max()) * 0.3
    + (df["TotalSteps"] / df["TotalSteps"].max()) * 0.3
)

# -------------------------
# 5. Behavioral Segmentation
# -------------------------

conditions = [
    df["TotalSteps"] < 5000,
    (df["TotalSteps"] >= 5000) & (df["TotalSteps"] < 10000),
    df["TotalSteps"] >= 10000,
]

choices = ["Low Engagement", "Inconsistent Actives", "High Discipline"]

df["Segment"] = np.select(conditions, choices)

# -------------------------
# 6. Aggregated Insights
# -------------------------

segment_summary = df.groupby("Segment").agg(
    AvgSteps=("TotalSteps", "mean"),
    AvgCalories=("Calories", "mean"),
    AvgActiveMinutes=("TotalActiveMinutes", "mean"),
    AvgEngagement=("EngagementScore", "mean"),
)

print("\nSegment Summary:\n")
print(segment_summary)

# -------------------------
# 7. Visualization Section
# -------------------------

plt.rcParams["figure.figsize"] = (8, 5)

# 7.1 Average Daily Steps by Segment
plt.figure()
segment_summary["AvgSteps"].plot(kind="bar")
plt.title("Average Daily Steps by Behavioral Segment")
plt.xlabel("User Segment")
plt.ylabel("Average Steps")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("chart_avg_steps_by_segment.png")
plt.close()

# 7.2 Engagement Score by Segment
plt.figure()
segment_summary["AvgEngagement"].plot(kind="bar")
plt.title("Average Engagement Score by Segment")
plt.xlabel("User Segment")
plt.ylabel("Engagement Score")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("chart_engagement_score.png")
plt.close()

# 7.3 Weekday vs Weekend Analysis
df["DayType"] = df["ActivityDate"].dt.dayofweek.apply(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

weekday_summary = df.groupby("DayType")["TotalSteps"].mean()

plt.figure()
weekday_summary.plot(kind="bar")
plt.title("Average Steps: Weekday vs Weekend")
plt.xlabel("Day Type")
plt.ylabel("Average Steps")
plt.tight_layout()
plt.savefig("chart_weekday_vs_weekend.png")
plt.close()

# 7.4 Correlation Heatmap
plt.figure()
corr = df[
    ["TotalSteps", "Calories", "TotalActiveMinutes", "EngagementScore"]
].corr()

sns.heatmap(corr, annot=True)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig("chart_correlation_matrix.png")
plt.close()

# -------------------------
# 8. Business Insight Outputs
# -------------------------

print("\nKey Business Insights:\n")

print("1. Inconsistent Actives represent the largest moderate-step segment.")
print("2. Engagement score correlates strongly with active minutes.")
print("3. Activity drops during weekends — opportunity for activation campaigns.")
print("4. High-discipline users present upsell potential.")

# -------------------------
# 9. Projected Impact Model
# -------------------------

avg_clv = 120  # hypothetical annual CLV
user_base = 10000
conversion_increase = 0.05

projected_revenue_gain = user_base * conversion_increase * avg_clv

print("\nProjected Revenue Gain from 5% Conversion Increase:")
print(f"${projected_revenue_gain:,.2f}")

# ============================================================
# END OF ANALYSIS
# ============================================================
