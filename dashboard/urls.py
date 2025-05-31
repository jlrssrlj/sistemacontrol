from django.urls import path
from . import views  


urlpatterns = [
    path('', views.principal, name='home'), 
    path('login/', views.login_view, name='login'),
    path('ventas/', views.crear_venta, name='ventas'), 
    path('logout/', views.logout_view, name='logout'),
]
