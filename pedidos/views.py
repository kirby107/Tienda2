from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto, Promocion
from .models import Pedido, DetallePedido


@login_required(login_url='/usuarios/login/')
def checkout(request):
    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('ver_carrito')

    items = []
    total = Decimal('0')
    promociones = Promocion.objects.filter(activo=True)
    selected_promocion = None
    discount = Decimal('0')

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=int(producto_id))
        subtotal = Decimal(item['precio']) * item['cantidad']
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'precio': item['precio'],
            'subtotal': subtotal,
        })

    promocion_id = request.POST.get('promocion') if request.method == 'POST' else request.GET.get('promocion')
    if promocion_id:
        selected_promocion = Promocion.objects.filter(id=promocion_id, activo=True).first()
        if selected_promocion:
            discount = total * selected_promocion.descuento / Decimal('100')

    total_final = total - discount

    if request.method == 'POST':
        pedido = Pedido.objects.create(usuario=request.user, promocion=selected_promocion)

        detalles = []
        for item in items:
            detalles.append(DetallePedido(
                pedido=pedido,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio=item['precio'],
            ))

        DetallePedido.objects.bulk_create(detalles)
        request.session['carrito'] = {}

        return redirect('detalle_pedido', pedido_id=pedido.id)

    return render(request, 'pedidos/checkout.html', {
        'items': items,
        'total': total,
        'promociones': promociones,
        'selected_promocion': selected_promocion,
        'discount': discount,
        'total_final': total_final,
    })


@login_required(login_url='/usuarios/login/')
def listar_pedidos(request):
    if request.user.rol in ['vendedor', 'admin']:
        pedidos = Pedido.objects.all().order_by('-fecha')
    else:
        pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'pedidos/listar_pedidos.html', {
        'pedidos': pedidos,
    })


@login_required(login_url='/usuarios/login/')
def eliminar_pedido(request, pedido_id):
    if request.user.rol != 'admin':
        return redirect('listar_pedidos')

    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')

    return redirect('detalle_pedido', pedido_id=pedido.id)


@login_required(login_url='/usuarios/login/')
def detalle_pedido(request, pedido_id):
    if request.user.rol == 'cliente':
        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    else:
        pedido = get_object_or_404(Pedido, id=pedido_id)

    detalles = DetallePedido.objects.filter(pedido=pedido)
    total = sum(detalle.precio * detalle.cantidad for detalle in detalles)
    descuento = Decimal('0')
    total_final = total

    if pedido.promocion:
        descuento = total * pedido.promocion.descuento / Decimal('100')
        total_final = total - descuento

    if request.method == 'POST' and request.user.rol in ['vendedor', 'admin']:
        nuevo_estado = request.POST.get('estado')
        estados_validos = dict(Pedido.ESTADOS)
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save()
            return redirect('detalle_pedido', pedido_id=pedido.id)

    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'total': total,
        'descuento': descuento,
        'total_final': total_final,
        'estados': Pedido.ESTADOS,
        'is_staff': request.user.rol in ['vendedor', 'admin'],
    })