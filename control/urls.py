from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),

    # users 
    path('ctrl_users/', views.ctrl_users, name='ctrl_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('ctrl_users/update/<user_id>', views.update_user, name='update_user'),
    path('ctrl_user/details/<user_id>', views.user_details, name='user_details'),

    # accounts 
    path('accounts/', views.AccountListView.as_view(), name='accounts'),
    path('accounts/update/<int:id>', views.update_account, name='update_account'),
    path('accounts/delete/<int:pk>', views.AccountDeleteView.as_view(), name='delete_account'),

    # transactions 
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transactions/update/<int:id>', views.update_transaction, name='transaction_update'),

    # profile 
    path('admin_profile', views.admin_profile, name='admin_profile'),
]