from dashboard.models import Gasto, Empleado, Proveedor, Arqueo
from django.shortcuts import get_object_or_404
from django.utils import timezone 

class GastosService:

    @staticmethod
    def listar_gastos():
        return Gasto.objects.all()
    
    @staticmethod
    def obtener_gasto(id):
        return get_object_or_404(Gasto, id=id)

    @staticmethod
    def crear_gastos(data):
        gasto = Gasto.objects.create(
            empleado=data['empleado'],
            proveedor=data['proveedor'],
            concepto=data['concepto'],
            monto=data['monto'],
            fecha=timezone.now(),
            arqueo=data['arqueo']
        )
        return gasto
    
    @staticmethod
    def editar_gasto(id, data):
        gasto = get_object_or_404(Gasto, id=id)
        gasto.empleado = data['empleado']
        gasto.proveedor = data['proveedor']
        gasto.concepto = data['concepto']
        gasto.monto = data['monto']
        gasto.arqueo = data['arqueo']
        gasto.save()
        return gasto
    
    @staticmethod
    def eliminar_gasto(id):
        gasto = get_object_or_404(Gasto, id=id)
        gasto.delete()
        return True