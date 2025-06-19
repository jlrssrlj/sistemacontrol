from django.db.models import Sum
from decimal import Decimal
from dashboard.models import Arqueo, Venta, Gasto
from django.utils import timezone
from django.shortcuts import get_object_or_404            

class ArqueoService:

    @staticmethod
    def crear_arqueo(data):
        arqueo = Arqueo.objects.create(
            empleado=data['empleado'],
            fecha_inicio=timezone.now(),
            monto_inicial=data['monto_inicial']
        )
        return arqueo

    @staticmethod
    def cerrar_arqueo(arqueo_id, monto_final):
        arqueo = get_object_or_404(Arqueo, id=arqueo_id)
        arqueo.fecha_fin = timezone.now()
        arqueo.monto_final = Decimal(monto_final)

        # ✅ Solo ventas del arqueo actual y del mismo empleado
        total_ventas = Venta.objects.filter(
            arqueo=arqueo,
            empleado=arqueo.empleado
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')

        # ✅ Solo gastos asociados al arqueo
        total_gastos = Gasto.objects.filter(
            arqueo=arqueo
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

        calculado = arqueo.monto_inicial + total_ventas - total_gastos
        arqueo.diferencia = calculado - arqueo.monto_final

        arqueo.save()
        return arqueo

    @staticmethod
    def listar_arqueos():
        arqueos = Arqueo.objects.select_related('empleado__user').order_by('-fecha_inicio')
        for arqueo in arqueos:
            arqueo.total_ventas = Venta.objects.filter(
                arqueo=arqueo,
                empleado=arqueo.empleado
            ).aggregate(total=Sum('total'))['total'] or 0

            arqueo.total_gastos = Gasto.objects.filter(
                arqueo=arqueo
            ).aggregate(total=Sum('monto'))['total'] or 0
        return arqueos

    @staticmethod
    def obtener_arqueo(id):
        return get_object_or_404(Arqueo, id=id)

    @staticmethod
    def eliminar_arqueo(id):
        arqueo = get_object_or_404(Arqueo, id=id)
        arqueo.delete()
