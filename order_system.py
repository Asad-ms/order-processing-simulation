
"""Order Processing & Subscription Management Simulation
Files:
- SQLite DB (demo.db)
- order_system.py (this script)
Functions:
- init_db(db_path)
- create_customer(...)
- create_product(...)
- create_order(...)
- update_order_status(...)
- create_subscription(...)
- cancel_subscription(...)
- validate_orders(...)
- generate_report(...)
Simple CLI demo at bottom.
"""
import sqlite3
from datetime import datetime, timedelta

def init_db(db_path="demo.db"):
    conn = sqlite3.connect(db_path)
    with open("schema.sql","r") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn

def create_customer(conn, name, email=None):
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (customer_name, email) VALUES (?,?)", (name,email))
    conn.commit()
    return cur.lastrowid

def create_product(conn, name, ptype="data_feed"):
    cur = conn.cursor()
    cur.execute("INSERT INTO products (product_name, product_type) VALUES (?,?)", (name,ptype))
    conn.commit()
    return cur.lastrowid

def create_order(conn, customer_id, product_id, comment=None):
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    status = "Processing"
    cur.execute("INSERT INTO orders (customer_id, product_id, created_at, status, comment) VALUES (?,?,?,?,?)",
                (customer_id, product_id, created_at, status, comment))
    conn.commit()
    return cur.lastrowid

def update_order_status(conn, order_id, new_status, comment=None):
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = ?, comment = ? WHERE order_id = ?", (new_status, comment, order_id))
    conn.commit()
    return cur.rowcount

def create_subscription(conn, order_id, months=1):
    cur = conn.cursor()
    start = datetime.utcnow().date()
    end = (start + timedelta(days=30*months)).isoformat()
    cur.execute("INSERT INTO subscriptions (order_id, start_date, end_date, active) VALUES (?,?,?,1)", (order_id, start.isoformat(), end))
    conn.commit()
    return cur.lastrowid

def cancel_subscription(conn, subscription_id):
    cur = conn.cursor()
    cur.execute("UPDATE subscriptions SET active = 0 WHERE subscription_id = ?", (subscription_id,))
    conn.commit()
    return cur.rowcount

def validate_orders(conn):
    """Simple validation: check for orders with missing customer or product references or invalid status"""
    cur = conn.cursor()
    issues = []
    cur.execute("SELECT order_id, customer_id, product_id, status FROM orders")
    for order_id, customer_id, product_id, status in cur.fetchall():
        # check customer exists
        c = cur.execute("SELECT 1 FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
        if not c:
            issues.append((order_id, 'Missing customer'))
        p = cur.execute("SELECT 1 FROM products WHERE product_id = ?", (product_id,)).fetchone()
        if not p:
            issues.append((order_id, 'Missing product'))
        if status not in ('Processing','Completed','Failed','Cancelled'):
            issues.append((order_id, f'Invalid status: {status}'))
    return issues

def generate_report(conn):
    cur = conn.cursor()
    cur.execute("""SELECT o.order_id, c.customer_name, p.product_name, o.created_at, o.status, o.comment
                   FROM orders o
                   JOIN customers c ON o.customer_id = c.customer_id
                   JOIN products p ON o.product_id = p.product_id
                   ORDER BY o.order_id""")
    rows = cur.fetchall()
    report_lines = []
    report_lines.append(["OrderID","Customer","Product","CreatedAt","Status","Comment"])
    for r in rows:
        report_lines.append(list(r))
    return report_lines

if __name__ == '__main__':
    # demo run
    db_path = 'demo.db'
    conn = init_db(db_path)
    # create sample customers/products
    cust1 = create_customer(conn, 'Shaik Mohammed Asad', 'mohammedasad.0319@gmail.com')
    cust2 = create_customer(conn, 'Test Customer', 'test@example.com')
    prod1 = create_product(conn, 'Market Data Feed', 'data_feed')
    prod2 = create_product(conn, 'Index Subscription', 'subscription')
    # create orders
    o1 = create_order(conn, cust1, prod1, 'Initial order for data feed')
    o2 = create_order(conn, cust2, prod2, 'Subscription order')
    # create subscription for order 2
    s1 = create_subscription(conn, o2, months=3)
    # update statuses
    update_order_status(conn, o1, 'Completed', 'Provisioned successfully')
    update_order_status(conn, o2, 'Processing', 'Waiting for billing validation')
    # intentionally create a bad order to show validation
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_id, product_id, created_at, status, comment) VALUES (?,?,?,?,?)", (999,999, datetime.utcnow().isoformat(), 'UnknownStatus', 'bad refs'))
    conn.commit()
    # run validation and report
    issues = validate_orders(conn)
    report = generate_report(conn)
    print('--- ISSUES ---')
    for i in issues:
        print(i)
    print('\n--- REPORT ---')
    for line in report:
        print(line)
