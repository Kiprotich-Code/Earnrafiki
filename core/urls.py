from django.urls import path
from . import views

# urlpatterns 
urlpatterns = [
    path('', views.home, name='home'),
    path('user_home/', views.user_home, name='user_home'),

    # accounts
    path('acc_details/', views.acc_details, name='acc_details'),

    # transactions 
    path('account/deposit/', views.deposit_view, name='deposit'),
    path('account/withdraw/', views.withdraw_view, name='withdraw'),
    path('account/transactions/', views.transaction_history_view, name='transaction_history'),

    # users
    path('my_profile', views.my_profile, name='my_profile'),
]