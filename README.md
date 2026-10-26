# 🛒 SmartBasket – Smart Grocery Shopping System

SmartBasket is a web-based grocery shopping application developed using Python and Django. It allows users to browse grocery products, search for items, manage a shopping cart, and place demo orders through a simple interface.

## ✨ Features

- **Product Catalog:** Browse grocery products and categories.
- **Product Search:** Find products quickly.
- **Shopping Cart:** Add products and manage quantities.
- **User Authentication:** Register, log in, and access personal orders.
- **Order Management:** Place demo orders and view order history.
- **Stock Validation:** Check product availability during checkout.
- **Admin Dashboard:** Manage products, categories, and orders.
- **Low-Stock Indicators:** Identify products with limited stock.
- **Product Alternatives:** View rule-based, lower-priced alternatives where available.

## 🛠️ Technologies Used

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML, CSS, Django Templates
- **Version Control:** Git and GitHub

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/subi-07/SmartBasket-Django.git
cd SmartBasket-Django
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Set up the database

```bash
python manage.py migrate
python manage.py seed_demo
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

## 🔐 Admin Dashboard

Create an administrator account:

```bash
python manage.py createsuperuser
```

Then open **http://127.0.0.1:8000/admin/** and sign in.

## 📝 Notes

- Demo checkout is provided for testing; no real payment gateway is integrated.
- The project is intended for learning and demonstration purposes.
- Before production deployment, configure secure environment variables, production settings, and a suitable production database.

## 👩‍💻 Author

**Subithra R**

Developed as a learning project to practise Python, Django, database models, user authentication, and web application development.
