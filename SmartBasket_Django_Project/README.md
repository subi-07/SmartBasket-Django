# SmartBasket — Smart Grocery Shopping System

A Django + SQLite grocery-store web application built as a student portfolio project. It includes a product catalogue, search/filter, session-based basket, user accounts, stock-aware checkout, order history, admin product management, low-stock labels, and lower-priced alternatives grouped by the shop.

## Requirements
- Python 3.10+
- pip

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ . Admin: http://127.0.0.1:8000/admin/

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

## Main features
1. Product catalogue with keyword search and category filtering.
2. Session basket with quantity updates/removal.
3. User sign-up and login.
4. Stock validation during add-to-basket and checkout; stock decrements after successful order.
5. Order history and order-status field.
6. Django admin for categories, products, and orders.
7. **Budget-aware alternatives:** admin can assign the same `swap_group` to comparable products; the detail page suggests in-stock items in that group with a lower price.
8. Low-stock label when stock is between 1 and 5.

## Demo notes / limitations
- Checkout is a simulation; no payment gateway, delivery integration, email, or real inventory sync is configured.
- The `SECRET_KEY` is for local development only. Do not deploy with `DEBUG=True` or the sample key.
- Product alternatives are rule-based, not AI-generated. They rely on the admin's `swap_group` value.
- This project is a portfolio learning build. Understand and test the code before describing it in an interview.

## Interview-ready explanation (say only after you have run and understood it)
“SmartBasket is a Django-based grocery shopping web app. I used Django models for products, categories, orders and order items, SQLite for local persistence, Django authentication for accounts, and sessions for the shopping basket. One feature I focused on is stock-aware checkout: before saving an order, the application validates quantities against current stock, then records the order and reduces inventory in a database transaction. I also added rule-based lower-priced alternatives using an admin-defined product group, plus low-stock indicators.”

## Resume bullet (after you personally run and verify the project)
**SmartBasket | Python, Django, SQLite, HTML/CSS**
- Built a grocery shopping web app with searchable product listings, category filters, user authentication, basket management, and order history.
- Implemented stock validation at checkout and inventory updates within a database transaction.
- Added rule-based lower-priced product alternatives and low-stock indicators to support budget-aware shopping.

## Before putting it on your resume
- Run it yourself and verify every feature.
- Change the sample products or styling so the final project reflects your own choices.
- Be prepared to explain models, sessions, authentication, transactions, and how the alternative suggestion works.
- Do not claim AI/ML or payment integration; neither is implemented here.
