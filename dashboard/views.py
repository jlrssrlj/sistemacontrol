from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Venta, DetalleVenta, Empleado

from dashboard.models import Empleado, Arqueo, Producto, Venta, DetalleVenta
from .services.venta_services import VentaService



@require_http_methods(["GET","POST"])
def principal(request):
    return render(request,'index.html')

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

@require_http_methods(["GET","POST"])
def ventas(request):
    return render(request, 'ventas.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from dashboard.models import Empleado, Arqueo, Producto, Venta, DetalleVenta, MedioPago

@login_required
def crear_venta(request):
    productos = Producto.objects.filter(stock__gt=0).order_by('nombre')
    medios_pago = MedioPago.objects.all()  # Carga los medios de pago desde BD

    if request.method == 'POST':
        medio_pago_id = request.POST.get('medio_pago')
        if not medio_pago_id:
            messages.error(request, "Por favor selecciona un medio de pago.")
            return render(request, 'tu_template.html', {'productos': productos, 'medios_pago': medios_pago})

        # Aquí puedes obtener el objeto MedioPago si lo necesitas
        medio_pago = None
        try:
            medio_pago = MedioPago.objects.get(id=medio_pago_id)
        except MedioPago.DoesNotExist:
            messages.error(request, "Medio de pago inválido.")
            return render(request, 'tu_template.html', {'productos': productos, 'medios_pago': medios_pago})

        
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
                        return render(request, 'tu_template.html', {'productos': productos, 'medios_pago': medios_pago})
                    subtotal = producto.precio * cantidad
                    total += subtotal
                    productos_venta.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
                except (Producto.DoesNotExist, ValueError):
                    messages.error(request, "Datos de producto inválidos.")
                    return render(request, 'tu_template.html', {'productos': productos, 'medios_pago': medios_pago})

        if not productos_venta:
            messages.error(request, "No has agregado productos a la venta.")
            return render(request, 'tu_template.html', {'productos': productos, 'medios_pago': medios_pago})

        
        empleado = Empleado.objects.get(user=request.user)

        venta = Venta.objects.create(
            empleado=empleado,
            total=total,
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
        return redirect('ventas')  # Cambia a la url que quieras

    # GET
    return render(request, 'ventas.html', {'productos': productos, 'medios_pago': medios_pago})
