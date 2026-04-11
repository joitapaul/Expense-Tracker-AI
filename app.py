import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from database import add_expense, view_expenses
from category_model import predict_category
from prediction_model import predict_next_month_expense
from insights import generate_insights
from budget_alerts import check_budget_alerts


# =============================
# PAGE CONFIG
# =============================

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# =============================
# SIDEBAR SETTINGS
# =============================

st.sidebar.header("⚙️ Settings")

theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown(
        """
        <style>
        body {background-color: #0e1117; color: white;}
        </style>
        """,
        unsafe_allow_html=True
    )


# =============================
# HEADER
# =============================

st.markdown(
    "<h1 style='text-align:center;'>💰 Smart Expense Tracker with AI Insights</h1>",
    unsafe_allow_html=True
)

st.divider()


# =============================
# ADD EXPENSE (MAIN SCREEN)
# =============================

st.subheader("➕ Add New Expense")

col1, col2, col3 = st.columns(3)

with col1:
    title = st.text_input("Expense Title")

with col2:
    amount = st.number_input("Amount", min_value=0.0)

with col3:
    date = st.date_input("Date", datetime.today())

category = predict_category(title) if title else "Other"

st.info(f"Detected Category: **{category}**")

if st.button("Add Expense"):

    if title.strip() == "":
        st.warning("Enter expense title")

    elif amount <= 0:
        st.warning("Amount must be greater than 0")

    else:
        add_expense(title, amount, category, str(date))
        st.success("Expense added successfully ✅")


st.divider()


# =============================
# LOAD DATA
# =============================

expenses = view_expenses()

if expenses:

    df = pd.DataFrame(
        expenses,
        columns=["ID", "Title", "Amount", "Category", "Date"]
    )

    df["Date"] = pd.to_datetime(df["Date"])

else:

    df = pd.DataFrame(
        columns=["ID", "Title", "Amount", "Category", "Date"]
    )


# =============================
# CSV UPLOAD (SIDEBAR)
# =============================

st.sidebar.header("📂 Upload CSV")

uploaded_file = st.sidebar.file_uploader(
    "Upload transaction CSV",
    type=["csv"]
)

if uploaded_file:

    csv_data = pd.read_csv(uploaded_file)

    st.sidebar.success("CSV uploaded successfully")

    st.write("Preview of Uploaded Data")
    st.dataframe(csv_data.head())


# =============================
# CATEGORY FILTER
# =============================

if not df.empty:

    selected_category = st.selectbox(
        "🎯 Filter by Category",
        ["All"] + list(df["Category"].unique())
    )

    if selected_category != "All":
        df = df[df["Category"] == selected_category]


# =============================
# EXPORT REPORT BUTTON
# =============================

if not df.empty:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download Expense Report",
        data=csv,
        file_name="expense_report.csv",
        mime="text/csv"
    )


# =============================
# KPI METRICS
# =============================

if not df.empty:

    total_spent = df["Amount"].sum()
    avg_spent = df["Amount"].mean()
    top_category = df.groupby("Category")["Amount"].sum().idxmax()

    c1, c2, c3 = st.columns(3)

    c1.metric("💸 Total Spending", f"₹{round(total_spent,2)}")
    c2.metric("📊 Average Expense", f"₹{round(avg_spent,2)}")
    c3.metric("🏆 Top Category", top_category)

st.divider()


# =============================
# NAVIGATION TABS
# =============================

tab1, tab2, tab3 = st.tabs(
    ["📊 Dashboard", "🧠 Insights", "🔮 Prediction"]
)


# =============================
# DASHBOARD TAB
# =============================

with tab1:

    if not df.empty:

        left, right = st.columns(2)

        with left:

            category_summary = (
                df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            pie_chart = px.pie(
                category_summary,
                names="Category",
                values="Amount",
                hole=0.4
            )

            st.plotly_chart(pie_chart, use_container_width=True)

        with right:

            monthly_summary = (
                df.groupby(df["Date"].dt.to_period("M"))["Amount"]
                .sum()
                .reset_index()
            )

            monthly_summary["Date"] = monthly_summary["Date"].astype(str)

            trend_chart = px.line(
                monthly_summary,
                x="Date",
                y="Amount",
                markers=True
            )

            st.plotly_chart(trend_chart, use_container_width=True)

    else:
        st.info("No expense data available")


# =============================
# INSIGHTS TAB
# =============================

with tab2:

    if not df.empty:

        insights = generate_insights(df)

        for insight in insights:
            st.info(insight)

    else:
        st.warning("No insights available yet")


# =============================
# PREDICTION TAB
# =============================

with tab3:

    if not df.empty:

        prediction = predict_next_month_expense(df)

        if prediction:
            st.success(f"Expected spending next month: ₹{prediction}")
        else:
            st.warning("Need at least 2 months of data")

        budgets = {
            "Food": 3000,
            "Transport": 1500,
            "Shopping": 4000,
            "Entertainment": 2000,
            "Groceries": 2500
        }

        alerts = check_budget_alerts(df, budgets)

        st.subheader("🚨 Budget Alerts")

        if alerts:
            for alert in alerts:
                st.error(alert)
        else:
            st.success("You are within budget this month ✅")

    else:
        st.warning("No prediction available yet")