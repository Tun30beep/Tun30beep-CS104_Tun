from flask import Flask, render_template, request, redirect
import sqlite3

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
# ADD ORDER
# =========================
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():

    conn = get_db_connection()

    menu_items = conn.execute(
        'SELECT * FROM menu_items'
    ).fetchall()

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        table_name = request.form['table_name']

        item_id = request.form['item_id']
        quantity = request.form['quantity']
        total_price = request.form['total_price']
        status = request.form['status']

        # ======================
        # CUSTOMER
        # ======================
        customer = conn.execute("""

            SELECT customer_id
            FROM customers

            WHERE name = ?

        """, (customer_name,)).fetchone()

        if customer:

            customer_id = customer[0]

        else:

            last_customer = conn.execute("""

                SELECT MAX(customer_id)
                FROM customers

            """).fetchone()

            if last_customer[0] is None:

                customer_id = 1

            else:

                customer_id = last_customer[0] + 1

            conn.execute("""

                INSERT INTO customers
                (
                    customer_id,
                    name
                )

                VALUES (?, ?)

            """, (
                customer_id,
                customer_name
            ))


        # ======================
        # TABLE
        # ======================
        table = conn.execute("""

            SELECT table_id
            FROM restaurant_tables

            WHERE table_number = ?

        """, (table_name,)).fetchone()

        if table:

            table_id = table[0]

        else:

            last_table = conn.execute("""

                SELECT MAX(table_id)
                FROM restaurant_tables

            """).fetchone()

            if last_table[0] is None:

                table_id = 1

            else:

                table_id = last_table[0] + 1

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
                table_id,
                table_name,
                4,
                'Available'
            ))


        # ======================
        # ORDER ID
        # ======================
        last_order = conn.execute("""

            SELECT MAX(order_id)
            FROM orders

        """).fetchone()

        if last_order[0] is None:

            order_id = 1

        else:

            order_id = last_order[0] + 1


        # ======================
        # INSERT ORDER
        # ======================
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


        # ======================
        # INSERT ORDER ITEM
        # ======================
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
            order_id,
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
        menu_items=menu_items
    )


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

        table_name = request.form['table_name']
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
            table_name,
            capacity,
            status
        ))

        conn.commit()

        conn.close()

        return redirect('/restaurant_tables')

    return render_template('add_table.html')


# =========================
# EDIT TABLE
# =========================
@app.route('/edit_table/<int:table_id>', methods=['GET', 'POST'])
def edit_table(table_id):

    conn = get_db_connection()

    table = conn.execute("""

        SELECT *
        FROM restaurant_tables

        WHERE table_id = ?

    """, (table_id,)).fetchone()

    if request.method == 'POST':

        table_name = request.form['table_name']
        capacity = request.form['capacity']
        status = request.form['status']

        conn.execute("""

            UPDATE restaurant_tables

            SET
                table_number = ?,
                capacity = ?,
                status = ?

            WHERE table_id = ?

        """, (
            table_name,
            capacity,
            status,
            table_id
        ))

        conn.commit()

        conn.close()

        return redirect('/restaurant_tables')

    conn.close()

    return render_template(
        'edit_table.html',
        table=table
    )


# =========================
# DELETE TABLE
# =========================
@app.route('/delete_table/<int:table_id>')
def delete_table(table_id):

    conn = get_db_connection()

    conn.execute("""

        DELETE FROM restaurant_tables

        WHERE table_id = ?

    """, (table_id,))

    conn.commit()

    conn.close()

    return redirect('/restaurant_tables')


# =========================
# RUN APP
# =========================
if __name__ == '__main__':

    app.run(debug=True)
