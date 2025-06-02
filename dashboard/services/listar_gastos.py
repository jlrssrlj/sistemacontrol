from dashboard.models import Gastos, Empleado, Proveedor, Arqueo
from django.shortcuts import get_object_or_404

class GastosService:

    @staticmethod
    def crear_gastos(data):
        empleado = get_object_or_404(Empleado, id=data['empleado_id'])
        proveedor = get_object_or_404(Proveedor, id=data['proveedor_id'])
        arqueo_id = data.get('arqueo_id')
        arqueo = Arqueo.objects.get(id=arqueo_id) if arqueo_id else None

        gastos = Gastos.objects.create(
            empleado=empleado,
            proveedor=proveedor,
            concepto=data['concepto'],
            monto=data['monto'],
            arqueo=arqueo
        )
        return gastos

    @staticmethod
    def actualizar_gasto(gasto_id, data):
        gastos = get_object_or_404(Gastos, id=gastos_id)
        gastos.empleado = get_object_or_404(Empleado, id=data['empleado_id'])
        gastos.proveedor = get_object_or_404(Proveedor, id=data['proveedor_id'])
        gastos.concepto = data['concepto']
        gastos.monto = data['monto']

        arqueo_id = data.get('arqueo_id')
        gastos.arqueo = Arqueo.objects.get(id=arqueo_id) if arqueo_id else None

        gasto.save()
        return gasto

    @staticmethod
    def eliminar_gastos(id):
        gastos = get_object_or_404(Gastos, id=id)
        gastos.delete()

    @staticmethod
    def listar_gastos():
        return Gastos.objects.all()
