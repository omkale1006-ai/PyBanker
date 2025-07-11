import json
import os
import random

# 📁 Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "accounts.json")

# 🔄 Load account data from file
def load_accounts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ JSON file is empty or invalid, starting fresh.")
            return {}
    return {}

# 💾 Save account data to file
def save_accounts(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Account data saved to: {DATA_FILE}")

# 🏦 Bank Account Class
class BankAccount:
    def __init__(self, name, acc_type, balance, acc_number=None):
        self.name = name
        self.acc_type = acc_type
        self.balance = balance
        self.acc_number = acc_number or self.generate_acc_number()

    def generate_acc_number(self):
        return str(random.randint(1000000000, 9999999999))

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("❌ Deposit amount must be positive.")
        self.balance += amount
        print(f"💰 Deposited ₹{amount}. New balance: ₹{self.balance}.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("❌ Insufficient balance.")
        self.balance -= amount
        print(f"🏧 Withdrew ₹{amount}. New balance: ₹{self.balance}.")

    def check_balance(self):
        return self.balance

    def display_details(self):
        return f"👤 Name: {self.name}\n🔢 Account No: {self.acc_number}\n🏦 Type: {self.acc_type}\n💼 Balance: ₹{self.balance}"

# 🧠 Program Start
raw_data = load_accounts()

while True:
    print("\n===== 🏦 Bank Menu =====")
    print("1️⃣ Create Account")
    print("2️⃣ Deposit")
    print("3️⃣ Withdraw")
    print("4️⃣ Check Balance")
    print("5️⃣ Show Account Details")
    print("0️⃣ Exit")

    choice = input("➡️ Enter your choice: ")

    if choice == '1':
        name = input("👤 Enter Name: ").title()
        acc_type = input("🏦 Account Type (Saving/Current): ").title()
        balance = float(input("💰 Opening Balance: "))

        # Optional duplicate check (same name + type)
        duplicate_found = False
        for acc_no, acc_data in raw_data.items():
            if acc_data["name"] == name and acc_data["acc_type"].lower() == acc_type.lower():
                print("⚠️ Account already exists with same name and account type.")
                duplicate_found = True
                break

        if not duplicate_found:
            new_acc = BankAccount(name, acc_type, balance)

            # Ensure unique account number
            while new_acc.acc_number in raw_data:
                new_acc.acc_number = new_acc.generate_acc_number()

            raw_data[new_acc.acc_number] = {
                "name": new_acc.name,
                "acc_type": new_acc.acc_type,
                "balance": new_acc.balance
            }
            save_accounts(raw_data)
            print(f"✅ Account Created! Your Account No is: {new_acc.acc_number}")

    elif choice == '2':
        acc_no = input("🔢 Enter Account No: ")
        if acc_no in raw_data:
            amount = float(input("💰 Enter Amount to Deposit: "))
            raw_data[acc_no]["balance"] += amount
            save_accounts(raw_data)
            print("✅ Deposit successful!")
        else:
            print("❌ Account not found!")

    elif choice == '3':
        acc_no = input("🔢 Enter Account No: ")
        if acc_no in raw_data:
            amount = float(input("💸 Enter Amount to Withdraw: "))
            if amount > raw_data[acc_no]["balance"]:
                print("❌ Insufficient balance!")
            else:
                raw_data[acc_no]["balance"] -= amount
                save_accounts(raw_data)
                print("✅ Withdrawal successful!")
        else:
            print("❌ Account not found!")

    elif choice == '4':
        acc_no = input("🔢 Enter Account No: ")
        if acc_no in raw_data:
            print(f"💼 Balance: ₹{raw_data[acc_no]['balance']}")
        else:
            print("❌ Account not found!")

    elif choice == '5':
        acc_no = input("🔢 Enter Account No: ")
        if acc_no in raw_data:
            data = raw_data[acc_no]
            print(f"👤 Name: {data['name']}")
            print(f"🏦 Type: {data['acc_type']}")
            print(f"💰 Balance: ₹{data['balance']}")
        else:
            print("❌ Account not found!")

    elif choice == '0':
        print("👋 Exiting... Thank you!")
        break

    else:
        print("❌ Invalid choice. Try again.")
