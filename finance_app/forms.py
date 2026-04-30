from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Transaction, Budget


class DateInput(forms.DateInput):
    input_type = 'date'


class StyledFormMixin:
    def apply_bootstrap(self):
        for _, field in self.fields.items():
            cls = 'form-control'
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                cls = 'form-select'
            field.widget.attrs['class'] = f"{field.widget.attrs.get('class', '')} {cls}".strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class TransactionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'title', 'category', 'amount', 'transaction_date', 'notes']
        widgets = {
            'transaction_date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional note'}),
        }


class BudgetForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit', 'month']
        widgets = {
            'month': DateInput(),
        }


class AIQuestionForm(StyledFormMixin, forms.Form):
    question = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ask about budgeting, saving, investing, or spending habits...'}))


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput())
