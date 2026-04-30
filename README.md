# AI Personal Finance Advisor

A Django web app for personal finance management with Gemini-powered financial advice, budget planning, reports, charts, REST API endpoints, login/register, and Khmer language support.

## Features

- User authentication: register, login, logout
- Expense and income tracking
- Monthly budgets
- Dashboard with category chart and monthly trend chart
- Simple 3-month financial forecast
- Gemini API integration for financial advice
- REST API for transactions and budgets
- English / Khmer interface switcher
- PostgreSQL-ready setup, with optional SQLite for quick local testing

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap, Chart.js
- Backend: Django + Django REST Framework + Gemini API
- Database: PostgreSQL

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your Gemini key and database settings.

## Run migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Main URLs

- `/register/` - create account
- `/login/` - sign in
- `/dashboard/` - main dashboard
- `/api/transactions/` - REST API for transactions
- `/api/budgets/` - REST API for budgets

## Gemini notes

If `GEMINI_API_KEY` is not set, the app returns demo advice instead of failing.

## API usage

After logging in through the browser, open:

- `/api/transactions/`
- `/api/budgets/`

You can also use Django session auth or HTTP basic auth.
