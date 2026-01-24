import sqlite3
import random

# Connect to SQLite DB (will create if not exists)
conn = sqlite3.connect('payments.db')
c = conn.cursor()

# Drop tables if exist
c.execute("DROP TABLE IF EXISTS transactions")

# Create transactions table
c.execute('''
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_id TEXT UNIQUE,
    gateway_amount REAL,
    bank_amount REAL,
    final_status TEXT,
    step1_status TEXT,
    step2_status TEXT,
    step3_status TEXT,
    step4_status TEXT
)
''')

# Possible step statuses
statuses = ['success', 'pending', 'failed']

# Generate 200+ transactions
for i in range(1, 201):
    txn_id = f'TXN{900000 + i}'
    gateway_amount = round(random.uniform(10, 500), 2)
    
    # Randomly decide if bank amount matches gateway (simulate pending/failure)
    bank_amount = gateway_amount if random.random() > 0.1 else round(random.uniform(0, gateway_amount), 2)
    
    # Step statuses
    step1 = 'success'
    step2 = 'success'
    step3 = random.choices(statuses, weights=[0.7,0.2,0.1])[0]
    step4 = 'success' if step3 == 'success' else 'pending'
    
    # Final status based on step3
    final = 'SUCCESS' if step3 == 'success' else ('PENDING' if step3 == 'pending' else 'FAILED')
    
    c.execute('''
    INSERT INTO transactions (txn_id, gateway_amount, bank_amount, final_status, step1_status, step2_status, step3_status, step4_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (txn_id, gateway_amount, bank_amount, final, step1, step2, step3, step4))

conn.commit()
conn.close()
print("Database initialized with 200+ transactions.")
