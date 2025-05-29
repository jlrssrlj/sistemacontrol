from django.urls import path
from . import views  


urlpatterns = [
    path('tedsito', views.principal, name='panel'),  
]
