
# Order Processing & Subscription Management Simulation

A small, beginner-friendly Python + SQLite project that simulates:
- creating customers, products, and orders
- updating order status
- creating and cancelling subscriptions
- validating orders for missing references or invalid status
- generating a simple report

Files:
- schema.sql : SQL schema for tables
- demo.db : sample SQLite database (created by running the demo)
- order_system.py : main script (contains functions + demo run)
- sample_run.txt : console output from a demo run

How to run:
1. (Optional) Create a Python virtual environment
2. Run: `python3 order_system.py`
3. The script will create `demo.db` in the same folder and print a validation report.

This project is intentionally simple so you can add it to your resume quickly and explain it in interviews.
