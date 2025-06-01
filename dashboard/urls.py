from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views  

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
    path('arqueos/', views.listar_arqueo, name='listar_arqueos'),
    path('arqueos/abrir/',views.crear_arqueo,name='crear_arqueo'),
    path('arqueos/cerrar/<int:id>/',views.cerrar_arqueo,name='cerrar_arqueo'),
    path('arqueos/eliminar/<int:id>/',views.eliminar_arqueo,name='eliminar_arqueo'),
    path('listar_producto/', views.listar_producto, name='listar_producto'),
    path('listar_producto/crear/',views.crear_producto,name='crear_producto'),
    path('listar_producto/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('listar_producto/eliminar/<int:id>/',views.eliminar_producto,name='eliminar_producto')


]
