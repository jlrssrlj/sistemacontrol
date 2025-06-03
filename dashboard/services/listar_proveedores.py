from dashboard.models import Proveedor
from django.shortcuts import get_object_or_404

class ProveedorService:

    @staticmethod
    def crear_proveedor(data):
        proveedor = Proveedor.objects.create(
            nombre=data['nombre'],
            nit=data['nit'],
            direccion=data['direccion'],
            telefono=data['telefono']
        )
        return proveedor

    @staticmethod
    def actualizar_proveedor(proveedor, data):
        proveedor.nombre = data.get('nombre', proveedor.nombre)
        proveedor.nit = data.get('nit', proveedor.nit)
        proveedor.direccion = data.get('direccion', proveedor.direccion)
        proveedor.telefono = data.get('telefono', proveedor.telefono)
        proveedor.save()
        return proveedor

    @staticmethod
    def eliminar_proveedor(id):
        proveedor = get_object_or_404(Proveedor, id=id)
        proveedor.delete()
        return True

    @staticmethod
    def obtener_proveedores():
        return Proveedor.objects.all()

    @staticmethod
    def obtener_proveedor(id):
        return get_object_or_404(Proveedor, id=id)
