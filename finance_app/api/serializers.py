from rest_framework import serializers
from finance_app.models import Transaction, Budget


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'category', 'title', 'amount', 'notes', 'transaction_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'monthly_limit', 'month', 'created_at']
        read_only_fields = ['id', 'created_at']
