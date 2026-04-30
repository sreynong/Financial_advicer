from django.conf import settings
from django.db import models


class OwnedModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)ss")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Transaction(OwnedModel):
    TRANSACTION_TYPES = (
        ('expense', 'Expense'),
        ('income', 'Income'),
    )

    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('housing', 'Housing'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health'),
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('education', 'Education'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    transaction_date = models.DateField()

    class Meta:
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Budget(OwnedModel):
    category = models.CharField(max_length=30)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.DateField(help_text='Use the first day of the month')

    class Meta:
        unique_together = ('user', 'category', 'month')
        ordering = ['-month', 'category']

    def __str__(self):
        return f"{self.category}: {self.monthly_limit}"
