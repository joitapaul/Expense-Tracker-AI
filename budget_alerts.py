import pandas as pd


def check_budget_alerts(df, budgets):

    alerts = []

    # Current month filtering
    df["Date"] = pd.to_datetime(df["Date"])
    current_month = df["Date"].dt.to_period("M").max()

    current_data = df[df["Date"].dt.to_period("M") == current_month]

    category_totals = current_data.groupby("Category")["Amount"].sum()

    for category, budget_limit in budgets.items():

        spent = category_totals.get(category, 0)

        if spent > budget_limit:

            alerts.append(
                f"⚠️ Budget exceeded for {category}: ₹{spent} / ₹{budget_limit}"
            )

    return alerts