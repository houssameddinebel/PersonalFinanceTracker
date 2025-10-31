import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "personal_finance.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(type_, category, description, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.date.today().isoformat()
    cursor.execute("""
        INSERT INTO transactions (date, type, category, description, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (date, type_, category, description, amount))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_monthly_report():
    transactions = get_transactions()
    if not transactions:
        print("No transactions found.")
        return
    df = pd.DataFrame(transactions, columns=['id','date','type','category','description','amount'])
    df['date'] = pd.to_datetime(df['date'])
    monthly = df.groupby([df['date'].dt.to_period('M'), 'type'])['amount'].sum().unstack().fillna(0)
    print(monthly)

def plot_expenses_by_category():
    transactions = get_transactions()
    df = pd.DataFrame(transactions, columns=['id','date','type','category','description','amount'])
    expenses = df[df['type'].str.lower() == 'expense']
    if expenses.empty:
        print("No expense data to visualize.")
        return
    summary = expenses.groupby('category')['amount'].sum()
    summary.plot(kind='pie', autopct='%1.1f%%', figsize=(6,6))
    plt.title("Expenses by Category")
    plt.show()

def menu():
    create_tables()
    while True:
        print("\n1. Add Transaction\n2. Show All Transactions\n3. Generate Monthly Report\n4. Visualize Expenses by Category\n5. Exit")
        choice = input("Choose: ")
        if choice == '1':
            type_ = input("Type (Income/Expense): ").capitalize()
            category = input("Category: ")
            description = input("Description: ")
            try:
                amount = float(input("Amount: "))
            except:
                print("Invalid amount!")
                continue
            add_transaction(type_, category, description, amount)
            print("Transaction added.")
        elif choice == '2':
            transactions = get_transactions()
            for t in transactions: print(t) if transactions else print("No transactions.")
        elif choice == '3':
            generate_monthly_report()
        elif choice == '4':
            plot_expenses_by_category()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
