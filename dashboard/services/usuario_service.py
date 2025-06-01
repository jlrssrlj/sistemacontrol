from django.contrib.auth.models import User
from dashboard.models import Empleado, Rol
from django.shortcuts import get_object_or_404

class UsuarioService:

    @staticmethod
    def crear_usuario_empleado(data):
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        Empleado.objects.create(
            user=user,
            rol=data['rol'],
            activo=True
        )
        return user

    @staticmethod
    def actualizar_usuario_empleado(empleado, data, es_superuser=False):
        usuario = empleado.user
        usuario.first_name = data.get('first_name', usuario.first_name)
        usuario.last_name = data.get('last_name', usuario.last_name)

        if es_superuser:
            usuario.is_staff = data.get('is_staff', usuario.is_staff)

        usuario.save()

        empleado.activo = data.get('activo', empleado.activo)
        rol = data.get('rol')
        if rol:
            empleado.rol = rol
        empleado.save()
        return empleado

    @staticmethod
    def eliminar_empleado(id):
        empleado = get_object_or_404(Empleado, id=id)
        empleado.delete()
        return True

    
    @staticmethod
    def obtener_empleados():
        return Empleado.objects.select_related('user', 'rol').all()
    #trae la informacion de la tabla de rol
    @staticmethod
    def obtener_roles():
        return Rol.objects.all()
