from django.urls import path
from orders.views import OrderPageView, charge

urlpatterns = [
    path('', OrderPageView.as_view(), name='orders'),
    path('charge/', charge, name='charge')
]