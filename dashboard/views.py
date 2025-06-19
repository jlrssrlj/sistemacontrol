from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Empleado,Producto, Venta, DetalleVenta, MedioPago,Rol
from .services.listar_ventas import listar_ventas
from .services.usuario_service import UsuarioService
from .forms import UsuarioEmpleadoForm
from django.contrib.auth.models import User
from dashboard.decorators import rol_requerido
from django.utils.decorators import method_decorator
from functools import wraps
from .vistas.views_rol import Rol_views
from .vistas.views_mediopago import Mediopago_views
from .vistas.views_proveedor import Proveedores_views
from .vistas.views_gastos import Gastos_views
from .vistas.views_categoria import Categorias_views
from .vistas.views_arqueo import Arqueo_views
from .vistas.views_productos import Producto_views



@require_http_methods(["GET","POST"])
def principal(request):
    return render(request,'index.html')

@login_required
def no_autorizado(request):
    return render(request, 'no_autorizado.html')


def admin(user):
    return user.is_superuser or user.is_staff

def solo_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')

        # Permitir acceso a superusuarios y usuarios con is_staff
        if user.is_superuser or user.is_staff:
            return view_func(request, *args, **kwargs)

        try:
            empleado = Empleado.objects.get(user=user)
            if empleado.rol.nombre.lower() == 'admin':
                return view_func(request, *args, **kwargs)
        except Empleado.DoesNotExist:
            pass  # Continuamos a redirección

        return redirect('no_autorizado')
    return _wrapped_view

@login_required
@solo_admin
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "El usuario ya existe")
            else:
                user = UsuarioService.crear_usuario_empleado(form.cleaned_data)
                messages.success(request, f"Empleado {user.get_full_name()} creado correctamente")
                return redirect('listar_empleado')
    else:
        form = UsuarioEmpleadoForm()

    return render(request, 'crear_usuario.html', {'form': form})

@login_required
def listar_empleado(request):
    empleados = UsuarioService.obtener_empleados()
    return render(request, "listar_empleados.html", {'empleados': empleados})

@login_required
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)

    if request.method == 'POST':
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'activo': request.POST.get('activo') == 'on',
            'rol': get_object_or_404(Rol, id=request.POST.get('rol')) if request.POST.get('rol') else None,
            'is_staff': request.POST.get('is_staff') == 'on'
        }
        UsuarioService.actualizar_usuario_empleado(empleado, data, request.user.is_superuser)
        messages.success(request, 'Empleado actualizado correctamente.')
        return redirect('listar_empleado')

    roles = UsuarioService.obtener_roles()
    return render(request, 'editar_empleado.html', {'empleado': empleado, 'roles': roles})

@login_required
def eliminar_empleado(request, id):
    if request.method == 'POST':
        UsuarioService.eliminar_empleado(id)
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('listar_empleado')

    empleado = get_object_or_404(Empleado, id=id)
    return render(request, 'confirmar_eliminacion.html', {'empleado': empleado})

@require_http_methods(["GET","POST"])
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('ventas')
        else:
            error = "usuairo o contraseña incorrecto"
    return render(request, 'login.html',{'error':error})

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('home')



from django.utils import timezone
from dashboard.models import Empleado, Venta, DetalleVenta, Producto, MedioPago, Arqueo
from django.contrib import messages

@login_required
@rol_requerido('admin', 'cajero')
def crear_venta(request):
    productos = Producto.objects.filter(stock__gt=0).order_by('nombre')
    medios_pago = MedioPago.objects.all()

    if request.method == 'POST':
        medio_pago_id = request.POST.get('medio_pago')
        if not medio_pago_id:
            messages.error(request, "Por favor selecciona un medio de pago.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        try:
            medio_pago = MedioPago.objects.get(id=medio_pago_id)
        except MedioPago.DoesNotExist:
            messages.error(request, "Medio de pago inválido.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        productos_venta = []
        total = 0
        for key in request.POST.keys():
            if key.startswith('producto_id_'):
                prod_id = request.POST[key]
                cantidad_key = f'cantidad_{prod_id}'
                try:
                    cantidad = int(request.POST.get(cantidad_key, 1))
                    producto = Producto.objects.get(id=prod_id)
                    if cantidad > producto.stock:
                        messages.error(request, f"No hay suficiente stock para {producto.nombre}.")
                        return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})
                    subtotal = producto.precio * cantidad
                    total += subtotal
                    productos_venta.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
                except (Producto.DoesNotExist, ValueError):
                    messages.error(request, "Datos de producto inválidos.")
                    return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        if not productos_venta:
            messages.error(request, "No has agregado productos a la venta.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        empleado = Empleado.objects.get(user=request.user)

        # Obtener arqueo abierto del empleado
        arqueo_abierto = Arqueo.objects.filter(empleado=empleado, fecha_fin__isnull=True).first()
        if not arqueo_abierto:
            messages.error(request, "No tienes un arqueo abierto. Debes abrir un arqueo antes de registrar ventas.")
            return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})

        # Crear la venta con arqueo y medio de pago
        venta = Venta.objects.create(
            empleado=empleado,
            arqueo=arqueo_abierto,
            total=total,
            medio_pago=medio_pago,
            fecha=timezone.now(),
        )

        for item in productos_venta:
            DetalleVenta.objects.create(
                venta=venta,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['producto'].precio
            )
            # Actualiza stock
            item['producto'].stock -= item['cantidad']
            item['producto'].save()

        messages.success(request, f"Venta registrada exitosamente. Total: ${total:.2f}")
        return redirect('ventas')

    return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})


@method_decorator(rol_requerido('admin'), name='dispatch')
class historial_ventas(LoginRequiredMixin, ListView):
    template_name = 'historial_ventas.html'
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        return Venta.objects.select_related('empleado__user', 'cliente', 'medio_pago') \
                            .prefetch_related('detalles__producto') \
                            .order_by('-fecha')
    


Arqueo_views.listar_arqueo
Arqueo_views.eliminar_arqueo
Arqueo_views.crear_arqueo
Arqueo_views.cerrar_arqueo

Categorias_views.listar_categoria
Categorias_views.editar_categoria
Categorias_views.eliminar_categoria
Categorias_views.crear_categoria


Gastos_views.listar_gatos
Gastos_views.crear_gasto
Gastos_views.eliminar_gasto
Gastos_views.editar_gasto



Proveedores_views.listar_proveedores
Proveedores_views.editar_proveedor
Proveedores_views.crear_proveedor
Proveedores_views.eliminar_proveedor



Mediopago_views.listar_mediopago
Mediopago_views.editar_mediopago
Mediopago_views.crear_mediopago
Mediopago_views.eliminar_mediopago
 
Rol_views.listar_rol
Rol_views.crear_rol
Rol_views.editar_rol
Rol_views.editar_rol

