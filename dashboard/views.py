from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

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

@login_required
@login_required
def crear_venta_view(request):
    empleado = get_object_or_404(Empleado, user=request.user)
    arqueo = Arqueo.objects.filter(empleado=empleado, fecha_fin__isnull=True).first()
    productos = Producto.objects.filter(stock__gt=0)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Crear la venta
                venta = Venta.objects.create(
                    empleado=empleado,
                    arqueo=arqueo,
                    total=0  # Se actualiza más adelante
                )

                total_venta = 0

                # Recorrer los productos enviados en el POST
                for key, value in request.POST.items():
                    if key.startswith('producto_id_'):
                        producto_id = key.replace('producto_id_', '')
                        cantidad_key = f'cantidad_{producto_id}'
                        cantidad = int(request.POST.get(cantidad_key, 0))

                        if cantidad < 1:
                            continue

                        producto = Producto.objects.get(id=producto_id)

                        if producto.stock < cantidad:
                            messages.error(request, f"No hay suficiente stock para {producto.nombre}")
                            raise Exception("Stock insuficiente")

                        subtotal = cantidad * producto.precio

                        DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=producto.precio
                        )

                        producto.stock -= cantidad
                        producto.save()

                        total_venta += subtotal

                venta.total = total_venta
                venta.save()

                messages.success(request, "Venta registrada exitosamente.")
                return redirect('ventas')  # Cambia por el nombre real de tu URL

        except Exception as e:
            messages.error(request, f"Error al procesar la venta: {str(e)}")

    return render(request, 'ventas.html', {
        'productos': productos
    })
