from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('webhook/set/', views.set_webhook, name='set_webhook'),
    path('webhook/delete/', views.delete_webhook, name='delete_webhook'),
]

