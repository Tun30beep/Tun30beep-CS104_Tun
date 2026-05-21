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
