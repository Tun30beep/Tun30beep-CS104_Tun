# =========================
# DASHBOARD
# =========================
@app.route('/')
def index():

    conn = get_db_connection()

    # ======================
    # ORDERS
    # ======================
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


    # ======================
    # CUSTOMERS
    # ======================
    customers = conn.execute("""

        SELECT *
        FROM customers

        ORDER BY customer_id DESC

        LIMIT 5

    """).fetchall()


    conn.close()

    return render_template(
        'index.html',
        orders=orders,
        customers=customers
    )
