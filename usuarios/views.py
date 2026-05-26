from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from usuarios.decorators import role_required
from productos.models import Producto, Promocion
from pedidos.models import Pedido


def registro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rol = request.POST.get("rol", "cliente")

        if password1 != password2:
            return render(request, "usuarios/registro.html", {
                "error": "Las contraseñas no coinciden."
            })

        if rol not in ["cliente", "vendedor", "admin"]:
            rol = "cliente"

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password1,
            rol=rol
        )

        login(request, user)
        return redirect('productos')

    return render(request, "usuarios/registro.html")


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('productos')
        else:
            error = "Credenciales incorrectas"

    return render(request, "usuarios/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect('login')


@role_required(['admin'])
def admin_panel(request):
    usuarios = Usuario.objects.order_by('username')
    promociones = Promocion.objects.all().order_by('-id')
    pedidos = Pedido.objects.all()

    reportes = {
        'total_usuarios': usuarios.count(),
        'total_productos': Producto.objects.count(),
        'total_pedidos': pedidos.count(),
        'pendientes': pedidos.filter(estado='pendiente').count(),
        'enviados': pedidos.filter(estado='enviado').count(),
        'entregados': pedidos.filter(estado='entregado').count(),
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'actualizar_rol':
            usuario_id = request.POST.get('usuario_id')
            nuevo_rol = request.POST.get('rol')
            if nuevo_rol in ['cliente', 'vendedor', 'admin']:
                try:
                    usuario = Usuario.objects.get(id=usuario_id)
                    usuario.rol = nuevo_rol
                    usuario.save()
                except Usuario.DoesNotExist:
                    pass
            return redirect('panel_admin')

        if action == 'crear_promocion':
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            descuento = request.POST.get('descuento') or 0
            activo = request.POST.get('activo') == 'on'
            if nombre:
                Promocion.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    descuento=descuento,
                    activo=activo,
                )
            return redirect('panel_admin')

        if action == 'eliminar_promocion':
            promo_id = request.POST.get('promocion_id')
            Promocion.objects.filter(id=promo_id).delete()
            return redirect('panel_admin')

    return render(request, 'admin/panel.html', {
        'reportes': reportes,
        'usuarios': usuarios,
        'promociones': promociones,
    })