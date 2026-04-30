from django.contrib import admin
from .models import Transaction, Budget


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'transaction_type', 'category', 'amount', 'transaction_date')
    list_filter = ('transaction_type', 'category', 'transaction_date')
    search_fields = ('title', 'notes', 'user__username')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'monthly_limit', 'month')
    list_filter = ('month', 'category')
    search_fields = ('user__username', 'category')
