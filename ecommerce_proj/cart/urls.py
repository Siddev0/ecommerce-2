from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/<str:type>/', views.update_cart, name="update"),
    path('remove/<int:product_id>/', views.remove_from_cart, name="remove_from_cart"),
]