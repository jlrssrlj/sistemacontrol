from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from ..services.categoria_service import CategoriaService 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class Categorias_views:
    @login_required
    def listar_categoria(request):
        categorias = CategoriaService.listar_categoria()
        print("Categorias en vista:", categorias)
        return render(request, 'categoria/listar_categoria.html', {'categorias': categorias})

    @login_required
    def crear_categoria(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                CategoriaService.crear_categoria({'nombre':nombre})
                return redirect('listar_categoria')
        return render(request,'categoria/crear_categoria.html')

    @login_required
    def editar_categoria(request, categoria_id):
        categoria = CategoriaService.obtener_categoria(categoria_id)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            if nombre:
                
                CategoriaService.editar_categoria(categoria_id, {'nombre': nombre})
                return redirect('listar_categoria')

        return render(request, 'categoria/editar_categoria.html', {'categoria': categoria})



    @login_required
    @require_POST
    def eliminar_categoria(request, categoria_id):
        try:
            CategoriaService.eliminar_categoria(categoria_id)
            
        except Exception:
            messages.error(request, 'Error al eliminar la categoría.')
        return redirect('listar_categoria')