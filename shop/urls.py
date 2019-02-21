from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.shop_detail),
    path('new/', views.shop_new),
    # path('<int:pk>/edit/', views.shop_edit),
    # path('<int:pk>/delete/', views.shop_delete),
]
