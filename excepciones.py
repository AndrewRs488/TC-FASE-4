"""Jerarquía de excepciones personalizadas para el sistema de Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base para todos los errores controlados del sistema."""


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando un dato no cumple el formato o rango esperado."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio o está vacío."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza al intentar ejecutar una acción inválida según el estado actual."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva incumple reglas de negocio o validación."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando los parámetros financieros generan valores incoherentes."""
    