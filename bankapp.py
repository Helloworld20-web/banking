from tkinter import *
from tkinter import messagebox
import os

accounts_file = "bankaccounts.txt"

def strong_password(password):
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(not char.isalnum() for char in password):
        return False

    return True


def load_accounts():
    accounts = {}

    if os.path.exists(accounts_file):
        file = open(accounts_file, "r")

        for line in file:
            line = line.strip()

            if line != "":
                parts = line.split("|")

                if len(parts) == 3:
                    username = parts[0]
                    password = parts[1]
                    balance = float(parts[2])

                    accounts[username] = {
                        "password": password,
                        "balance": balance
                    }

        file.close()

    return accounts


def save_accounts():
    file = open(accounts_file, "w")

    for username in accounts:
        password = accounts[username]["password"]
        balance = accounts[username]["balance"]

        file.write(f"{username}|{password}|{balance}\n")

    file.close()


accounts = load_accounts()
current_user = ""


def login():
    global current_user

    username = username_entry.get()
    password = password_entry.get()

    if username in accounts:
        if accounts[username]["password"] == password:
            current_user = username
            messagebox.showinfo("Login", "Login successful!")
            open_bank_window()
        else:
            messagebox.showerror("Login Error", "Incorrect password!")
    else:
        messagebox.showerror("Login Error", "Account does not exist!")


def create_account():
    new_window = Toplevel(window)
    new_window.title("Create your Account Window")
    new_window.geometry("400x350")

    Label(new_window, text="Create Account", font=("Arial", 20)).pack(pady=20)

    Label(new_window, text="Username:").pack()
    new_username = Entry(new_window)
    new_username.pack(pady=5)

    Label(new_window, text="Password:").pack()
    new_password = Entry(new_window, show="*")
    new_password.pack(pady=5)

    Label(new_window, text="Starting Balance:").pack()
    starting_balance = Entry(new_window)
    starting_balance.pack(pady=5)

    def make_account():
        username = new_username.get()
        password = new_password.get()
        balance = starting_balance.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Enter a username and password")
            return


        if strong_password(password) != True:
            messagebox.showerror("Weak Password", "Password must have:\n\n- At least 8 characters\n- At least 1 uppercase letter\n- At least 1 lowercase letter\n- At least 1 number\n- At least 1 special character (!@#$%)")
            return

        if username in accounts:
            messagebox.showerror("Error", "Username already exists")
            return

        try:
            balance = float(balance)

            if balance < 15:
                messagebox.showerror("Error", "Balance should at minimum: 15")
                return

        except ValueError:
            messagebox.showerror("Error", "Dude")
            return

        accounts[username] = {
            "password": password,
            "balance": balance
        }

        save_accounts()

        messagebox.showinfo("Account Created", f"Account {username} has been created")
        new_window.destroy()

    Button(new_window, text="Create Account", bg="green", command=make_account).pack(pady=15)
    Button(new_window, text="Close", bg="green", command=new_window.destroy).pack()


def open_bank_window():
    bank_window = Toplevel(window)
    bank_window.title(f"{current_user}'s Bank Account")
    bank_window.geometry("400x400")

    Label(bank_window, text=f"Welcome {current_user}!", font=("Arial", 18)).pack(pady=20)

    balance_label = Label(bank_window, text=f"Balance: ${accounts[current_user]['balance']:.2f}", font=("Arial", 15))
    balance_label.pack(pady=10)

    def deposit():
        deposit_window = Toplevel(bank_window)
        deposit_window.title("Deposit Window")
        deposit_window.geometry("350x250")

        Label(deposit_window, text="Deposit Money", font=("Arial", 18)).pack(pady=20)

        Label(deposit_window, text="Amount:").pack()
        amount_entry = Entry(deposit_window)
        amount_entry.pack(pady=10)

        def add_money():
            try:
                amount = float(amount_entry.get())

                if amount <= 0:
                    messagebox.showerror("Error", "Enter an amount greater than 0!")
                    return

                accounts[current_user]["balance"] += amount
                save_accounts()

                balance_label.config(text=f"Balance: ${accounts[current_user]['balance']:.2f}")

                messagebox.showinfo("Deposit", f"${amount:.2f} deposited!")
                deposit_window.destroy()

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")

        Button(deposit_window, text="Deposit", bg="green", command=add_money).pack(pady=10)
        Button(deposit_window, text="Close", bg="red", command=deposit_window.destroy).pack()

    def transfer():
        transfer_window = Toplevel(bank_window)
        transfer_window.title("Transfer Window")
        transfer_window.geometry("400x300")

        Label(transfer_window, text="Transfer Money", font=("Arial", 18)).pack(pady=20)

        Label(transfer_window, text="Recipient Username:").pack()
        recipient_entry = Entry(transfer_window)
        recipient_entry.pack(pady=5)

        Label(transfer_window, text="Amount:").pack()
        amount_entry = Entry(transfer_window)
        amount_entry.pack(pady=5)

        def send_money():
            recipient = recipient_entry.get()

            if recipient not in accounts:
                messagebox.showerror("Error", "Recipient account does not exist!")
                return

            if recipient == current_user:
                messagebox.showerror("Error", "You cannot transfer money to yourself!")
                return

            try:
                amount = float(amount_entry.get())

                if amount <= 0:
                    messagebox.showerror("Error", "Enter an amount greater than 0!")
                    return

                if amount > accounts[current_user]["balance"]:
                    messagebox.showerror("Error", "You do not have enough money!")
                    return

                accounts[current_user]["balance"] -= amount
                accounts[recipient]["balance"] += amount

                save_accounts()

                balance_label.config(text=f"Balance: ${accounts[current_user]['balance']:.2f}")

                messagebox.showinfo("Transfer", f"${amount:.2f} sent to {recipient}!")
                transfer_window.destroy()

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")

        Button(transfer_window, text="Transfer", bg="green", command=send_money).pack(pady=15)
        Button(transfer_window, text="Close", bg="red", command=transfer_window.destroy).pack()

    def logout():
        bank_window.destroy()

    Button(bank_window, text="Deposit", bg="green", width=20, command=deposit).pack(pady=10)
    Button(bank_window, text="Transfer Money", bg="green", width=20, command=transfer).pack(pady=10)
    Button(bank_window, text="Logout", bg="red", width=20, command=logout).pack(pady=20)


window = Tk()
window.title("Bank Program")
window.geometry("400x350")

Label(window, text="Bank Program", font=("Arial", 24)).pack(pady=25)

Label(window, text="Username:").pack()
username_entry = Entry(window)
username_entry.pack(pady=5)

Label(window, text="Password:").pack()
password_entry = Entry(window, show="*")
password_entry.pack(pady=5)

login_btn = Button(window, text="Login", bg="green", width=20, command=login)
login_btn.pack(pady=15)

create_btn = Button(window, text="Create your Account", bg="green", width=20, command=create_account)
create_btn.pack()

window.mainloop()