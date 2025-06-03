from dashboard.models import Categoria
from django.shortcuts import get_object_or_404

class CategoriaService:

    @staticmethod
    def crear_categoria(data):
        categoria = Categoria.objects.create(nombre=data['nombre'])
        return categoria

    @staticmethod
    def editar_categoria(categoria_id, data):
        categoria = get_object_or_404(Categoria, id=categoria_id)
        categoria.nombre = data['nombre']
        categoria.save()
        return categoria

    @staticmethod
    def eliminar_categoria(categoria_id):
        categoria = get_object_or_404(Categoria, id=categoria_id)
        categoria.delete()

    @staticmethod
    def obtener_categoria(categoria_id):
        return get_object_or_404(Categoria, id=categoria_id)

    @staticmethod
    def listar_categoria():
        return Categoria.objects.all().order_by('nombre')
