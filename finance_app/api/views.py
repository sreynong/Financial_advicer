from rest_framework import permissions, viewsets
from finance_app.models import Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer


class UserOwnedQuerysetMixin:
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(UserOwnedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    model = Transaction


class BudgetViewSet(UserOwnedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    model = Budget
