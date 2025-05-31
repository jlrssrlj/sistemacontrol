# dashboard/decorators.py (o el nombre de tu app)

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def rol_requerido(*roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            try:
                rol = request.user.empleado.rol.nombre.lower()
            except AttributeError:
                messages.error(request, "No tienes un rol asignado.")
                return redirect('no_autorizado')

            if rol in [r.lower() for r in roles_permitidos]:
                return view_func(request, *args, **kwargs)

            messages.error(request, "No tienes permiso para acceder a esta vista.")
            return redirect('no_autorizado')
        return _wrapped_view
    return decorador
