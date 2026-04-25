# Hardware Shop Final - Intelligent Hardware-Focused E-Commerce (Django)

This final project demonstrates:

- Catalog management with dynamic hardware specifications stored in JSON
- Compatibility-oriented product suggestions using explicit links and heuristic matching
- Session-based cart workflow
- Draft and submitted order lifecycle
- Fulfillment logic that selects inventory, supplier, or manufacturing
- Inventory management with optional serial-level traceability
- Pricing/procurement and manufacturing dashboards
- Basic warranty / RMA workflow
- REST API with JWT and DRF token authentication routes
- Demo-ready payment, shipping, and tax estimate integrations
- Automated Django coverage with 13 passing tests

## Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py loaddata fixtures/demo_data.json
python manage.py createsuperuser
python manage.py runserver
```

## Key Pages

- Home: http://127.0.0.1:8000/
- Products: http://127.0.0.1:8000/catalog/products/
- Cart: http://127.0.0.1:8000/cart/
- Orders: http://127.0.0.1:8000/orders/
- RMA: http://127.0.0.1:8000/rma/
- Inventory dashboard: http://127.0.0.1:8000/inventory/dashboard/
- Pricing dashboard: http://127.0.0.1:8000/pricing/dashboard/
- Manufacturing dashboard: http://127.0.0.1:8000/manufacturing/dashboard/
- API root: http://127.0.0.1:8000/api/
- API docs: http://127.0.0.1:8000/api/docs/

## Verification

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Submission Notes

- Demo data is provided in `fixtures/demo_data.json` so the project does not depend on a bundled SQLite database snapshot.
- Payment, shipping, and tax are implemented as demo-ready stubs. They support quote and estimate workflows and can be replaced with real credentials later.
- The API includes JWT and DRF token issuance plus a protected `/api/auth/me/` endpoint. Main resource endpoints remain open in development for easier review.
- If you run the project from a cloud-synced folder such as OneDrive and SQLite reports locking or disk I/O issues, copy the project to a normal local folder before running migrations.
- The report source lives in `CPSC_597__Project_Seminar_Project_Report/main.tex`.
