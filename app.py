from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# DB Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="debasis@2005",
        database="bankdb"
    )

# Login Page
@app.route('/')
def home():
    return render_template('login.html')


# 🔐 Login System
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        session['user'] = username
        return redirect('/dashboard')
    else:
        return render_template('login.html', error="❌ Invalid Username or Password")


# 🏦 Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(balance) FROM accounts")
    total_balance = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        'dashboard.html',
        username=session['user'],
        total_accounts=total_accounts,
        total_balance=total_balance
    )


# ➕ CREATE ACCOUNT
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        acc_no = request.form['acc_no']
        name = request.form['name']
        balance = request.form['balance']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts VALUES (%s,%s,%s)", (acc_no, name, balance))
        conn.commit()
        conn.close()

        return "✅ Account Created Successfully"

    return render_template('create.html')


# 💰 DEPOSIT
@app.route('/deposit', methods=['GET','POST'])
def deposit():
    if request.method == 'POST':
        acc_no = request.form['acc_no']
        amount = request.form['amount']

        conn = get_connection()
        cursor = conn.cursor()

        # Check account exists
        cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s", (acc_no,))
        data = cursor.fetchone()

        if data:
            cursor.execute("UPDATE accounts SET balance=balance+%s WHERE acc_no=%s", (amount, acc_no))
            conn.commit()
            msg = "✅ Money Deposited Successfully"
        else:
            msg = "❌ Account Not Found"

        conn.close()
        return msg

    return render_template('deposit.html')


# 💸 WITHDRAW
@app.route('/withdraw', methods=['GET','POST'])
def withdraw():
    if request.method == 'POST':
        acc_no = request.form['acc_no']
        amount = float(request.form['amount'])

        conn = get_connection()
        cursor = conn.cursor()

        # Check balance
        cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s", (acc_no,))
        data = cursor.fetchone()

        if data:
            current_balance = data[0]

            if current_balance >= amount:
                cursor.execute("UPDATE accounts SET balance=balance-%s WHERE acc_no=%s", (amount, acc_no))
                conn.commit()
                msg = "✅ Withdraw Successful"
            else:
                msg = "❌ Insufficient Balance"
        else:
            msg = "❌ Account Not Found"

        conn.close()
        return render_template('withdraw.html', message=msg)

    return render_template('withdraw.html')


# 📊 BALANCE
@app.route('/balance', methods=['GET','POST'])
def balance():
    if request.method == 'POST':
        acc_no = request.form['acc_no']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s", (acc_no,))
        data = cursor.fetchone()

        conn.close()

        if data:
            msg = f"💰 Your Balance is: ₹ {data[0]}"
        else:
            msg = "❌ Account Not Found"

        return render_template('balance.html', message=msg)

    return render_template('balance.html')


# 📄 DETAILS
@app.route('/details', methods=['GET','POST'])
def details():
    return render_template('details.html')


# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)