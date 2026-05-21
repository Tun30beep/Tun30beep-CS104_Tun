from flask import Flask, render_template, request, redirect
import sqlite3

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

DATABASE = 'database.db'


# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# =========================
# DASHBOARD
# =========================
@app.route('/')
def index():

    conn = get_db_connection()

    orders = conn.execute("""

        SELECT
            o.order_id,
            c.name,
            rt.table_number,
            mi.item_name,
            o.total_price,
            o.status

        FROM orders o

        JOIN customers c
        ON o.customer_id = c.customer_id

        JOIN restaurant_tables rt
        ON o.table_id = rt.table_id

        JOIN order_items oi
        ON o.order_id = oi.order_id

        JOIN menu_items mi
        ON oi.item_id = mi.item_id

        ORDER BY o.order_id DESC

    """).fetchall()

    conn.close()

    return render_template(
        'index.html',
        orders=orders
    )


# =========================
# MENU PAGE
# =========================
@app.route('/menu')
def menu():

    conn = get_db_connection()

    menu_items = conn.execute(
        'SELECT * FROM menu_items'
    ).fetchall()

    conn.close()

    return render_template(
        'menu.html',
        menu_items=menu_items
    )


# =========================
# ADD MENU
# =========================
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():

    if request.method == 'POST':

        item_name = request.form['item_name']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']

        conn = get_db_connection()

        last_item = conn.execute("""

            SELECT MAX(item_id)
            FROM menu_items

        """).fetchone()

        if last_item[0] is None:

            new_id = 1

        else:

            new_id = last_item[0] + 1

        conn.execute("""

            INSERT INTO menu_items
            (
                item_id,
                item_name,
                category,
                price,
                stock
            )

            VALUES (?, ?, ?, ?, ?)

        """, (
            new_id,
            item_name,
            category,
            price,
            stock
        ))

        conn.commit()

        conn.close()

        return redirect('/menu')

    return render_template('add_menu.html')


