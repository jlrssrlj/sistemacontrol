from django.shortcuts import render, redirect, get_object_or_404
from ..services.listar_producto import ProductoService
from django.contrib.auth.decorators import login_required
from dashboard.models import Categoria, Producto, Proveedor


class Producto_views:

    @login_required
    def crear_producto(request):
        if request.method == 'POST':
            categoria_id = request.POST.get('categoria_id')
            proveedor_id = request.POST.get('proveedor_id')  # Corregido el typo

            data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'precio': request.POST.get('precio'),
                'stock': request.POST.get('stock'),
                'categoria_id': categoria_id,
                'proveedor_id': proveedor_id
            }

            ProductoService.crear_producto(data)
            return redirect('listar_producto')

        categorias = Categoria.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, 'productos/crear_producto.html', {
            'categorias': categorias,
            'proveedores': proveedores
        })

    @login_required
    def listar_producto(request):
        productos = ProductoService.listar_producto()
        return render(request, 'productos/listar_producto.html', {'producto': productos})

    @login_required
    def editar_producto(request, id):
        producto = get_object_or_404(Producto, id=id)

        if request.method == 'POST':
            data = {
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'precio': request.POST.get('precio'),
                'stock': request.POST.get('stock'),
                'categoria_id': request.POST.get('categoria_id'),
                'proveedor_id': request.POST.get('proveedor_id')
            }
            ProductoService.actualizar_producto(producto.id, data)
            return redirect('listar_producto')

        categorias = Categoria.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, 'productos/editar_producto.html', {
            'producto': producto,
            'categorias': categorias,
            'proveedores': proveedores
        })

    @login_required
    def eliminar_producto(request, id):
        producto = get_object_or_404(Producto, id=id)

        if request.method == 'POST':
            ProductoService.eliminar_producto(id)
            return redirect('listar_producto')

        return render(request, 'productos/confirmar_eliminacion_producto.html', {'producto': producto})
