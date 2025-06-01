from dashboard.models import Arqueo
from django.utils import timezone
from django.shortcuts import get_object_or_404

class ArqueoService:

    @staticmethod
    def crear_arqueo(data):
        arqueo = Arqueo.objects.create(
            empleado = data['empleado'],
            fecha_inicio =timezone.now(),
            monto_inicial= data['monto_inicial']
        )
        return arqueo
    
    @staticmethod
    def cerrar_arqueo(arqueo_id,monto_final):
        arqueo = get_object_or_404(Arqueo, id= arqueo_id)
        arqueo.fecha_fin= timezone.now()
        arqueo.monto_final= monto_final
        arqueo.diferencia = float(monto_final)- float(arqueo.monto_inicial)
        arqueo.save()
        return arqueo
    
    @staticmethod
    def listar_arqueos():
        return Arqueo.objects.select_related('empleado__user').order_by('-fecha_inicio')
    
    @staticmethod
    def obtener_arqueo(id):
        return get_object_or_404(Arqueo, id=id)
    
    @staticmethod
    def eliminar_arqueo(id):
        arqueo=get_object_or_404(Arqueo, id= id)
        arqueo.delete()
