import pandas as pd


def generate_insights(df):

    insights = []

    # Ensure Date column is datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # =============================
    # Highest Spending Category
    # =============================

    category_summary = df.groupby("Category")["Amount"].sum()

    if not category_summary.empty:

        highest_category = category_summary.idxmax()

        insights.append(
            f"Highest spending category: {highest_category}"
        )

    # =============================
    # Monthly Trend Analysis
    # =============================

    monthly_summary = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
    )

    if len(monthly_summary) >= 2:

        last_month = monthly_summary.iloc[-1]
        previous_month = monthly_summary.iloc[-2]

        if previous_month != 0:

            change_percent = round(
                ((last_month - previous_month) / previous_month) * 100,
                2
            )

            if change_percent > 0:

                insights.append(
                    f"Your total spending increased by {change_percent}% compared to last month."
                )

            elif change_percent < 0:

                insights.append(
                    f"Great job! Spending decreased by {abs(change_percent)}% compared to last month."
                )

    # =============================
    # Category Trend Intelligence
    # =============================

    df["Month"] = df["Date"].dt.to_period("M")

    unique_months = df["Month"].unique()

    if len(unique_months) >= 2:

        last_month = unique_months[-1]
        previous_month = unique_months[-2]

        last_data = df[df["Month"] == last_month]
        prev_data = df[df["Month"] == previous_month]

        last_category = last_data.groupby("Category")["Amount"].sum()
        prev_category = prev_data.groupby("Category")["Amount"].sum()

        for category in last_category.index:

            if category in prev_category and prev_category[category] != 0:

                change = last_category[category] - prev_category[category]

                percent_change = round(
                    (change / prev_category[category]) * 100,
                    2
                )

                if percent_change > 0:

                    insights.append(
                        f"{category} spending increased by {percent_change}% this month."
                    )

                elif percent_change < 0:

                    insights.append(
                        f"{category} spending decreased by {abs(percent_change)}% this month."
                    )

    # =============================
    # Savings Suggestion Engine
    # =============================

    total_spending = df["Amount"].sum()

    if total_spending > 0:

        for category, amount in category_summary.items():

            percent = (amount / total_spending) * 100

            if percent > 35:

                savings = round(amount * 0.10, 2)

                insights.append(
                    f"You spend {round(percent,2)}% on {category}. Reducing 10% could save ₹{savings}."
                )

    # =============================
    # Expense Anomaly Detection
    # =============================

    for category, group in df.groupby("Category"):

        mean = group["Amount"].mean()
        std = group["Amount"].std()

        if std > 0:

            threshold = mean + (2 * std)

            anomalies = group[group["Amount"] > threshold]

            for _, row in anomalies.iterrows():

                insights.append(
                    f"Unusual expense detected: ₹{row['Amount']} on {category}"
                )

    return insights