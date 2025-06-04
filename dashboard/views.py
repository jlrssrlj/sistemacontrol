from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Empleado,Gasto, Proveedor, Arqueo,Producto, Venta, DetalleVenta, MedioPago,Rol, Categoria
from .services.listar_ventas import listar_ventas
from .services.usuario_service import UsuarioService
from .services.arqueo_service import ArqueoService
from .services.listar_producto import ProductoService
from .services.categoria_service import CategoriaService
from .services.gastos_service import GastosService
from .services.listar_proveedores import Proveedor
from .services.mediopago_service import MediopagoService
from .services.rol_service import Rolservice
from .forms import UsuarioEmpleadoForm
from django.contrib.auth.models import User
from dashboard.decorators import rol_requerido
from django.utils.decorators import method_decorator
from functools import wraps
from .models import Proveedor
from .forms import ProveedorForm



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



@login_required
@rol_requerido('admin', 'cajero')
def crear_venta(request):
    productos = Producto.objects.filter(stock__gt=0).order_by('nombre')
    medios_pago = MedioPago.objects.all()  # Carga los medios de pago desde BD

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

        # Crear la venta con medio de pago
        venta = Venta.objects.create(
            empleado=empleado,
            total=total,
            medio_pago=medio_pago,  # Aquí se guarda correctamente
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
        return redirect('ventas')  # Asegúrate de que esta URL exista

    # Si es GET
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
    
def producto_list(request):
    return render(request,'listar_producto.html')

@login_required
def crear_arqueo(request):
    if request.method == 'POST':
        monto_inicial = request.POST.get('monto_inicial')
        
        try:
            monto_inicial = float(monto_inicial)
        except ValueError:
            return render(request,'crear_arqueo.html')
        
        empleado = request.user.empleado

        data ={
            'monto_inicial': monto_inicial,
            'empleado': empleado
        }

        ArqueoService.crear_arqueo(data)
        return redirect('listar_arqueos')
    return render(request,'crear_arqueo.html')

@login_required

def cerrar_arqueo(request, id):
    arqueo = ArqueoService.obtener_arqueo(id)

    if request.method == 'POST':
        monto_final = request.POST.get('monto_final')
        try:
            monto_final = float(monto_final)
            ArqueoService.cerrar_arqueo(id, monto_final)
            return redirect('listar_arqueos')  
        except ValueError:
            return render(request, 'cerrar_arqueo.html', {
                'arqueo': arqueo,
                'error': 'El monto final debe ser un número válido.'
            })

    return render(request, 'cerrar_arqueo.html', {
        'arqueo': arqueo
    })


@login_required
def listar_arqueo(request):
    arqueos = ArqueoService.listar_arqueos()
    context = {
        'arqueos': arqueos,
    }
    return render(request,'listar_arqueos.html',context)

@login_required
def eliminar_arqueo(request, id):
    arqueo = ArqueoService.eliminar_arqueo(id)

    if request.method == 'POST':
        ArqueoService.eliminar_arqueo(id)
        return redirect('listar_arqueo')
    return render(request,'confirmacion_eliminacion_arqueo.html', {'arqueo':arqueo})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        print(f"Categoria ID recibida: {categoria_id}")  # <-- Depuración

        data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'precio': request.POST.get('precio'),
            'stock': request.POST.get('stock'),
            'categoria_id': categoria_id
        }

        ProductoService.crear_producto(data)
        messages.success(request, 'Producto creado correctamente.')
        return redirect('listar_producto')

    categorias = Categoria.objects.all()
    return render(request, 'crear_producto.html', {'categorias': categorias})



@login_required
def listar_producto(request):
    producto = ProductoService.listar_producto()
    return render(request, 'listar_producto.html', {'producto': producto})


@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'precio': request.POST.get('precio'),
            'stock': request.POST.get('stock'),
            'categoria_id': request.POST.get('categoria_id')
        }
        ProductoService.actualizar_producto(producto.id, data)
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('listar_producto')

    categorias = Categoria.objects.all()
    return render(request, 'editar_producto.html', {'producto': producto, 'categorias': categorias})


@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        ProductoService.eliminar_producto(id)
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('listar_producto')

    return render(request, 'confirmar_eliminacion_producto.html', {'producto': producto})

