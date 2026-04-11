import sqlite3

# Connect to database
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()


# Function to insert expense
def add_expense(title, amount, category, date):
    cursor.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
        (title, amount, category, date)
    )
    conn.commit()


# Function to view expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    return cursor.fetchall()