from django.urls import path
from .views import checkout, listar_pedidos, detalle_pedido, eliminar_pedido

urlpatterns = [
    path('', listar_pedidos, name='listar_pedidos'),
    path('checkout/', checkout, name='checkout'),
    path('<int:pedido_id>/eliminar/', eliminar_pedido, name='eliminar_pedido'),
    path('<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
]