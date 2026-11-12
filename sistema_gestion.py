"""Controlador principal en memoria para Software FJ (sin base de datos)."""

from typing import Optional
from entidades import Cliente
from excepciones import DatosInvalidosError, SoftwareFJError
from logger_config import configurar_logger
from reserva import Reserva
from servicios import Servicio


class SistemaSoftwareFJ:
    """Administra listas internas de clientes, servicios y reservas con tolerancia a fallos."""

    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self._logger = configurar_logger()
        self._logger.info("=== Sistema Integral Software FJ iniciado correctamente ===")

    def registrar_cliente(
        self,
        cliente_id: str,
        documento: str,
        nombre: str,
        correo: str,
        telefono: str,
    ) -> Optional[Cliente]:
        """Crea y almacena un cliente capturando cualquier error sin detener el sistema."""
        try:
            if any(c.id == cliente_id or c.documento == documento for c in self._clientes):
                raise DatosInvalidosError(
                    f"Ya existe un cliente registrado con ID '{cliente_id}' o documento '{documento}'."
                )
            nuevo_cliente = Cliente(cliente_id, documento, nombre, correo, telefono)
        except SoftwareFJError as err:
            self._logger.error("Registro de cliente fallido (%s): %s", cliente_id, err)
            return None
        else:
            self._clientes.append(nuevo_cliente)
            self._logger.info("Cliente registrado: %s", nuevo_cliente.obtener_resumen())
            return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> Optional[Servicio]:
        """Registra un servicio polimórfico en el catálogo interno."""
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto proporcionado no es un Servicio válido.")
            if any(s.id == servicio.id for s in self._servicios):
                raise DatosInvalidosError(f"El servicio con ID '{servicio.id}' ya existe.")
        except SoftwareFJError as err:
            self._logger.error("Registro de servicio fallido: %s", err)
            return None
        else:
            self._servicios.append(servicio)
            self._logger.info("Servicio registrado: %s", servicio.describir_servicio())
            return servicio

    def crear_reserva(
        self,
        reserva_id: str,
        cliente: Optional[Cliente],
        servicio: Optional[Servicio],
        duracion_horas: int,
        impuesto: float = 0.19,
        descuento: Optional[float] = None,
        cargo_adicional: float = 0.0,
    ) -> Optional[Reserva]:
        """Instancia una reserva aplicando validaciones y encadenamiento de excepciones."""
        try:
            if any(r.id == reserva_id for r in self._reservas):
                raise DatosInvalidosError(f"El ID de reserva '{reserva_id}' ya está en uso.")
            nueva_reserva = Reserva(
                reserva_id=reserva_id,
                cliente=cliente,  # type: ignore[arg-type]
                servicio=servicio,  # type: ignore[arg-type]
                duracion_horas=duracion_horas,
                impuesto=impuesto,
                descuento=descuento,
                cargo_adicional=cargo_adicional,
                logger=self._logger,
            )
        except SoftwareFJError as err:
            self._logger.error("Creación de reserva fallida (%s): %s", reserva_id, err)
            return None
        else:
            self._reservas.append(nueva_reserva)
            self._logger.info("Reserva creada: %s", nueva_reserva.obtener_resumen())
            return nueva_reserva

    def confirmar_reserva(self, reserva: Optional[Reserva]) -> bool:
        """Confirma una reserva existente de forma segura."""
        try:
            if reserva is None:
                raise DatosInvalidosError("No se proporcionó una reserva válida para confirmar.")
            reserva.confirmar()
            return True
        except SoftwareFJError as err:
            self._logger.error("Fallo controlado al confirmar reserva: %s", err)
            return False

    def procesar_reserva(self, reserva: Optional[Reserva]) -> bool:
        """Procesa una reserva confirmada de forma segura."""
        try:
            if reserva is None:
                raise DatosInvalidosError("No se proporcionó una reserva válida para procesar.")
            reserva.procesar()
            return True
        except SoftwareFJError as err:
            self._logger.error("Fallo controlado al procesar reserva: %s", err)
            return False

    def cancelar_reserva(self, reserva: Optional[Reserva], motivo: str = "") -> bool:
        """Cancela una reserva de forma segura."""
        try:
            if reserva is None:
                raise DatosInvalidosError("No se proporcionó una reserva válida para cancelar.")
            reserva.cancelar(motivo or "Cancelación administrativa")
            return True
        except SoftwareFJError as err:
            self._logger.error("Fallo controlado al cancelar reserva: %s", err)
            return False

    def generar_reporte_consola(self) -> None:
        """Imprime el estado final de las listas en memoria tras la simulación."""
        print("\n" + "=" * 75)
        print("RESUMEN FINAL EN MEMORIA - SOFTWARE FJ")
        print("=" * 75)
        print(f"Total Clientes activos:   {len(self._clientes)}")
        print(f"Total Servicios catálogo: {len(self._servicios)}")
        print(f"Total Reservas válidas:   {len(self._reservas)}")
        print("-" * 75)
        for reserva in self._reservas:
            print(f" • {reserva.obtener_resumen()}")
        print("=" * 75 + "\n")