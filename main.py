# bank_app.py
import streamlit as st
from datetime import datetime

# ------------------ OOP CLASS ------------------
class BankAccount:
    def __init__(self, name, acc_number, balance=0):
        self.name = name
        self.acc_number = acc_number
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append((datetime.now(), f"Deposited ₹{amount}"))
        return f"✅ Deposited ₹{amount}. New Balance: ₹{self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "❌ Insufficient balance!"
        self.balance -= amount
        self.transactions.append((datetime.now(), f"Withdrew ₹{amount}"))
        return f"✅ Withdrew ₹{amount}. New Balance: ₹{self.balance}"

    def get_details(self):
        return {
            "Holder Name": self.name,
            "Account Number": self.acc_number,
            "Balance": self.balance
        }

    def get_transactions(self):
        return self.transactions

# ------------------ STREAMLIT APP ------------------

st.set_page_config(page_title="Bank Account App", page_icon="🏦")

# Store multiple accounts
if "accounts" not in st.session_state:
    st.session_state.accounts = {}

# Sidebar Navigation
menu = st.sidebar.radio(
    "📌 Navigation",
    ["Create Account", "Select Account & Operate"]
)

# ------------------ CREATE ACCOUNT ------------------
if menu == "Create Account":
    st.header("🏦 Open a New Bank Account")
    name = st.text_input("Enter Account Holder Name")
    acc_number = st.text_input("Enter Account Number")
    balance = st.number_input("Initial Deposit (₹)", min_value=0, step=100)

    if st.button("Create Account"):
        if not name or not acc_number:
            st.error("⚠ Please enter all details!")
        elif acc_number in st.session_state.accounts:
            st.error("⚠ Account number already exists!")
        else:
            st.session_state.accounts[acc_number] = BankAccount(name, acc_number, balance)
            st.success(f"✅ Account Created Successfully for {name}")

# ------------------ ACCOUNT OPERATIONS ------------------
elif menu == "Select Account & Operate":
    if st.session_state.accounts:
        selected_acc = st.selectbox(
            "Select Account",
            list(st.session_state.accounts.keys()),
            format_func=lambda acc: f"{acc} - {st.session_state.accounts[acc].name}"
        )

        account = st.session_state.accounts[selected_acc]
        st.subheader(f"Account Holder: {account.name}")

        operation = st.radio("Choose Operation", ["View Details", "Deposit", "Withdraw", "Transaction History"])

        # View Details
        if operation == "View Details":
            details = account.get_details()
            st.write(f"**Holder Name:** {details['Holder Name']}")
            st.write(f"**Account Number:** {details['Account Number']}")
            st.write(f"**Balance:** ₹{details['Balance']}")

        # Deposit
        elif operation == "Deposit":
            amount = st.number_input("Enter amount to deposit", min_value=1, step=100)
            if st.button("Deposit Money"):
                st.success(account.deposit(amount))

        # Withdraw
        elif operation == "Withdraw":
            amount = st.number_input("Enter amount to withdraw", min_value=1, step=100)
            if st.button("Withdraw Money"):
                msg = account.withdraw(amount)
                if "❌" in msg:
                    st.error(msg)
                else:
                    st.success(msg)

        # Transaction History
        elif operation == "Transaction History":
            transactions = account.get_transactions()
            if transactions:
                for date, action in transactions:
                    st.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')} - {action}")
            else:
                st.info("No transactions yet.")

    else:
        st.warning("⚠ No accounts found. Please create an account first.")
