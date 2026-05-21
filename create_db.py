import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()


# =========================
# CUSTOMERS
# =========================
cursor.execute("""

CREATE TABLE customers (

    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    phone TEXT,

    email TEXT

)

""")


# =========================
# EMPLOYEES
# =========================
cursor.execute("""

CREATE TABLE employees (

    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    role TEXT,

    phone TEXT

)

""")


# =========================
# RESTAURANT TABLES
# =========================
cursor.execute("""

CREATE TABLE restaurant_tables (

    table_id INTEGER PRIMARY KEY AUTOINCREMENT,

    table_number INTEGER,

    capacity INTEGER,

    status TEXT

)

""")


# =========================
# MENU ITEMS
# =========================
cursor.execute("""

CREATE TABLE menu_items (

    item_id INTEGER PRIMARY KEY AUTOINCREMENT,

    item_name TEXT,

    category TEXT,

    price REAL,

    stock INTEGER

)

""")


# =========================
# ORDERS
# =========================
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


# =========================
# ORDER ITEMS
# =========================
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


# ======================================================
# INSERT CUSTOMERS (10)
# ======================================================
customers = [

("John", "0811111111", "john@gmail.com"),
("Alice", "0822222222", "alice@gmail.com"),
("Mike", "0833333333", "mike@gmail.com"),
("Sarah", "0844444444", "sarah@gmail.com"),
("Tom", "0855555555", "tom@gmail.com"),
("Emma", "0866666666", "emma@gmail.com"),
("James", "0877777777", "james@gmail.com"),
("Lisa", "0888888888", "lisa@gmail.com"),
("David", "0899999999", "david@gmail.com"),
("Anna", "0800000000", "anna@gmail.com")

]

cursor.executemany("""

INSERT INTO customers
(name, phone, email)

VALUES (?, ?, ?)

""", customers)


# ======================================================
# INSERT EMPLOYEES (10)
# ======================================================
employees = [

("Robert", "Cashier", "0911111111"),
("Jennifer", "Chef", "0922222222"),
("Alex", "Manager", "0933333333"),
("Ben", "Waiter", "0944444444"),
("Chris", "Chef", "0955555555"),
("Daniel", "Cashier", "0966666666"),
("Eva", "Waiter", "0977777777"),
("Frank", "Chef", "0988888888"),
("Grace", "Manager", "0999999999"),
("Helen", "Waiter", "0900000000")

]

cursor.executemany("""

INSERT INTO employees
(name, role, phone)

VALUES (?, ?, ?)

""", employees)


# ======================================================
# INSERT RESTAURANT TABLES (10)
# ======================================================
tables = [

(1, 2, "available"),
(2, 4, "occupied"),
(3, 6, "reserved"),
(4, 2, "available"),
(5, 4, "occupied"),
(6, 8, "available"),
(7, 2, "reserved"),
(8, 6, "occupied"),
(9, 4, "available"),
(10, 10, "occupied")

]

cursor.executemany("""

INSERT INTO restaurant_tables
(table_number, capacity, status)

VALUES (?, ?, ?)

""", tables)


# ======================================================
# INSERT MENU ITEMS (10)
# ======================================================
menu_items = [

("Pizza", "Food", 299, 50),
("Burger", "Food", 199, 30),
("Coke", "Drink", 39, 100),
("Pasta", "Food", 259, 40),
("Steak", "Food", 599, 15),
("Salad", "Food", 149, 25),
("Coffee", "Drink", 79, 80),
("Tea", "Drink", 59, 70),
("Ice Cream", "Dessert", 99, 35),
("Orange Juice", "Drink", 89, 60)

]

cursor.executemany("""

INSERT INTO menu_items
(item_name, category, price, stock)

VALUES (?, ?, ?, ?)

""", menu_items)


# ======================================================
# INSERT ORDERS (10)
# ======================================================
orders = [

(1,1,1,338,"paid"),
(2,2,2,199,"pending"),
(3,3,3,450,"paid"),
(4,4,4,520,"pending"),
(5,5,5,299,"paid"),
(6,6,6,799,"pending"),
(7,7,7,120,"paid"),
(8,8,8,220,"pending"),
(9,9,9,159,"paid"),
(10,10,10,650,"pending")

]

cursor.executemany("""

INSERT INTO orders
(customer_id, employee_id, table_id, total_price, status)

VALUES (?, ?, ?, ?, ?)

""", orders)


# ======================================================
# INSERT ORDER ITEMS (10)
# ======================================================
order_items = [

(1,1,1,299),
(2,2,1,199),
(3,3,2,78),
(4,4,1,259),
(5,5,1,599),
(6,6,2,298),
(7,7,1,79),
(8,8,3,177),
(9,9,2,198),
(10,10,1,89)

]

cursor.executemany("""

INSERT INTO order_items
(order_id, item_id, quantity, subtotal)

VALUES (?, ?, ?, ?)

""", order_items)


conn.commit()

conn.close()

print("Database created successfully with 60 records!")
