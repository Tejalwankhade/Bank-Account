# bank_account_app.py
import streamlit as st

# ------------------ OOP CLASS ------------------
class BankAccount:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ₹{amount}. New Balance: ₹{self.balance}"
        else:
            return "Deposit amount must be greater than 0."

    def withdraw(self, amount):
        if amount <= 0:
            return "Withdrawal amount must be greater than 0."
        elif amount > self.balance:
            return "Insufficient balance."
        else:
            self.balance -= amount
            return f"Withdrew ₹{amount}. New Balance: ₹{self.balance}"

    def check_balance(self):
        return f"Your current balance is ₹{self.balance}"

# ------------------ DEFAULT USER DATABASE ------------------
# For demo purposes, storing in a dictionary (username: BankAccount)
users_db = {
    "tejal": BankAccount("tejal", "1234", 1000),
    "admin": BankAccount("admin", "admin123", 5000),
}

# ------------------ STREAMLIT APP ------------------
st.set_page_config(page_title="Bank Account App", page_icon="🏦")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

st.title("🏦 Simple Bank Account System")

# ------------------ LOGIN ------------------
if not st.session_state.logged_in:
    st.subheader("🔐 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in users_db and users_db[username].password == password:
            st.session_state.logged_in = True
            st.session_state.current_user = users_db[username]
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password.")
else:
    # ------------------ BANK OPERATIONS ------------------
    st.success(f"Welcome {st.session_state.current_user.username}!")

    menu = st.radio("Select an Operation", ["Deposit", "Withdraw", "Check Balance", "Logout"])

    if menu == "Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit Money"):
            msg = st.session_state.current_user.deposit(amount)
            st.info(msg)

    elif menu == "Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw Money"):
            msg = st.session_state.current_user.withdraw(amount)
            st.info(msg)

    elif menu == "Check Balance":
        if st.button("Show Balance"):
            msg = st.session_state.current_user.check_balance()
            st.info(msg)

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.success("You have been logged out.")
