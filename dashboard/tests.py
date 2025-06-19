from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

from dashboard.models import Empleado, Rol, Arqueo, Venta, Gasto, Cliente, Producto, Proveedor, Categoria, MedioPago
from dashboard.services.arqueo_service import ArqueoService

class CerrarArqueoServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cajero', password='1234')
        self.rol = Rol.objects.create(nombre='Cajero')
        self.empleado = Empleado.objects.create(user=self.user, rol=self.rol)

        self.proveedor = Proveedor.objects.create(nombre="ProveedorX", nit="999", direccion="Calle 123", telefono="321")
        self.categoria = Categoria.objects.create(nombre="Granos")
        self.producto = Producto.objects.create(nombre="Frijoles", descripcion="Negros", precio=10000, stock=50, categoria=self.categoria, proveedor=self.proveedor)
        self.mediopago = MedioPago.objects.create(nombre="Efectivo")
        self.cliente = Cliente.objects.create(nombre="ClienteX", identificacion="222", telefono="000", direccion="Calle")

        self.arqueo = Arqueo.objects.create(
            empleado=self.empleado,
            fecha_inicio=timezone.now(),
            monto_inicial=Decimal("100000.00")
        )

        Venta.objects.create(
            empleado=self.empleado,
            arqueo=self.arqueo,
            cliente=self.cliente,
            total=Decimal("30000.00"),
            medio_pago=self.mediopago
        )

        Gasto.objects.create(
            empleado=self.empleado,
            proveedor=self.proveedor,
            concepto="Gasto prueba",
            monto=Decimal("7000.00"),
            arqueo=self.arqueo
        )

    def test_cerrar_arqueo_calculos_correctos(self):
        #
        monto_final_usuario = Decimal("122000.00")

        arqueo_cerrado = ArqueoService.cerrar_arqueo(self.arqueo.id, monto_final_usuario)

        # Valores esperados
        total_ventas = Decimal("30000.00")
        total_gastos = Decimal("7000.00")
        calculado_por_sistema = self.arqueo.monto_inicial + total_ventas - total_gastos 
        diferencia_esperada = calculado_por_sistema - monto_final_usuario  

        # Imprimir 
        print("\n--- RESULTADOS TEST ARQUEO ---")
        print(f"Total Ventas:     {total_ventas}")
        print(f"Total Gastos:     {total_gastos}")
        print(f"Monto Inicial:    {self.arqueo.monto_inicial}")
        print(f"Monto Final (Caja): {monto_final_usuario}")
        print(f"Monto Sistema:    {calculado_por_sistema}")
        print(f"Diferencia:       {arqueo_cerrado.diferencia}")
        print(f'Diferencia esperada:{diferencia_esperada}')
        print("------------------------------")

        self.assertIsNotNone(arqueo_cerrado.fecha_fin)
        self.assertEqual(arqueo_cerrado.monto_final, monto_final_usuario)
        self.assertEqual(arqueo_cerrado.diferencia, Decimal("1000.00"))
