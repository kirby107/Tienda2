from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from usuarios.decorators import role_required
from .models import Producto, Categoria, Promocion

def lista_productos(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    promociones = Promocion.objects.filter(activo=True)

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'query': query,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'promociones': promociones,
    })


@role_required(['vendedor', 'admin'])
def crear_producto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio = float(request.POST.get('precio') or 0)
        stock = int(request.POST.get('stock') or 0)
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
        )

        return redirect('productos')

    return render(request, 'productos/crear.html', {
        'categorias': categorias,
    })


@role_required(['vendedor', 'admin'])
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', '').strip()
        producto.descripcion = request.POST.get('descripcion', '').strip()
        producto.precio = float(request.POST.get('precio') or 0)
        producto.stock = int(request.POST.get('stock') or 0)
        categoria_id = request.POST.get('categoria')
        producto.categoria = get_object_or_404(Categoria, id=categoria_id)
        producto.save()
        return redirect('productos')

    return render(request, 'productos/editar.html', {
        'producto': producto,
        'categorias': categorias,
    })

def tienda(request):
    categoria_id = request.GET.get('categoria')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, "productos/tienda.html", {
        "productos": productos,
        "categorias": categorias
    })