from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Proveedor
from ..forms import UsuarioEmpleadoForm
from ..forms import ProveedorForm
from ..services.listar_proveedores import ProveedorService


class Proveedores_views:
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