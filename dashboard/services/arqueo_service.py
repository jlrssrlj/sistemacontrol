from django.db.models import Sum
from decimal import Decimal
from dashboard.models import Arqueo, Venta, Gasto
from django.utils import timezone
from django.shortcuts import get_object_or_404            

class ArqueoService:                                        # mediante la creaccion de la clase "class" guardamos las funciones relacionadas al arqueo en "arqueoservice"

    @staticmethod                                           # llamada los modelos
    def crear_arqueo(data):                                 # Creamos una funcion "def" llamada crear_arqueo que recibe el parametro data donde almacenara los datos para crear el nuevo arqueo
        arqueo  = Arqueo.objects.create(                    # arqueo (guardeme el resultado de lo que vamos a crear en arqueo) = Arqueo (nombre de la tabla donde guardaremos la informacion).
                                                            #objects (herramient de django que permite realizar la funcion junto a create)// create debido a que vamos a crear un nuevo arqueo que se almacenara en la base de datos
        empleado = data ['empleado'],                   # 
        fecha_inicio = timezone.now(),                  # guardamos la fecha actual de cuando crearemos el arqueo
        monto_inicial = data ['monto_inicial']          # agrega el monto inicial
        )      
        return arqueo                                   # devuelve y almacena los datos anteriormente creados.
    
    @staticmethod
    def cerrar_arqueo(arqueo_id, monto_final):
        arqueo = get_object_or_404(Arqueo, id=arqueo_id)
        arqueo.fecha_fin = timezone.now()
        arqueo.monto_final = Decimal(monto_final)

        total_ventas = Venta.objects.filter(arqueo=arqueo).aggregate(total=Sum('total'))['total'] or Decimal('0')
        total_gastos = Gasto.objects.filter(arqueo=arqueo).aggregate(total=Sum('monto'))['total'] or Decimal('0')

        calculado = arqueo.monto_inicial + total_ventas - total_gastos
        arqueo.diferencia = calculado - arqueo.monto_final

        arqueo.save()
        return arqueo

    
    @staticmethod
    def listar_arqueos():
        arqueos = Arqueo.objects.select_related('empleado__user').order_by('-fecha_inicio')
        for arqueo in arqueos:
            arqueo.total_ventas = Venta.objects.filter(arqueo=arqueo).aggregate(total=Sum('total'))['total'] or 0
            arqueo.total_gastos = Gasto.objects.filter(arqueo=arqueo).aggregate(total=Sum('monto'))['total'] or 0
        return arqueos
    
    @staticmethod
    def obtener_arqueo(id):                                 # funcion para buscar el arqueo mediante el id
        return get_object_or_404(Arqueo, id=id)             # si no encuentra el id del arqueo que estamos buscando muestra un error 404
    
    @staticmethod
    def eliminar_arqueo(id):                                # funcion parta eliminar el arqueo mediante el id
        arqueo=get_object_or_404(Arqueo, id= id)            # si no encuentra el id del arqueo que queremos eliminar muestra un error 404
        arqueo.delete()                                     # guarda la informacion en la base de datos.
