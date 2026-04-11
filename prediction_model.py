import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def predict_next_month_expense(df):

    if len(df) < 2:
        return None  # Not enough data to predict

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Monthly aggregation
    monthly_data = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
        .reset_index()
    )

    monthly_data["MonthIndex"] = np.arange(len(monthly_data))

    X = monthly_data[["MonthIndex"]]
    y = monthly_data["Amount"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_month_index = [[len(monthly_data)]]
    prediction = model.predict(next_month_index)

    return round(prediction[0], 2)