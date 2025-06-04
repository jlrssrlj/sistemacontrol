from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Rol
from ..services.rol_service import Rolservice

class Rol_views:
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
   