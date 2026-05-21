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
# ADD EMPLOYEE
# =========================
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():

    if request.method == 'POST':

        name = request.form['name']
        role = request.form['role']
        phone = request.form['phone']

        conn = get_db_connection()

        conn.execute("""

            INSERT INTO employees
            (name, role, phone)

            VALUES (?, ?, ?)

        """, (
            name,
            role,
            phone
        ))

        conn.commit()

        conn.close()

        return redirect('/employees')

    return render_template('add_employee.html')


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
