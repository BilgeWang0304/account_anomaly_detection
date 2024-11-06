import sqlite3
import random
from datetime import datetime, timedelta
import csv
import os

class DataGenerator:
    def __init__(self, num_accounts=1000, num_transactions=5000, fraud_percentage=0.05):
        self.conn = sqlite3.connect('../database/card.sqlite3')
        self.num_accounts = num_accounts
        self.num_transactions = num_transactions
        self.fraud_percentage = fraud_percentage  
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_log (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                amount INTEGER NOT NULL,
                sender_balance INTEGER NOT NULL,
                is_fraud INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def luhn_algorithm(self):
        card = [4, 0, 0, 0, 0, 0] + random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
        digits = card.copy()
        for index in range(len(digits)):
            if (index + 1) % 2 != 0:
                digits[index] *= 2
            if digits[index] > 9:
                digits[index] -= 9
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
        balance = random.randint(8000, 100000)  # Random initial balance
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)
        ''', (card_number, pin, balance))
        self.conn.commit()

        return card_number

    def generate_accounts(self):
        for _ in range(self.num_accounts):
            self.create_account()

    def simulate_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT number FROM card')
        accounts = cursor.fetchall()

        transactions = []
        transfer_count = {}

        for i in range(self.num_transactions):
            sender = random.choice(accounts)[0]
            receiver = random.choice(accounts)[0]
            while receiver == sender:
                receiver = random.choice(accounts)[0]

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if sender not in transfer_count:
                transfer_count[sender] = 0
            
            transfer_count[sender] += 1

            if transfer_count[sender] > 2:
                is_fraud = 1
                amount = random.randint(0, 100000)
            else:
                is_fraud = 1 if random.random() < self.fraud_percentage else 0
                if is_fraud:
                    amount = random.randint(20000, 100000)
                else:
                    amount = random.randint(10, 20000)

            cursor.execute('SELECT balance FROM card WHERE number = ?', (sender,))
            sender_balance = cursor.fetchone()[0]

            if sender_balance >= amount:
                cursor.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (amount, sender))
                cursor.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (amount, receiver))
                self.conn.commit()
                cursor.execute('''
                    INSERT INTO transaction_log (timestamp, sender, receiver, amount, is_fraud)
                    VALUES (?, ?, ?, ?, ?)
                ''', (timestamp, sender, receiver, amount, is_fraud))
                self.conn.commit()

                transactions.append([timestamp, sender, receiver, amount, sender_balance, is_fraud])

        csv_file_path = os.path.join('../database', 'transaction_log.csv')
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'sender', 'receiver', 'amount', 'sender_balance', 'is_fraud']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(transactions)

    def generate_data(self):
        print("Generating accounts...")
        self.generate_accounts()
        print("Simulating transactions...")
        self.simulate_transactions()
        print("Data generation complete!")


# Run the data generator
if __name__ == "__main__":
    generator = DataGenerator(num_accounts=2000, num_transactions=10000, fraud_percentage=0.05)
    generator.generate_data()
