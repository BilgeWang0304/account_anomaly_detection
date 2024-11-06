import sqlite3
import random
from scripts.anomaly_detection import detect_anomaly

class Account:
    def __init__(self):
        self.conn = sqlite3.connect('../database/card.sqlite3')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def menu(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            choice = input(">")
            
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print("Bye!")
                break
            else:
                print("Invalid option! Please choose 1, 2, or 0.")
    
    def luhn_algorithm(self):
        card = [4, 0, 0, 0, 0, 0] + random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
        digits = card.copy()
        index = 0
        for num in digits:
            if (index + 1) % 2 != 0:
                digits[index] = num * 2
            index += 1
        index = 0
        for num in digits:
            if num > 9:
                digits[index] -= 9
            index += 1
        total = sum(digits)
        card.append((total * 9) % 10)
        return ''.join(map(str, card))

    def generate_card_number(self):
        return self.luhn_algorithm()
    
    def generate_pin(self):
        return f"{random.randint(0, 9999):04d}"

    def create_account(self):
        card_number = self.generate_card_number()
        pin = self.generate_pin()
        balance = 0
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)
        ''', (card_number, pin, balance))
        self.conn.commit()
        
        print("\nYour card has been created")
        print(f"Your card number:\n{card_number}")
        print(f"Your card PIN:\n{pin}\n")

    def login(self):
        card_number = input("Enter your card number:\n>")
        pin = input("Enter your PIN:\n>")

        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM card WHERE number = ? AND pin = ?
        ''', (card_number, pin))
        account = cursor.fetchone()
        
        if account:
            print("\nYou have successfully logged in!")
            self.account_menu(account)
        else:
            print("\nWrong card number or PIN!\n")
        
    def account_menu(self, account):
        while True:
            print("\n1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            choice = input(">")
            
            if choice == '1':
                self.check_balance(account)
            elif choice == '2':
                self.add_income(account)
            elif choice == '3':
                self.do_transfer(account)
            elif choice == '4':
                self.close_account(account)
                break
            elif choice == '5':
                print("\nYou have successfully logged out!\n")
                break
            elif choice == '0':
                print("Bye!")
                exit()
            else:
                print("Invalid option! Please choose 1, 2, 3, 4, 5, or 0.")

    def add_income(self, account):
        income = int(input("Enter income:\n>"))
        cursor = self.conn.cursor()
        new_balance = account[3] + income

        cursor.execute('''
            UPDATE card SET balance = ? WHERE number = ?
        ''', (new_balance, account[1]))
        self.conn.commit()
        
        print("Income was added!")

    def do_transfer(self, account):
        receiver_card_number = input("Transfer\nEnter card number:\n>")

        if not self.luhn_algorithm(receiver_card_number):
            print("Probably you made a mistake in the card number. Please try again!")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM card WHERE number = ?
        ''', (receiver_card_number,))
        receiver_account = cursor.fetchone()

        if receiver_account is None:
            print("Such a card does not exist.")
            return
        
        if account[1] == receiver_card_number:
            print("You can't transfer money to the same account!")
            return
        
        amount = int(input("Enter how much money you want to transfer:\n>"))
        
        if amount > account[3]:
            print("Not enough money!")
            return
        
        new_balance_sender = account[3] - amount
        new_balance_receiver = receiver_account[3] + amount
        
        cursor.execute('''
            UPDATE card SET balance = ? WHERE number = ?
        ''', (new_balance_sender, account[1]))
        
        cursor.execute('''
            UPDATE card SET balance = ? WHERE number = ?
        ''', (new_balance_receiver, receiver_card_number))
        
        self.conn.commit()
        
        print("Success!")
        
    def close_account(self, account):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM card WHERE number = ?
        ''', (account[1],))
        self.conn.commit()
        print("The account has been closed!")