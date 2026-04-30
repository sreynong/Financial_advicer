from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(choices=[('expense', 'Expense'), ('income', 'Income')], max_length=10)),
                ('category', models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('housing', 'Housing'), ('entertainment', 'Entertainment'), ('health', 'Health'), ('salary', 'Salary'), ('freelance', 'Freelance'), ('investment', 'Investment'), ('education', 'Education'), ('utilities', 'Utilities'), ('other', 'Other')], max_length=30)),
                ('title', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('notes', models.TextField(blank=True)),
                ('transaction_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-transaction_date', '-created_at']},
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=30)),
                ('monthly_limit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('month', models.DateField(help_text='Use the first day of the month')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-month', 'category'], 'unique_together': {('user', 'category', 'month')}},
        ),
    ]
