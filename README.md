# Restaurant Management System

A web-based Restaurant Management System developed using Flask and SQLite.
This project supports full CRUD operations for restaurant management including customers, employees, menu items, tables, and food orders.

---

# Features

* Dashboard with Latest Orders
* Customer Management
* Employee Management
* Menu Management
* Restaurant Table Management
* Order Management
* Full CRUD Operations
* SQLite Database Integration
* SQL JOIN Queries
* Real-time Database Updates
* Responsive UI using HTML and CSS

---

# Technologies Used

## Frontend

* HTML
* CSS

## Backend

* Python Flask

## Database

* SQLite

## Deployment

* PythonAnywhere

## Version Control

* GitHub

---

# Database Structure

The system contains 6 main tables:

* customers
* employees
* restaurant_tables
* menu_items
* orders
* order_items

The project uses:

* Primary Keys
* Foreign Keys
* LEFT JOIN Queries

to connect data between tables.

---

# CRUD Operations

The system supports:

## Create

* Add Customer
* Add Employee
* Add Menu
* Add Table
* Add Order

## Read

* View Dashboard
* View Customers
* View Employees
* View Menu
* View Tables
* View Orders

## Update

* Edit Customers
* Edit Employees
* Edit Menu
* Edit Tables
* Edit Orders

## Delete

* Delete Customers
* Delete Employees
* Delete Menu
* Delete Tables
* Delete Orders

---

# SQL JOIN Example

```sql
SELECT
    o.order_id,
    c.name,
    rt.table_number,
    mi.item_name,
    o.total_price,
    o.status

FROM orders o

LEFT JOIN customers c
ON o.customer_id = c.customer_id

LEFT JOIN restaurant_tables rt
ON o.table_id = rt.table_id

LEFT JOIN order_items oi
ON o.order_id = oi.order_id

LEFT JOIN menu_items mi
ON oi.item_id = mi.item_id

ORDER BY o.order_id DESC;
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Tun30beep/Tun30beep-CS104_Tun.git
```

## Enter Project Folder

```bash
cd Tun30beep-CS104_Tun
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

---

# Project Structure

```text
Tun30beep-CS104_Tun/
│
├── app.py
├── database.db
├── requirements.txt
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── customers.html
│   ├── employees.html
│   ├── menu.html
│   ├── restaurant_tables.html
│   ├── add_order.html
│   └── ...
```

---

# Deployment

Application deployed on PythonAnywhere:

https://tun999.pythonanywhere.com/

---

# GitHub Repository

https://github.com/Tun30beep/Tun30beep-CS104_Tun

---

# Developed By

Tun30beep

---

# License

This project is developed for educational purposes.

