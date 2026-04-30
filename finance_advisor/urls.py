from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from finance_app import views
from finance_app.api.views import BudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register('transactions', TransactionViewSet, basename='api-transactions')
router.register('budgets', BudgetViewSet, basename='api-budgets')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('income/', views.income_view, name='income'),
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings_view, name='settings'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('set-language/<str:language_code>/', views.set_language, name='set_language'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('ai/advice/', views.ai_advice, name='ai_advice'),
    path('api/', include(router.urls)),
]
