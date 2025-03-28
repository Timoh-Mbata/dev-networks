import sqlite3
from flask import Blueprint, request, jsonify
from .stk_buygoods_payment import initiate_stk_push

payment_bp = Blueprint('payment', __name__)

def init_db():
    with sqlite3.connect("payments.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            mac_address TEXT UNIQUE,
                            phone_number TEXT,
                            amount REAL,
                            transaction_id TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
init_db()

@payment_bp.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    mac_address = data.get("mac_address")
    phone_number = data.get("phone_number")
    amount = data.get("amount")

    if not mac_address or not phone_number or amount is None:
        return jsonify({"message": "Missing required details"}), 400

    if amount < 50:
        return jsonify({"message": "Payment failed. Please pay the required amount."}), 400
    transaction_id = initiate_stk_push(phone_number, amount, mac_address)

    if transaction_id:
        with sqlite3.connect("payments.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO payments (mac_address, phone_number, amount, transaction_id) VALUES (?, ?, ?, ?)",
                           (mac_address, phone_number, amount, transaction_id))
            conn.commit()

        return jsonify({"message": "Payment request sent. Approve on your phone.", "transaction_id": transaction_id}), 200
    else:
        return jsonify({"message": "Payment request failed"}), 400

@payment_bp.route('/check_access', methods=['GET'])
def check_access():
    mac_address = request.args.get("mac_address")

    if not mac_address:
        return jsonify({"message": "Missing mac_address"}), 400

    with sqlite3.connect("payments.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE mac_address = ?", (mac_address,))
        record = cursor.fetchone()

    if record:
        return jsonify({"access": True}), 200
    else:
        return jsonify({"access": False}), 200