@login_required
def listar_categoria(request):
    categorias = CategoriaService.listar_categoria()
    print("Categorias en vista:", categorias)
    return render(request, 'listar_categoria.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            CategoriaService.crear_categoria({'nombre':nombre})
            return redirect('listar_categoria')
    return render(request,'crear_categoria.html')

@login_required
def editar_categoria(request, categoria_id):
    categoria = CategoriaService.obtener_categoria(categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            
            CategoriaService.editar_categoria(categoria_id, {'nombre': nombre})
            return redirect('listar_categoria')

    return render(request, 'editar_categoria.html', {'categoria': categoria})

from django.views.decorators.http import require_POST

@login_required
@require_POST
def eliminar_categoria(request, categoria_id):
    try:
        CategoriaService.eliminar_categoria(categoria_id)
        
    except Exception:
        messages.error(request, 'Error al eliminar la categoría.')
    return redirect('listar_categoria')


@login_required
def listar_gatos(request):
    gastos = GastosService.listar_gastos()
    return render(request, 'listar_gastos.html', {'gastos': gastos})


@login_required
def crear_gasto(request):
    if request.method == 'POST':
        empleado = Empleado.objects.get(user=request.user)

        arqueo_abierto = Arqueo.objects.filter(empleado=empleado, fecha_fin__isnull=True).first()
        if not arqueo_abierto:
            messages.error(request, "Debe tener un arqueo abierto para registrar un gasto.")
            return redirect('listar_arqueos')

        data = {
            'empleado': empleado,
            'proveedor': Proveedor.objects.get(id=request.POST['proveedor']),
            'concepto': request.POST['concepto'],
            'monto': request.POST['monto'],
            'arqueo': arqueo_abierto
        }

        GastosService.crear_gastos(data)
        messages.success(request, "Gasto registrado exitosamente.")
        return redirect('listar_gastos')

    proveedores = Proveedor.objects.all()
    return render(request, 'crear_gastos.html', {
        'proveedores': proveedores
    })


@login_required
def editar_gasto(request, id):
    gasto = GastosService.obtener_gasto(id)

    if request.method == 'POST':
        data = {
            'empleado': Empleado.objects.get(id=request.POST['empleado']),
            'proveedor': Proveedor.objects.get(id=request.POST['proveedor']),
            'concepto': request.POST['concepto'],
            'monto': request.POST['monto'],
            'arqueo': Arqueo.objects.get(id=request.POST['arqueo']),
        }
        GastosService.editar_gasto(id, data)
        messages.success(request, "Gasto editado correctamente.")
        return redirect('listar_gastos')

    empleados = Empleado.objects.all()
    proveedores = Proveedor.objects.all()
    arqueos = Arqueo.objects.all()

    return render(request, 'editar_gasto.html', {
        'gasto': gasto,
        'empleados': empleados,
        'proveedores': proveedores,
        'arqueos': arqueos,
    })


@login_required
def eliminar_gasto(request, id):
    if request.method == 'POST':
        GastosService.eliminar_gasto(id)
        messages.success(request, "Gasto eliminado correctamente.")
    return redirect('listar_gastos')


def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'listar_proveedores.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'crear_proveedor.html', {'form': form})

def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'crear_proveedor.html', {'form': form})

def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    return redirect('listar_proveedores')

def listar_mediopago(request):
    pagos = MediopagoService.listar_mediopago()
    return render(request, 'mediopago/listar_mediopago.html',{'pagos': pagos})

def crear_mediopago(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            MediopagoService.crear_mediopago({'nombre': nombre})
            return redirect('listar_medio_pago')
        else:
            return render(request, 'mediopago/crear_mediopago.html',{'error': 'El nombre es obligatorio'})
    
    return render(request, 'mediopago/crear_mediopago.html')


def editar_mediopago(request, id):
    pago = get_object_or_404(MediopagoService.listar_mediopago(), id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            MediopagoService.editar_mediopago(id, {'nombre': nombre})
            return redirect('listar_medio_pago')  
        else:
            return render(request, 'mediopago/editar_mediopago.html', {
                'pago': pago,
                'error': 'El nombre es obligatorio'
            })

    return render(request, 'mediopago/editar_mediopago.html', {'pago': pago})

def eliminar_mediopago(request,id):
    if request.method == 'POST':
        MediopagoService.eliminar_mediopago(id)
        return redirect('listar_medio_pago')
    pago = get_object_or_404(MediopagoService.listar_mediopago(), id=id)
    return render(request, 'mediopago/eliminar_mediopago.html',{'pago':pago})

def listar_rol(request):
    rol = Rolservice.listar_rol()
    return render(request, 'rol/listar_rol.html',{'rol': rol})

def crear_rol(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            Rolservice.crear_rol({'nombre': nombre})
            return redirect('listar_rol')
        else:
            return render(request, 'rol/crear_rol.html',{'error': 'El nombre es obligatorio'})
    
    return render(request, 'rol/crear_rol.html')


def editar_rol(request, id):
    rol = get_object_or_404(Rolservice.listar_rol(), id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            Rolservice.editar_rol(id, {'nombre': nombre})
            return redirect('listar_rol')  
        else:
            return render(request, 'rol/editar_rol.html', {
                'rol': rol,
                'error': 'El nombre es obligatorio'
            })

    return render(request, 'rol/editar_rol.html', {'rol': rol})

def eliminar_rol(request,id):
    if request.method == 'POST':
        Rolservice.eliminar_rol(id)
        return redirect('listar_rol')
    rol = get_object_or_404(Rolservice.listar_rol(), id=id)
    return render(request, 'rol/eliminar_rol.html',{'rol':rol})


