import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# =========================================
# CUSTOMERS
# =========================================
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

# =========================================
# EMPLOYEES
# =========================================
cursor.execute("""
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    phone TEXT
)
""")

# =========================================
# RESTAURANT TABLES
# =========================================
cursor.execute("""
CREATE TABLE restaurant_tables (
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    status TEXT NOT NULL
)
""")

# =========================================
# MENU ITEMS
# =========================================
cursor.execute("""
CREATE TABLE menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

# =========================================
# ORDERS
# =========================================
cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    employee_id INTEGER,
    table_id INTEGER,
    total_price REAL,
    status TEXT,

    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id),

    FOREIGN KEY(table_id)
        REFERENCES restaurant_tables(table_id)
)
""")

# =========================================
# ORDER ITEMS
# =========================================
cursor.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    subtotal REAL,

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY(item_id)
        REFERENCES menu_items(item_id)
)
""")

# =========================================
# INSERT MOCK DATA
# =========================================

cursor.execute("""
INSERT INTO customers
(name, phone, email)
VALUES
('John', '0811111111', 'john@gmail.com'),
('Alice', '0822222222', 'alice@gmail.com')
""")

cursor.execute("""
INSERT INTO employees
(name, role, phone)
VALUES
('Robert', 'Cashier', '0911111111'),
('Jennifer', 'Chef', '0922222222')
""")

cursor.execute("""
INSERT INTO restaurant_tables
(table_number, capacity, status)
VALUES
(1, 4, 'available'),
(2, 2, 'occupied')
""")

cursor.execute("""
INSERT INTO menu_items
(item_name, category, price, stock)
VALUES
('Pizza', 'Food', 299, 50),
('Burger', 'Food', 199, 30),
('Coke', 'Drink', 39, 100)
""")

cursor.execute("""
INSERT INTO orders
(customer_id, employee_id, table_id, total_price, status)
VALUES
(1, 1, 1, 338, 'paid'),
(2, 1, 2, 199, 'pending')
""")

conn.commit()

conn.close()

print("Database created successfully!")