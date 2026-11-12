"""Módulo de servicios abstractos y especializados con polimorfismo y sobrecarga."""

from abc import ABC, abstractmethod
from typing import Optional
from entidades import EntidadSistema
from excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadSistema, ABC):
    """Clase abstracta que define el contrato base para los servicios de Software FJ."""

    def __init__(
        self,
        servicio_id: str,
        nombre: str,
        tarifa_hora: float,
        disponible: bool = True,
    ) -> None:
        super().__init__(servicio_id)
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_hora is None or tarifa_hora <= 0:
            raise DatosInvalidosError(
                f"La tarifa por hora debe ser mayor a cero (recibido: {tarifa_hora})."
            )
        self._nombre: str = str(nombre).strip()
        self._tarifa_hora: float = float(tarifa_hora)
        self._disponible: bool = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Valida los parámetros específicos de cada tipo de servicio."""

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción detallada y polimórfica del servicio."""

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Calcula el subtotal base antes de impuestos y descuentos."""

    def calcular_costo_total(
        self,
        duracion_horas: int,
        impuesto: float = 0.19,
        descuento: Optional[float] = None,
        cargo_adicional: float = 0.0,
    ) -> float:
        """Método sobrecargado mediante parámetros opcionales para calcular costos finales.

        Permite calcular únicamente con duración e IVA por defecto, o incorporar
        porcentajes de descuento y cargos adicionales logísticos.
        """
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' ({self.id}) no se encuentra disponible."
            )
        if duracion_horas <= 0:
            raise CalculoInconsistenteError(
                f"La duración debe ser mayor a 0 horas (recibido: {duracion_horas})."
            )
        if impuesto < 0 or impuesto > 1:
            raise CalculoInconsistenteError(
                f"El impuesto debe estar entre 0 y 1 (recibido: {impuesto})."
            )
        if cargo_adicional < 0:
            raise CalculoInconsistenteError("El cargo adicional no puede ser negativo.")

        porcentaje_desc = 0.0 if descuento is None else float(descuento)
        if porcentaje_desc < 0 or porcentaje_desc >= 1:
            raise CalculoInconsistenteError(
                f"El descuento debe estar en el rango [0.0, 1.0) (recibido: {porcentaje_desc})."
            )

        subtotal = self.calcular_costo_base(duracion_horas) + float(cargo_adicional)
        monto_descuento = subtotal * porcentaje_desc
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + float(impuesto))

        if total <= 0:
            raise CalculoInconsistenteError("El cálculo final produjo un monto no positivo.")

        return round(total, 2)

    def validar_integridad(self) -> bool:
        return self.validar_parametros() and self._tarifa_hora > 0

    def obtener_resumen(self) -> str:
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas tecnológicas y de reuniones."""

    def __init__(
        self,
        servicio_id: str,
        nombre: str,
        tarifa_hora: float,
        capacidad: int,
        incluye_videoconferencia: bool = True,
        disponible: bool = True,
    ) -> None:
        super().__init__(servicio_id, nombre, tarifa_hora, disponible)
        self.capacidad = capacidad
        self.incluye_videoconferencia = incluye_videoconferencia
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self.capacidad <= 0 or self.capacidad > 200:
            raise DatosInvalidosError(
                f"Capacidad de sala fuera de rango (1-200): {self.capacidad}."
            )
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        recargo_tech = 15000.0 if self.incluye_videoconferencia else 0.0
        return (self.tarifa_hora * duracion_horas) + recargo_tech

    def describir_servicio(self) -> str:
        equipo = "con videoconferencia" if self.incluye_videoconferencia else "estándar"
        return (
            f"Sala [{self.id}] '{self.nombre}' | Capacidad: {self.capacidad} personas "
            f"({equipo}) | Tarifa: ${self.tarifa_hora:,.2f}/h"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de hardware y estaciones de trabajo."""

    def __init__(
        self,
        servicio_id: str,
        nombre: str,
        tarifa_hora: float,
        tipo_equipo: str,
        cantidad: int,
        disponible: bool = True,
    ) -> None:
        super().__init__(servicio_id, nombre, tarifa_hora, disponible)
        self.tipo_equipo = tipo_equipo
        self.cantidad = cantidad
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self.tipo_equipo or not str(self.tipo_equipo).strip():
            raise ParametroFaltanteError("Debe especificar el tipo de equipo a alquilar.")
        if self.cantidad <= 0:
            raise DatosInvalidosError(
                f"La cantidad de equipos debe ser al menos 1 (recibido: {self.cantidad})."
            )
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        return self.tarifa_hora * self.cantidad * duracion_horas

    def describir_servicio(self) -> str:
        return (
            f"Alquiler Equipo [{self.id}] '{self.nombre}' | Tipo: {self.tipo_equipo} "
            f"x{self.cantidad} und | Tarifa unitaria: ${self.tarifa_hora:,.2f}/h"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría de arquitectura y desarrollo de software."""

    MODALIDADES_VALIDAS = ("virtual", "presencial")

    def __init__(
        self,
        servicio_id: str,
        nombre: str,
        tarifa_hora: float,
        area_especialidad: str,
        modalidad: str = "virtual",
        disponible: bool = True,
    ) -> None:
        super().__init__(servicio_id, nombre, tarifa_hora, disponible)
        self.area_especialidad = area_especialidad
        self.modalidad = modalidad.strip().lower() if modalidad else ""
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self.area_especialidad or not str(self.area_especialidad).strip():
            raise ParametroFaltanteError("El área de especialidad de la asesoría es obligatoria.")
        if self.modalidad not in self.MODALIDADES_VALIDAS:
            raise DatosInvalidosError(
                f"Modalidad '{self.modalidad}' no válida. Use: {self.MODALIDADES_VALIDAS}."
            )
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        factor_modalidad = 1.15 if self.modalidad == "presencial" else 1.0
        return self.tarifa_hora * duracion_horas * factor_modalidad

    def describir_servicio(self) -> str:
        return (
            f"Asesoría [{self.id}] '{self.nombre}' | Área: {self.area_especialidad} "
            f"| Modalidad: {self.modalidad.capitalize()} | Tarifa: ${self.tarifa_hora:,.2f}/h"
        )