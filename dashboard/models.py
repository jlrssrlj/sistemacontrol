from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# 1. Categoría de Producto
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
# 2. Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre    

# 3. Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

# 4. Rol de Empleado
class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# 5. Empleado (Usuario extendido)
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

# 6. Arqueo de Caja
class Arqueo(models.Model):  #Se crea una clase llamado arqueo que representa una tabla de la base de datos, cada vez que se cree un arqueo nuevo se guardara la informacion en dicha tabla.
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)  #almacena el nombre del empleado que realizo el arqueo medianmte una relacion que se conecta con el modelo empleado.
    fecha_inicio = models.DateTimeField()   #guarda la informacion de cuando se realizo el arqueo, fecha y hora.
    fecha_fin = models.DateTimeField(null=True, blank=True)     # guarda la informacion de cuando termina el arqueo, si no ha terminado deja la palabra null
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)    # almacena la cantidad o monto inicial con la que se iniciara el arqueo.
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)   #guarda la cantidad o monto final al cerrar el arqueo, si no se ha cerrado deja la palabra null
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    # almacena la diferencia entre el monto inicial y el monto final, esta operacion se realiza en arqueo_service.py

    def __str__(self):
        return f"Arqueo {self.id} - {self.fecha_inicio.date()}" #Muestra la informacion del arqueo.

# 7. Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    

class MedioPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# 8. Venta
class Venta(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)  
    arqueo = models.ForeignKey(Arqueo, on_delete=models.SET_NULL, null=True)  
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    medio_pago = models.ForeignKey(MedioPago, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha}"

# 9. Detalle de Venta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return Decimal(self.cantidad) * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"



# 10. Gasto
class Gasto(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    concepto = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    arqueo = models.ForeignKey(Arqueo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.concepto} - {self.monto}"
    

