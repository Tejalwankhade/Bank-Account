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
        return f"Deposited ₹{amount}. New Balance: ₹{self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "❌ Insufficient balance!"
        self.balance -= amount
        self.transactions.append((datetime.now(), f"Withdrew ₹{amount}"))
        return f"Withdrew ₹{amount}. New Balance: ₹{self.balance}"

    def get_balance(self):
        return self.balance

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

# Session state for account
if "account" not in st.session_state:
    st.session_state.account = None

st.title("🏦 Simple Bank Account Management")

menu = st.sidebar.radio("Navigation", ["Create Account", "Account Details", "Deposit", "Withdraw", "Transactions"])

# Create Account
if menu == "Create Account":
    st.header("Open a New Bank Account")
    name = st.text_input("Enter Account Holder Name")
    acc_number = st.text_input("Enter Account Number")
    balance = st.number_input("Initial Deposit", min_value=0, step=100)

    if st.button("Create Account"):
        if name and acc_number:
            st.session_state.account = BankAccount(name, acc_number, balance)
            st.success(f"✅ Account Created Successfully for {name}")
        else:
            st.error("Please fill all details!")

# Show Account Details
elif menu == "Account Details":
    st.header("📄 Account Information")
    if st.session_state.account:
        details = st.session_state.account.get_details()
        st.write(f"**Holder Name:** {details['Holder Name']}")
        st.write(f"**Account Number:** {details['Account Number']}")
        st.write(f"**Balance:** ₹{details['Balance']}")
    else:
        st.warning("No account found. Please create one.")

# Deposit Money
elif menu == "Deposit":
    st.header("💰 Deposit Money")
    if st.session_state.account:
        amount = st.number_input("Enter amount to deposit", min_value=1, step=100)
        if st.button("Deposit"):
            message = st.session_state.account.deposit(amount)
            st.success(message)
    else:
        st.warning("Please create an account first.")

# Withdraw Money
elif menu == "Withdraw":
    st.header("💳 Withdraw Money")
    if st.session_state.account:
        amount = st.number_input("Enter amount to withdraw", min_value=1, step=100)
        if st.button("Withdraw"):
            message = st.session_state.account.withdraw(amount)
            if "❌" in message:
                st.error(message)
            else:
                st.success(message)
    else:
        st.warning("Please create an account first.")

# Transaction History
elif menu == "Transactions":
    st.header("📜 Transaction History")
    if st.session_state.account:
        transactions = st.session_state.account.get_transactions()
        if transactions:
            for date, action in transactions:
                st.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')} - {action}")
        else:
            st.info("No transactions yet.")
    else:
        st.warning("Please create an account first.")
