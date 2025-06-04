from dashboard.models import Rol
from django.shortcuts import get_object_or_404

class Rolservice:

    @staticmethod
    def crear_rol(data):
        pago = Rol.objects.create(
            nombre = data['nombre']
        )
        return pago
    
    @staticmethod
    def listar_rol():
        pago = Rol.objects.all()
        return pago
    
    @staticmethod
    def eliminar_rol(id):
        pago = get_object_or_404(Rol, id=id)
        pago.delete()

    @staticmethod
    def editar_rol(id,data):
        pago = get_object_or_404(Rol, id=id)
        pago.nombre = data['nombre']
        pago.save()
        return pago