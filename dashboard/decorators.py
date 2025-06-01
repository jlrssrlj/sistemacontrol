from functools import wraps
from django.shortcuts import redirect


def rol_requerido(*roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            # Permitir acceso al superusuario
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                rol = request.user.empleado.rol.nombre.lower()
            except AttributeError:
                return redirect('no_autorizado')

            if rol in [r.lower() for r in roles_permitidos]:
                return view_func(request, *args, **kwargs)
            
            return redirect('no_autorizado')
        return _wrapped_view
    return decorador
