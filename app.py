from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB = 'payments.db'

def get_txn(txn_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT txn_id, gateway_amount, bank_amount, final_status, step1_status, step2_status, step3_status, step4_status FROM transactions WHERE txn_id=?", (txn_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "txn_id": row[0],
            "gateway_amount": row[1],
            "bank_amount": row[2],
            "final_status": row[3],
            "steps": [
                {"name": "Payment Initiated", "status": row[4]},
                {"name": "Gateway Accepted", "status": row[5]},
                {"name": "Bank Processing", "status": row[6]},
                {"name": "Settlement", "status": row[7]}
            ]
        }
    return None

@app.route('/')
def home():
    # Serves the HTML dashboard
    return render_template('dashboard.html')

@app.route('/transaction/<txn_id>')
def transaction(txn_id):
    txn = get_txn(txn_id)
    if txn:
        return jsonify(txn)
    return jsonify({"error": "Transaction not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
