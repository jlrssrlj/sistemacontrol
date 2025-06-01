from dashboard.models import Producto, Categoria
from django.shortcuts import get_object_or_404

class ProductoService:
    
    @staticmethod
    def crear_producto(data):
        categoria = None
        categoria_id = data.get('categoria_id')
        
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                categoria = None
                
        producto = Producto.objects.create(
            nombre = data['nombre'],
            descripcion = data['descripcion'],
            precio = data['precio'],
            stock = data['stock'],
            categoria = categoria
            #categoria = data ['categoria'],
            #categoria = data.get('categoria')
        )
        return producto
    
    @staticmethod
    def actualizar_producto(producto_id,data):
        producto = get_object_or_404(Producto, id=producto_id)
        
        producto.nombre = data['nombre']
        producto.descripcion = data['descripcion']
        producto.precio = data['precio']
        producto.stock = data['stock']
        categoria = data['categoria_id']
        producto.categoria = get_object_or_404(Categoria, id=categoria)
        producto.save()
        return producto
    
    @staticmethod
    def eliminar_producto(id):
        producto=get_object_or_404(Producto, id= id)            # si no encuentra el id del arqueo que queremos eliminar muestra un error 404
        producto.delete()

    @staticmethod
    def listar_producto():
        
        return Producto.objects.all()