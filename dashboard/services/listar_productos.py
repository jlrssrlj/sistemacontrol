from dashboard.models import Producto


class ProductoService:
    @staticmethod
    def crear_producto(data):
        return Producto.objects.create(**data)
    
    @staticmethod
    def actualizar_producto(producto,data):
        for attr, value in data.items():
            setattr(producto, attr, value)
        producto.save()
        return producto
    
    @staticmethod
    def eliminar_producto(producto):
        producto.delete()

    @staticmethod
    def listar_producto():
        return Producto.objects.all()