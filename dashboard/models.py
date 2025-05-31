from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# 1. Categoría de Producto
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# 2. Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

# 3. Rol de Empleado
class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# 4. Empleado (Usuario extendido)
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

# 5. Arqueo de Caja
class Arqueo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)  
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Arqueo {self.id} - {self.fecha_inicio.date()}"

# 6. Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# 7. Venta
class Venta(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)  
    arqueo = models.ForeignKey(Arqueo, on_delete=models.SET_NULL, null=True)  
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha}"

# 8. Detalle de Venta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return Decimal(self.cantidad) * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# 9. Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

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
    
class MedioPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

