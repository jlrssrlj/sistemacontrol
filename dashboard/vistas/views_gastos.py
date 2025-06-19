from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Proveedor, Empleado, Arqueo
from django.contrib import auth, messages
from ..services.listar_gastos import GastosService
from django.contrib.auth.decorators import login_required

class Gastos_views:

    @login_required
    def listar_gatos(request):
        gastos = GastosService.listar_gastos()
        return render(request, 'gastos/listar_gastos.html', {'gastos': gastos})


    @login_required
    def crear_gasto(request):
        if request.method == 'POST':
            empleado = Empleado.objects.get(user=request.user)

            arqueo_abierto = Arqueo.objects.filter(empleado=empleado, fecha_fin__isnull=True).first()
            if not arqueo_abierto:
                
                return redirect('listar_arqueos')

            data = {
                'empleado': empleado,
                'proveedor': Proveedor.objects.get(id=request.POST['proveedor']),
                'concepto': request.POST['concepto'],
                'monto': request.POST['monto'],
                'arqueo': arqueo_abierto
            }

            GastosService.crear_gastos(data)
            
            return redirect('listar_gastos')

        proveedores = Proveedor.objects.all()
        return render(request, 'gastos/crear_gastos.html', {
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

        return render(request, 'gastos/editar_gasto.html', {
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