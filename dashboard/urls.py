from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views 
from dashboard.vistas import (views_productos as producto) 

urlpatterns = [
    path('', views.principal, name='home'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ventas/', views.crear_venta, name='ventas'),
    path('historial_ventas', views.historial_ventas.as_view(), name='historial_ventas'),
    path('crear_usuario', views.crear_usuario, name='crear_usuario'),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),
    path('listar_empleado/', views.listar_empleado, name='listar_empleado'),
    path('empleado/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleado/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('arqueos/', views.Arqueo_views.listar_arqueo, name='listar_arqueos'),
    path('arqueos/abrir/',views.Arqueo_views.crear_arqueo,name='crear_arqueo'),
    path('arqueos/cerrar/<int:id>/',views.Arqueo_views.cerrar_arqueo,name='cerrar_arqueo'),
    path('arqueos/eliminar/<int:id>/',views.Arqueo_views.eliminar_arqueo,name='eliminar_arqueo'),
    path('listar_producto/', producto.Producto_views.listar_producto, name='listar_producto'),
    path('listar_producto/crear/',producto.Producto_views.crear_producto,name='crear_producto'),
    path('listar_producto/editar/<int:id>/', producto.Producto_views.editar_producto, name='editar_producto'),
    path('listar_producto/eliminar/<int:id>/',producto.Producto_views.eliminar_producto,name='eliminar_producto'),
    path('categorias/', views.Categorias_views.listar_categoria, name='listar_categoria'),
    path('categoria/crear/', views.Categorias_views.crear_categoria,name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.Categorias_views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.Categorias_views.eliminar_categoria, name='eliminar_categoria'),
    path('listar_gastos/',views.Gastos_views.listar_gatos, name='listar_gastos'),
    path('listar_gastos/crear_gastos/',views.Gastos_views.crear_gasto,name='crear_gasto'),
    path('gastos/editar/<int:id>/', views.Gastos_views.editar_gasto, name='editar_gasto'),
    path('gastos/eliminar/<int:id>/', views.Gastos_views.eliminar_gasto, name='eliminar_gasto'),
    path('proveedores/', views.Proveedores_views.listar_proveedores, name='listar_proveedores'),
    path('proveedores/nuevo/', views.Proveedores_views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', views.Proveedores_views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', views.Proveedores_views.eliminar_proveedor, name='eliminar_proveedor'),
    path('configuracion/medio_de_pago/', views.Mediopago_views.listar_mediopago, name='listar_medio_pago'),
    path('medio_de_pago/crear/', views.Mediopago_views.crear_mediopago, name='crear_mediopago'),
    path('medio_de_pago/editar/<int:id>/', views.Mediopago_views.editar_mediopago,name='editar_pago'),
    path('medio_de_pago/eliminar/<int:id>', views.Mediopago_views.eliminar_mediopago, name='eliminar_mediopago'),
    path('configuracion/rol/', views.Rol_views.listar_rol, name='listar_rol'),
    path('rol/crear/', views.Rol_views.crear_rol, name='crear_rol'),
    path('rol/editar/<int:id>/', views.Rol_views.editar_rol,name='editar_rol'),
    path('rol/eliminar/<int:id>', views.Rol_views.eliminar_rol, name='eliminar_rol')

]
