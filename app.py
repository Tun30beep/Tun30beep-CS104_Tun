from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'


# =========================================
# DATABASE CONNECTION
# =========================================
def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================
# DASHBOARD
# =========================================
@app.route('/')
def index():

    conn = get_db_connection()

    orders = conn.execute("""

        SELECT
            o.order_id,
            c.name AS customer_name,
            rt.table_number,
            o.total_price,
            o.status

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN restaurant_tables rt
            ON o.table_id = rt.table_id

        ORDER BY o.order_id DESC

    """).fetchall()

    conn.close()

    return render_template(
        'index.html',
        orders=orders
    )


# =========================================
# MENU PAGE
# =========================================
@app.route('/menu')
def menu():

    conn = get_db_connection()

    menu_items = conn.execute("""
        SELECT * FROM menu_items
    """).fetchall()

    conn.close()

    return render_template(
        'menu.html',
        menu_items=menu_items
    )


# =========================================
# CUSTOMER LIST
# =========================================
@app.route('/customers')
def customers():

    conn = get_db_connection()

    customer_list = conn.execute("""
        SELECT * FROM customers
    """).fetchall()

    conn.close()

    return render_template(
        'customers.html',
        customers=customer_list
    )


# =========================================
# ADD CUSTOMER
# =========================================
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    if request.method == 'POST':

        name = request.form['name']

        phone = request.form['phone']

        email = request.form['email']

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO customers
            (name, phone, email)
            VALUES (?, ?, ?)
        """, (
            name,
            phone,
            email
        ))

        conn.commit()

        conn.close()

        return redirect('/customers')

    return render_template('add_customer.html')


# =========================================
# ADD ORDER
# =========================================
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():

    conn = get_db_connection()

    customers = conn.execute("""
        SELECT * FROM customers
    """).fetchall()

    if request.method == 'POST':

        order_id = request.form['order_id']

        customer_id = request.form['customer_id']

        table_input = request.form['table_id']

        quantity = request.form['quantity']

        total_price = request.form['total_price']

        status = request.form['status']

        # INSERT TABLE
        conn.execute("""
            INSERT INTO restaurant_tables
            (table_number, capacity, status)
            VALUES (?, ?, ?)
        """, (
            table_input,
            4,
            'occupied'
        ))

        conn.commit()

        # GET LAST TABLE ID
        table_row = conn.execute("""
            SELECT table_id
            FROM restaurant_tables
            ORDER BY table_id DESC
            LIMIT 1
        """).fetchone()

        table_id = table_row['table_id']

        # INSERT ORDER
        conn.execute("""
            INSERT INTO orders
            (
                order_id,
                customer_id,
                employee_id,
                table_id,
                total_price,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            customer_id,
            1,
            table_id,
            total_price,
            status
        ))

        conn.commit()

        conn.close()

        return redirect('/')

    conn.close()

    return render_template(
        'add_order.html',
        customers=customers
    )


# =========================================
# ADD MENU
# =========================================
@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':

        item_name = request.form['item_name']

        category = request.form['category']

        price = request.form['price']

        stock = request.form['stock']

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO menu_items
            (item_name, category, price, stock)
            VALUES (?, ?, ?, ?)
        """, (
            item_name,
            category,
            price,
            stock
        ))

        conn.commit()

        conn.close()

        return redirect('/menu')

    return render_template('add.html')


# =========================================
# EDIT MENU
# =========================================
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):

    conn = get_db_connection()

    item = conn.execute("""
        SELECT * FROM menu_items
        WHERE item_id = ?
    """, (item_id,)).fetchone()

    if request.method == 'POST':

        item_name = request.form['item_name']

        category = request.form['category']

        price = request.form['price']

        stock = request.form['stock']

        conn.execute("""
            UPDATE menu_items
            SET
                item_name = ?,
                category = ?,
                price = ?,
                stock = ?
            WHERE item_id = ?
        """, (
            item_name,
            category,
            price,
           stock,
            item_id
        ))

        conn.commit()

        conn.close()

        return redirect('/menu')

    conn.close()

    return render_template(
        'edit.html',
        item=item
    )


# =========================================
# DELETE MENU
# =========================================
@app.route('/delete/<int:item_id>')
def delete(item_id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM menu_items
        WHERE item_id = ?
    """, (item_id,))

    conn.commit()

    conn.close()

    return redirect('/menu')


# =========================================
# RUN FLASK
# =========================================
if __name__ == '__main__':

    app.run(debug=True)