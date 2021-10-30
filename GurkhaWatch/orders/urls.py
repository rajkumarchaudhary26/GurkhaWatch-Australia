from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(),
         name='create-checkout-session'),
    path('payment-success/', views.paymentSuccess,
         name='payment-success'),
    path('payment-cancel/', views.paymentCancel,
         name='payment-cancel'),
    path('webhook/stripe/', views.my_webhook_view,
         name='webhook-stripe'),
]
