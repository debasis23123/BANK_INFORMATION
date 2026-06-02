A simple Bank Management System built using Flask (Python) and MySQL.
This project allows users to manage bank accounts, perform transactions, and view account details through a web interface.

🚀 Features
🔐 User Login System (Session-based authentication)
🏦 Dashboard with:
Total Accounts
Total Bank Balance
➕ Create New Bank Account
💰 Deposit Money
💸 Withdraw Money
📊 Check Account Balance
📄 View Account Details
🚪 Logout Functionality
🛠️ Tech Stack
Backend: Python, Flask
Database: MySQL
Frontend: HTML, CSS
Connector: mysql-connector-python
📁 Project Structure
bank-system/
│── app.py
│── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── create.html
│   ├── deposit.html
│   ├── withdraw.html
│   ├── balance.html
│   ├── details.html
│── static/
│── requirements.txt
│── README.md
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/debasis23123/BANK_INFORMATION.git
cd bank-system
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # Linux/Mac
3️⃣ Install Dependencies
pip install flask mysql-connector-python

Or use:

pip install -r requirements.txt