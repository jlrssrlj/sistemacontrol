from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.principal, name='home'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ventas/', views.crear_venta, name='ventas'),
    path('historial_ventas', views.historial_ventas.as_view(), name='historial_ventas'),
    
]