# =========================
# EDIT MENU
# =========================
@app.route('/edit_menu/<int:item_id>', methods=['GET', 'POST'])
def edit_menu(item_id):

    conn = get_db_connection()

    item = conn.execute("""

        SELECT *
        FROM menu_items

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
        'edit_menu.html',
        item=item
    )


# =========================
# DELETE MENU
# =========================
@app.route('/delete_menu/<int:item_id>')
def delete_menu(item_id):

    conn = get_db_connection()

    conn.execute("""

        DELETE FROM menu_items

        WHERE item_id = ?

    """, (item_id,))

    conn.commit()

    conn.close()

    return redirect('/menu')


# =========================
# CUSTOMERS PAGE
# =========================
@app.route('/customers')
def customers_page():

    conn = get_db_connection()

    customers = conn.execute(
        'SELECT * FROM customers'
    ).fetchall()

    conn.close()

    return render_template(
        'customers.html',
        customers=customers
    )


# =========================
# ADD CUSTOMER
# =========================
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = get_db_connection()

        last_customer = conn.execute("""

            SELECT MAX(customer_id)
            FROM customers

        """).fetchone()

        if last_customer[0] is None:

            new_id = 1

        else:

            new_id = last_customer[0] + 1

        conn.execute("""

            INSERT INTO customers
            (
                customer_id,
                name,
                phone,
                email
            )

            VALUES (?, ?, ?, ?)

        """, (
            new_id,
            name,
            phone,
            email
        ))

        conn.commit()

        conn.close()

        return redirect('/customers')

    return render_template('add_customer.html')


# =========================
# EDIT CUSTOMER
# =========================
@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):

    conn = get_db_connection()

    customer = conn.execute("""

        SELECT *
        FROM customers

        WHERE customer_id = ?

    """, (customer_id,)).fetchone()

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn.execute("""

            UPDATE customers

            SET
                name = ?,
                phone = ?,
                email = ?

            WHERE customer_id = ?

        """, (
            name,
            phone,
            email,
            customer_id
        ))

        conn.commit()

        conn.close()

        return redirect('/customers')

    conn.close()

    return render_template(
        'edit_customer.html',
        customer=customer
    )


# =========================
# DELETE CUSTOMER
# =========================
@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):

    conn = get_db_connection()

    conn.execute("""

        DELETE FROM customers

        WHERE customer_id = ?

    """, (customer_id,))

    conn.commit()

    conn.close()

    return redirect('/customers')


# =========================
# EMPLOYEES PAGE
# =========================
@app.route('/employees')
def employees():

    conn = get_db_connection()

    employees = conn.execute(
        'SELECT * FROM employees'
    ).fetchall()

    conn.close()

    return render_template(
        'employees.html',
        employees=employees
    )


# =========================
# ADD EMPLOYEE
# =========================
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():

    if request.method == 'POST':

        name = request.form['name']
        role = request.form['role']
        phone = request.form['phone']

        conn = get_db_connection()

        last_employee = conn.execute("""

            SELECT MAX(employee_id)
            FROM employees

        """).fetchone()

        if last_employee[0] is None:

            new_id = 1

        else:

            new_id = last_employee[0] + 1

        conn.execute("""

            INSERT INTO employees
            (
                employee_id,
                name,
                role,
                phone
            )

            VALUES (?, ?, ?, ?)

        """, (
            new_id,
            name,
            role,
            phone
        ))

        conn.commit()

        conn.close()

        return redirect('/employees')

    return render_template('add_employee.html')


# =========================
# RESTAURANT TABLES
# =========================
@app.route('/restaurant_tables')
def restaurant_tables():

    conn = get_db_connection()

    tables = conn.execute(
        'SELECT * FROM restaurant_tables'
    ).fetchall()

    conn.close()

    return render_template(
        'restaurant_tables.html',
        tables=tables
    )


# =========================
# ADD TABLE
# =========================
@app.route('/add_table', methods=['GET', 'POST'])
def add_table():

    if request.method == 'POST':

        table_number = request.form['table_number']
        capacity = request.form['capacity']
        status = request.form['status']

        conn = get_db_connection()

        last_table = conn.execute("""

            SELECT MAX(table_id)
            FROM restaurant_tables

        """).fetchone()

        if last_table[0] is None:

            new_id = 1

        else:

            new_id = last_table[0] + 1

        conn.execute("""

            INSERT INTO restaurant_tables
            (
                table_id,
                table_number,
                capacity,
                status
            )

            VALUES (?, ?, ?, ?)

        """, (
            new_id,
            table_number,
            capacity,
            status
        ))

        conn.commit()

        conn.close()

        return redirect('/restaurant_tables')

    return render_template('add_table.html')


# =========================
# ADD ORDER
# =========================
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():

    conn = get_db_connection()

    customers = conn.execute(
        'SELECT * FROM customers'
    ).fetchall()

    tables = conn.execute(
        'SELECT * FROM restaurant_tables'
    ).fetchall()

    menu_items = conn.execute(
        'SELECT * FROM menu_items'
    ).fetchall()

    if request.method == 'POST':

        customer_id = request.form['customer_id']
        table_id = request.form['table_id']
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        total_price = request.form['total_price']
        status = request.form['status']

        last_order = conn.execute("""

            SELECT MAX(order_id)
            FROM orders

        """).fetchone()

        if last_order[0] is None:

            new_order_id = 1

        else:

            new_order_id = last_order[0] + 1

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
            new_order_id,
            customer_id,
            1,
            table_id,
            total_price,
            status
        ))

        conn.execute("""

            INSERT INTO order_items
            (
                order_id,
                item_id,
                quantity,
                subtotal
            )

            VALUES (?, ?, ?, ?)

        """, (
            new_order_id,
            item_id,
            quantity,
            total_price
        ))

        conn.commit()

        conn.close()

        return redirect('/')

    conn.close()

    return render_template(
        'add_order.html',
        customers=customers,
        tables=tables,
        menu_items=menu_items
    )


# =========================
# RUN APP
# =========================
if __name__ == '__main__':

    app.run(debug=True)
