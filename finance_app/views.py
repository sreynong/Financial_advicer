from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import AIQuestionForm, BudgetForm, TransactionForm, RegisterForm
from .models import Budget, Transaction
from .services import (
    build_financial_summary,
    build_forecast,
    build_monthly_trends,
    generate_ai_advice,
    get_language,
    get_translations,
)


def _dashboard_context(request):
    summary = build_financial_summary(request.user)
    today = timezone.localdate()
    month_start = today.replace(day=1)
    lang = get_language(request)

    category_breakdown = list(
        Transaction.objects.filter(user=request.user, transaction_type='expense', transaction_date__gte=month_start, transaction_date__lte=today)
        .values('category').annotate(total=Sum('amount')).order_by('-total')
    )

    return {
        'summary': summary,
        'category_breakdown': category_breakdown,
        'recent_transactions': Transaction.objects.filter(user=request.user)[:10],
        'budgets': Budget.objects.filter(user=request.user, month=month_start),
        'transaction_form': TransactionForm(),
        'budget_form': BudgetForm(initial={'month': month_start}),
        'ai_form': AIQuestionForm(),
        'trend_data': build_monthly_trends(request.user),
        'forecast_data': build_forecast(request.user),
        'ui': get_translations(lang),
        'current_language': lang,
    }


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'finance_app/dashboard.html', _dashboard_context(request))


@login_required
def expenses_view(request):
    expenses = Transaction.objects.filter(user=request.user, transaction_type='expense')
    return render(request, 'finance_app/transactions.html', {'title': 'Expenses', 'transactions': expenses, 'ui': get_translations(get_language(request)), 'current_language': get_language(request)})


@login_required
def income_view(request):
    incomes = Transaction.objects.filter(user=request.user, transaction_type='income')
    return render(request, 'finance_app/transactions.html', {'title': 'Income', 'transactions': incomes, 'ui': get_translations(get_language(request)), 'current_language': get_language(request)})


@login_required
def reports_view(request):
    context = _dashboard_context(request)
    return render(request, 'finance_app/reports.html', context)


@login_required
def settings_view(request):
    return render(request, 'finance_app/settings.html', {'ui': get_translations(get_language(request)), 'current_language': get_language(request)})



class CustomLoginView(LoginView):
    template_name = 'finance_app/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = get_language(self.request)
        context.update({'ui': get_translations(lang), 'current_language': lang})
        return context

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Welcome! Your account has been created.')
        return redirect('dashboard')
    return render(request, 'finance_app/register.html', {'form': form, 'ui': get_translations(get_language(request)), 'current_language': get_language(request)})


def set_language(request, language_code):
    if language_code in ['en', 'km']:
        request.session['language'] = language_code
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            tx.save()
            messages.success(request, 'Transaction saved successfully.')
        else:
            messages.error(request, 'Please correct the transaction form.')
    return redirect('dashboard')


@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget saved successfully.')
        else:
            messages.error(request, 'Please correct the budget form.')
    return redirect('dashboard')


@login_required
def ai_advice(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST request required.'}, status=405)

    form = AIQuestionForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False, 'error': 'Question is required.'}, status=400)

    try:
        result = generate_ai_advice(request.user, form.cleaned_data['question'], language=get_language(request))
        return JsonResponse(result)
    except Exception as exc:
        return JsonResponse({'success': False, 'error': str(exc)}, status=500)
