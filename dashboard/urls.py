from django.urls import path
from . import views  


urlpatterns = [
    path('', views.principal, name='panel'), 
    path('login/', views.login_view, name='login'),
    path('ventas/', views.ventas, name='ventas'), 
    path('logout/', views.login_view, name='logout'),
]
