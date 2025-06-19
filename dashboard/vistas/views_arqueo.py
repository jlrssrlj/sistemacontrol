from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import Arqueo, Venta
from ..services.arqueo_service import ArqueoService

class Arqueo_views:

    @login_required
    def crear_arqueo(request):
        if request.method == 'POST':
            monto_inicial = request.POST.get('monto_inicial')

            try:
                monto_inicial = float(monto_inicial)
            except ValueError:
                return render(request, 'arqueo/crear_arqueo.html', {
                    'error': 'El monto inicial debe ser un número válido.'
                })

            empleado = request.user.empleado

            data = {
                'monto_inicial': monto_inicial,
                'empleado': empleado
            }

            ArqueoService.crear_arqueo(data)
            return redirect('listar_arqueos')

        return render(request, 'arqueo/crear_arqueo.html')

    @login_required
    def cerrar_arqueo(request, id):
        arqueo = ArqueoService.obtener_arqueo(id)

        # ✅ Obtener ventas del arqueo y del empleado correspondiente
        ventas = Venta.objects.filter(
            arqueo=arqueo,
            empleado=arqueo.empleado
        ).select_related('cliente', 'medio_pago')

        if request.method == 'POST':
            monto_final = request.POST.get('monto_final')

            try:
                monto_final = float(monto_final)
                ArqueoService.cerrar_arqueo(id, monto_final)
                return redirect('listar_arqueos')

            except ValueError:
                return render(request, 'arqueo/cerrar_arqueo.html', {
                    'arqueo': arqueo,
                    'ventas': ventas,
                    'error': 'El monto final debe ser un número válido.'
                })

        return render(request, 'arqueo/cerrar_arqueo.html', {
            'arqueo': arqueo,
            'ventas': ventas
        })

    @login_required
    def listar_arqueo(request):
        arqueos = ArqueoService.listar_arqueos()
        context = {
            'arqueos': arqueos,
        }
        return render(request, 'arqueo/listar_arqueos.html', context)

    @login_required
    def eliminar_arqueo(request, id):
        arqueo = get_object_or_404(Arqueo, id=id)

        if request.method == 'POST':
            ArqueoService.eliminar_arqueo(id)
            return redirect('listar_arqueos')

        return render(request, 'arqueo/confirmacion_eliminacion_arqueo.html', {
            'arqueo': arqueo
        })
