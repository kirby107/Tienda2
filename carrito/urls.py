from django.urls import path
from . import views

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('', views.ver_carrito, name='ver_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('sumar/<int:producto_id>/', views.sumar_producto, name='sumar_producto'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar_producto'),
]