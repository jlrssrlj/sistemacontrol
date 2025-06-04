from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Proveedor, Empleado, Arqueo
from django.contrib import auth, messages
from ..services.categoria_service import CategoriaService 
from django.contrib.auth.decorators import login_required

class Categorias_views:
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