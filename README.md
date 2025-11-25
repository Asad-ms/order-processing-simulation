# Order Processing & Subscription Management Simulation

**A small, beginner-friendly Python + SQLite simulation that demonstrates basic order lifecycle, subscription management, validation checks and simple operational reporting.**

---

## Demo
This repository contains a simple CLI/demo script that:
- creates customers, products and orders
- updates order status
- creates and cancels subscriptions
- validates orders for missing references or invalid status
- generates a tabular operational report

---

## Files
- `order_system.py` — main Python script (functions + demo run)
- `schema.sql` — SQLite schema for customers, products, orders, subscriptions
- `demo.db` — sample database created by the demo (optional)
- `sample_run.txt` — console output captured from a demo run
- `README.md` — this file

---

## Tech
- Python 3 (no external dependencies)
- SQLite (built-in)
- Works on macOS / Linux / Windows

---

## Quick start (run locally)
1. (Optional) create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
# or  .\venv\Scripts\Activate.ps1  # Windows PowerShell
