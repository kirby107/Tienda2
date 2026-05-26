from django.shortcuts import redirect, get_object_or_404
from productos.models import Producto
from django.shortcuts import render

def agregar_carrito(request, producto_id):

    carrito = request.session.get('carrito', {})

    producto = get_object_or_404(Producto, id=producto_id)

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1
        }

    request.session['carrito'] = carrito

    print(carrito)

    return redirect('productos')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})

    print("Carrito:",carrito)

    total = 0
    for item in carrito.values():
        total += item['precio'] * item['cantidad']

    return render(request, 'carrito/carrito.html', {
        'carrito': carrito,
        'total': total
    })

def eliminar_carrito(request, producto_id):

    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]

    request.session['carrito'] = carrito

    return redirect('ver_carrito')

def carrito_count(request):
    carrito = request.session.get('carrito', {})
    return {
        'cart_count': sum(item['cantidad'] for item in carrito.values())
    }

def sumar_producto(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def restar_producto(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] -= 1

        if carrito[str(producto_id)]['cantidad'] <= 0:
            del carrito[str(producto_id)]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')