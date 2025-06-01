#crea las consultas que se realizaran sobre la base de datos.

from dashboard.models import Arqueo                         # usamos el modelo arqueo que tenemos en dashboard models.py
from django.utils import timezone                           # mediante la funcion timezone nos dice la fecha y hora actual del sistema
from django.shortcuts import get_object_or_404              # buesca un registro en la base de datos, si no encuentra dicho registro muestra un error 404 no esta

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
    
    @staticmethod                                           # llamada los modelos
    def cerrar_arqueo(arqueo_id,monto_final):               # sirve para cerrar el arqueo con el id y el monto final
        arqueo = get_object_or_404(Arqueo, id= arqueo_id)   # busca el arqueo creado por el id, si no encuentra dicho id del arqueo iniciado muestra error 404 no encontrado
        arqueo.fecha_fin= timezone.now()                    # guarda la fecha actual de cuando se cerrara el arqueo
        arqueo.monto_final= monto_final                     # pide el monto final con el que se cerrara el arqueo
        arqueo.diferencia = float(monto_final)- float(arqueo.monto_inicial) # calcula la diferencia entre el monto inicial y el monto final del arqueo, float es el tipo de dato.
        arqueo.save()                                       # guarda los datos en la base de datos
        return arqueo                                       # devuelve la informacion actualizada.
    
    @staticmethod
    def listar_arqueos():
        return Arqueo.objects.select_related('empleado__user').order_by('-fecha_inicio')
    
    @staticmethod
    def obtener_arqueo(id):                                 # funcion para buscar el arqueo mediante el id
        return get_object_or_404(Arqueo, id=id)             # si no encuentra el id del arqueo que estamos buscando muestra un error 404
    
    @staticmethod
    def eliminar_arqueo(id):                                # funcion parta eliminar el arqueo mediante el id
        arqueo=get_object_or_404(Arqueo, id= id)            # si no encuentra el id del arqueo que queremos eliminar muestra un error 404
        arqueo.delete()                                     # guarda la informacion en la base de datos.
