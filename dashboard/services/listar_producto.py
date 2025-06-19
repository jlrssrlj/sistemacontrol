from dashboard.models import Producto, Categoria, Proveedor
from django.shortcuts import get_object_or_404

class ProductoService:
    
    @staticmethod
    def crear_producto(data):
        categoria = None
        proveedor = None

        # Obtener categoría
        categoria_id = data.get('categoria_id')
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=int(categoria_id))
            except (Categoria.DoesNotExist, ValueError, TypeError):
                categoria = None

        # Obtener proveedor
        proveedor_id = data.get('proveedor_id')
        if proveedor_id:
            try:
                proveedor = Proveedor.objects.get(id=int(proveedor_id))
            except (Proveedor.DoesNotExist, ValueError, TypeError):
                proveedor = None

        # Crear producto
        producto = Producto.objects.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio=data['precio'],
            stock=data['stock'],
            categoria=categoria,
            proveedor=proveedor
        )
        return producto


    
    @staticmethod
    def actualizar_producto(producto_id, data):
        producto = get_object_or_404(Producto, id=producto_id)

        # Actualizar campos simples
        producto.nombre = data['nombre']
        producto.descripcion = data['descripcion']
        producto.precio = data['precio']
        producto.stock = data['stock']

        # Obtener categoría
        categoria_id = data.get('categoria_id')
        if categoria_id:
            try:
                producto.categoria = Categoria.objects.get(id=int(categoria_id))
            except (Categoria.DoesNotExist, ValueError, TypeError):
                producto.categoria = None
        else:
            producto.categoria = None

        # Obtener proveedor
        proveedor_id = data.get('proveedor_id')
        if proveedor_id:
            try:
                producto.proveedor = Proveedor.objects.get(id=int(proveedor_id))
            except (Proveedor.DoesNotExist, ValueError, TypeError):
                producto.proveedor = None
        else:
            producto.proveedor = None

        producto.save()
        return producto

    
    @staticmethod
    def eliminar_producto(id):
        producto=get_object_or_404(Producto, id= id)            # si no encuentra el id del arqueo que queremos eliminar muestra un error 404
        producto.delete()

    @staticmethod
    def listar_producto():
        
        return Producto.objects.all()