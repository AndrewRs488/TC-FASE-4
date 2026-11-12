"""Módulo de gestión de reservas con control de estados y encadenamiento de excepciones."""

from enum import Enum
import logging
from typing import Optional
from entidades import Cliente, EntidadSistema
from excepciones import (
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    SoftwareFJError,
)
from servicios import Servicio


class EstadoReserva(Enum):
    """Estados posibles dentro del ciclo de vida de una reserva."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"


class Reserva(EntidadSistema):
    """Integra Cliente, Servicio y duración gestionando transiciones seguras."""

    def __init__(
        self,
        reserva_id: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int,
        impuesto: float = 0.19,
        descuento: Optional[float] = None,
        cargo_adicional: float = 0.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(reserva_id)
        if not isinstance(cliente, Cliente) or not cliente.validar_integridad():
            raise ReservaInvalidaError("La reserva requiere un cliente válido y activo.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Servicio.")

        self._cliente: Cliente = cliente
        self._servicio: Servicio = servicio
        self._duracion_horas: int = duracion_horas
        self._impuesto: float = impuesto
        self._descuento: Optional[float] = descuento
        self._cargo_adicional: float = cargo_adicional
        self._estado: EstadoReserva = EstadoReserva.PENDIENTE
        self._costo_total: float = 0.0
        self._logger = logger or logging.getLogger("SoftwareFJ")

        # Calcula y valida costos iniciales encadenando excepciones si hay inconsistencias
        self._recalcular_costo()

    def _recalcular_costo(self) -> None:
        """Calcula el costo aplicando encadenamiento de excepciones ante fallos."""
        try:
            self._costo_total = self._servicio.calcular_costo_total(
                duracion_horas=self._duracion_horas,
                impuesto=self._impuesto,
                descuento=self._descuento,
                cargo_adicional=self._cargo_adicional,
            )
        except SoftwareFJError as err:
            raise ReservaInvalidaError(
                f"Fallo al validar costos para la reserva '{self.id}': {err}"
            ) from err

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def confirmar(self) -> None:
        """Confirma una reserva pendiente usando try/except/else/finally."""
        auditoria_completada = False
        try:
            if self._estado != EstadoReserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva '{self.id}' en estado {self._estado.value}."
                )
            self._recalcular_costo()
        except SoftwareFJError as err:
            self._logger.error("Error al confirmar reserva %s: %s", self.id, err)
            raise
        else:
            self._estado = EstadoReserva.CONFIRMADA
            auditoria_completada = True
            self._logger.info(
                "Reserva %s CONFIRMADA | Cliente: %s | Total: $%.2f",
                self.id,
                self._cliente.nombre,
                self._costo_total,
            )
        finally:
            self._logger.info(
                "Cierre de transacción de confirmación [%s] (éxito=%s).",
                self.id,
                auditoria_completada,
            )

    def procesar(self) -> None:
        """Ejecuta y finaliza una reserva previamente confirmada."""
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas CONFIRMADAS (actual: {self._estado.value})."
                )
        except OperacionNoPermitidaError as err:
            self._logger.error("Error al procesar reserva %s: %s", self.id, err)
            raise
        else:
            self._estado = EstadoReserva.PROCESADA
            self._logger.info(
                "Reserva %s PROCESADA exitosamente para el servicio '%s'.",
                self.id,
                self._servicio.nombre,
            )
        finally:
            self._logger.info("Auditoría de procesamiento finalizada para reserva %s.", self.id)

    def cancelar(self, motivo: str = "Solicitud del cliente") -> None:
        """Cancela una reserva siempre que no haya sido procesada."""
        try:
            if self._estado == EstadoReserva.PROCESADA:
                raise OperacionNoPermitidaError(
                    f"La reserva '{self.id}' ya fue PROCESADA y no puede cancelarse."
                )
            if self._estado == EstadoReserva.CANCELADA:
                raise OperacionNoPermitidaError(
                    f"La reserva '{self.id}' ya se encuentra CANCELADA."
                )
        except OperacionNoPermitidaError as err:
            self._logger.error("Error al cancelar reserva %s: %s", self.id, err)
            raise
        else:
            self._estado = EstadoReserva.CANCELADA
            self._logger.warning(
                "Reserva %s CANCELADA. Motivo: %s", self.id, motivo
            )
        finally:
            self._logger.info("Registro de cancelación verificado para reserva %s.", self.id)

    def validar_integridad(self) -> bool:
        return self._costo_total > 0 and self._estado != EstadoReserva.CANCELADA

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self._estado.value} | "
            f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion_horas}h | Total: ${self._costo_total:,.2f}"
        )