from dashboard.models import Venta

def listar_ventas():
    """
    Retorna un queryset con las ventas ordenadas por fecha descendente,
    con select_related para optimizar consultas.
    """
    return Venta.objects.select_related('empleado', 'cliente').order_by('-fecha')
