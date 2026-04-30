import os
from decimal import Decimal
from collections import OrderedDict
from datetime import date
import requests
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from .models import Transaction, Budget


GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'


TRANSLATIONS = {
    'en': {
        'app_name': 'Finance AI',
        'dashboard': 'Dashboard',
        'expenses': 'Expenses',
        'income': 'Income',
        'reports': 'Reports',
        'settings': 'Settings',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'financial_overview': 'Financial Overview',
        'monthly_income': 'Monthly Income',
        'monthly_expenses': 'Monthly Expenses',
        'estimated_savings': 'Estimated Savings',
        'forecast': 'Forecast',
        'ask_ai': 'Ask AI for Advice',
        'save_transaction': 'Save Transaction',
        'save_budget': 'Save Budget',
        'language': 'Language',
    },
    'km': {
        'app_name': 'ហិរញ្ញវត្ថុ AI',
        'dashboard': 'ផ្ទាំងគ្រប់គ្រង',
        'expenses': 'ចំណាយ',
        'income': 'ចំណូល',
        'reports': 'របាយការណ៍',
        'settings': 'ការកំណត់',
        'login': 'ចូលគណនី',
        'register': 'បង្កើតគណនី',
        'logout': 'ចាកចេញ',
        'financial_overview': 'ទិដ្ឋភាពហិរញ្ញវត្ថុ',
        'monthly_income': 'ចំណូលប្រចាំខែ',
        'monthly_expenses': 'ចំណាយប្រចាំខែ',
        'estimated_savings': 'ប្រាក់សន្សំប្រហែល',
        'forecast': 'ការព្យាករណ៍',
        'ask_ai': 'សួរ AI សម្រាប់ដំបូន្មាន',
        'save_transaction': 'រក្សាទុកប្រតិបត្តិការ',
        'save_budget': 'រក្សាទុកថវិកា',
        'language': 'ភាសា',
    },
}


def get_language(request):
    return request.session.get('language', 'en')


def get_translations(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en'])


def _month_key(d: date) -> str:
    return d.strftime('%Y-%m')


def build_financial_summary(user):
    today = timezone.localdate()
    month_start = today.replace(day=1)

    expenses_qs = Transaction.objects.filter(user=user, transaction_type='expense', transaction_date__gte=month_start, transaction_date__lte=today)
    income_qs = Transaction.objects.filter(user=user, transaction_type='income', transaction_date__gte=month_start, transaction_date__lte=today)

    monthly_expenses = expenses_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    monthly_income = income_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    savings = monthly_income - monthly_expenses

    top_expenses = list(expenses_qs.values('category').annotate(total=Sum('amount')).order_by('-total')[:5])
    budgets = list(Budget.objects.filter(user=user, month=month_start).values('category', 'monthly_limit'))

    return {
        'month': month_start.strftime('%B %Y'),
        'monthly_income': float(monthly_income),
        'monthly_expenses': float(monthly_expenses),
        'estimated_savings': float(savings),
        'top_expenses': top_expenses,
        'budgets': budgets,
        'recent_transactions': list(
            Transaction.objects.filter(user=user).values('transaction_type', 'title', 'category', 'amount', 'transaction_date').order_by('-transaction_date', '-created_at')[:8]
        ),
    }


def build_monthly_trends(user, months=6):
    rows = Transaction.objects.filter(user=user).annotate(month=TruncMonth('transaction_date')).values('month', 'transaction_type').annotate(total=Sum('amount')).order_by('month')
    series = OrderedDict()
    today = timezone.localdate().replace(day=1)
    for offset in range(months - 1, -1, -1):
        month = today.month - offset
        year = today.year
        while month <= 0:
            month += 12
            year -= 1
        month_date = date(year, month, 1)
        series[_month_key(month_date)] = {'label': month_date.strftime('%b %Y'), 'income': 0.0, 'expense': 0.0}
    for row in rows:
        if row['month'] is None:
            continue
        key = _month_key(row['month'])
        if key in series:
            series[key][row['transaction_type']] = float(row['total'] or 0)
    return list(series.values())


def build_forecast(user, future_months=3):
    trends = build_monthly_trends(user, months=6)
    if not trends:
        return []
    avg_income = sum(m['income'] for m in trends) / max(len(trends), 1)
    avg_expense = sum(m['expense'] for m in trends) / max(len(trends), 1)
    base = timezone.localdate().replace(day=1)
    forecast = []
    month = base.month
    year = base.year
    for _ in range(future_months):
        month += 1
        if month > 12:
            month = 1
            year += 1
        month_date = date(year, month, 1)
        forecast.append({
            'label': month_date.strftime('%b %Y'),
            'predicted_income': round(avg_income, 2),
            'predicted_expense': round(avg_expense, 2),
            'predicted_savings': round(avg_income - avg_expense, 2),
        })
    return forecast


def generate_ai_advice(user, user_question: str, language='en'):
    api_key = os.getenv('GEMINI_API_KEY', '').strip()
    summary = build_financial_summary(user)
    forecast = build_forecast(user)

    language_prompt = 'Respond in Khmer.' if language == 'km' else 'Respond in English.'
    prompt = f'''
You are a helpful personal finance advisor for a web application.
Give practical, simple, and safe guidance.
Avoid pretending to be a licensed financial planner.
{language_prompt}
Use the user's data summary and forecast below.
Return concise bullet points with action steps.

User data summary:
{summary}

Forecast:
{forecast}

User question:
{user_question}
'''

    if not api_key:
        answer = (
            'Gemini API key is not configured yet.\n\n'
            'Demo advice based on your current data:\n'
            f"- This month income: ${summary['monthly_income']:.2f}\n"
            f"- This month expenses: ${summary['monthly_expenses']:.2f}\n"
            f"- Estimated savings: ${summary['estimated_savings']:.2f}\n"
            '- Set GEMINI_API_KEY in your .env file to enable live AI advice.'
        )
        if language == 'km':
            answer = (
                'មិនទាន់បានកំណត់ Gemini API key នៅឡើយទេ។\n\n'
                'ដំបូន្មានសាកល្បងផ្អែកលើទិន្នន័យបច្ចុប្បន្ន៖\n'
                f"- ចំណូលខែនេះ: ${summary['monthly_income']:.2f}\n"
                f"- ចំណាយខែនេះ: ${summary['monthly_expenses']:.2f}\n"
                f"- ប្រាក់សន្សំប្រហែល: ${summary['estimated_savings']:.2f}\n"
                '- សូមកំណត់ GEMINI_API_KEY ក្នុង .env ដើម្បីប្រើ AI ពិតប្រាកដ។'
            )
        return {'success': True, 'answer': answer}

    response = requests.post(
        f'{GEMINI_URL}?key={api_key}',
        json={'contents': [{'parts': [{'text': prompt}]}]},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    text = data['candidates'][0]['content']['parts'][0]['text']
    return {'success': True, 'answer': text}
