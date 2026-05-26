from django.urls import path
from .views import lista_productos, crear_producto, editar_producto

urlpatterns = [
    path('', lista_productos, name='productos'),
    path('crear/', crear_producto, name='crear_producto'),
    path('editar/<int:producto_id>/', editar_producto, name='editar_producto'),
]