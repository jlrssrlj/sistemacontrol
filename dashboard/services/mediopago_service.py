from dashboard.models import MedioPago
from django.shortcuts import get_object_or_404

class MediopagoService:

    @staticmethod
    def crear_mediopago(data):
        pago = MedioPago.objects.create(
            nombre = data['nombre']
        )
        return pago
    
    @staticmethod
    def listar_mediopago():
        pago = MedioPago.objects.all()
        return pago
    
    @staticmethod
    def eliminar_mediopago(id):
        pago = get_object_or_404(MedioPago, id=id)
        pago.delete()

    @staticmethod
    def editar_mediopago(id,data):
        pago = get_object_or_404(MedioPago, id=id)
        pago.nombre = data['nombre']
        pago.save()
        return pago