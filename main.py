import streamlit as st

# 🏦 Bank Account Class (OOP)
class BankAccount:
    def __init__(self, name, acc_number, balance=0):
        """Initialize account details."""
        self.name = name
        self.acc_number = acc_number
        self.balance = balance

    def deposit(self, amount):
        """Deposit money into the account."""
        self.balance += amount
        return f"✅ Deposited ₹{amount}. New Balance: ₹{self.balance}"

    def withdraw(self, amount):
        """Withdraw money if sufficient balance exists."""
        if amount <= self.balance:
            self.balance -= amount
            return f"💸 Withdrew ₹{amount}. New Balance: ₹{self.balance}"
        else:
            return "❌ Insufficient Balance!"

    def show_balance(self):
        """Return current balance."""
        return f"📌 {self.name}'s Account Balance: ₹{self.balance}"


# ---------------------------
# STREAMLIT APP START
# ---------------------------
st.set_page_config(page_title="Bank Account System", page_icon="🏦")

st.title("🏦 Simple Bank Account System")
st.write("A small interactive app to simulate deposits, withdrawals, and balance checks.")

# Store account object in session state so it persists
if "account" not in st.session_state:
    st.session_state.account = None

# Create account form
if st.session_state.account is None:
    st.subheader("Create Your Bank Account")
    name = st.text_input("Enter Account Holder Name")
    acc_number = st.text_input("Enter Account Number")
    balance = st.number_input("Initial Balance (₹)", min_value=0, value=0, step=100)

    if st.button("Create Account"):
        if name and acc_number:
            st.session_state.account = BankAccount(name, acc_number, balance)
            st.success(f"✅ Account created for {name} with balance ₹{balance}")
        else:
            st.warning("Please enter both name and account number.")

# Show account actions if account exists
else:
    st.subheader(f"Welcome, {st.session_state.account.name}!")
    st.write(st.session_state.account.show_balance())

    # Deposit money
    st.write("### 💰 Deposit Money")
    deposit_amount = st.number_input("Enter amount to deposit", min_value=0, value=0, step=100)
    if st.button("Deposit"):
        if deposit_amount > 0:
            result = st.session_state.account.deposit(deposit_amount)
            st.success(result)
        else:
            st.warning("Please enter an amount greater than ₹0.")

    # Withdraw money
    st.write("### 💸 Withdraw Money")
    withdraw_amount = st.number_input("Enter amount to withdraw", min_value=0, value=0, step=100)
    if st.button("Wi
