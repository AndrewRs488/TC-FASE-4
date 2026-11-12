"""Punto de entrada con 12 simulaciones completas (válidas e inválidas) para Software FJ."""

from excepciones import SoftwareFJError
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from sistema_gestion import SistemaSoftwareFJ


def ejecutar_simulaciones() -> None:
    """Ejecuta 12 escenarios completos demostrando resiliencia y manejo de excepciones."""
    sistema = SistemaSoftwareFJ()

    # 1. Registro válido de Cliente 1
    cliente_1 = sistema.registrar_cliente(
        "CLI-001", "1090456789", "Laura Gómez", "laura.gomez@empresa.com", "3105551234"
    )

    # 2. Registro válido de Cliente 2
    cliente_2 = sistema.registrar_cliente(
        "CLI-002", "88234910", "Carlos Mendoza", "cmendoza@techcol.co", "3209876543"
    )

    # 3. Registro inválido de Cliente (correo mal formado y teléfono corto)
    sistema.registrar_cliente(
        "CLI-003", "1090111222", "Andrés Pérez", "correo_sin_arroba.com", "123"
    )

    # 4. Creación válida de Servicio 1: Reserva de Sala
    sala_juntas = None
    try:
        sala_juntas = ReservaSala(
            "SRV-01", "Sala Innovación A", 80000.0, capacidad=25, incluye_videoconferencia=True
        )
        sistema.registrar_servicio(sala_juntas)
    except SoftwareFJError as err:
        sistema._logger.error("Error instanciando Sala: %s", err)

    # 5. Creación válida de Servicio 2: Alquiler de Equipos
    equipos_dev = None
    try:
        equipos_dev = AlquilerEquipo(
            "SRV-02", "Workstations Linux", 35000.0, tipo_equipo="Portátil i7 32GB", cantidad=4
        )
        sistema.registrar_servicio(equipos_dev)
    except SoftwareFJError as err:
        sistema._logger.error("Error instanciando AlquilerEquipo: %s", err)

    # 6. Creación válida de Servicio 3: Asesoría Especializada
    asesoria_cloud = None
    try:
        asesoria_cloud = AsesoriaEspecializada(
            "SRV-03", "Arquitectura Cloud", 120000.0, "DevOps & AWS", modalidad="presencial"
        )
        sistema.registrar_servicio(asesoria_cloud)
    except SoftwareFJError as err:
        sistema._logger.error("Error instanciando AsesoriaEspecializada: %s", err)

    # 7. Creación inválida de Servicio (tarifa negativa -> DatosInvalidosError)
    try:
        servicio_erroneo = ReservaSala("SRV-ERR", "Sala Fantasma", -50000.0, capacidad=10)
        sistema.registrar_servicio(servicio_erroneo)
    except SoftwareFJError as err:
        sistema._logger.error("Simulación 7 - Creación de servicio rechazada: %s", err)

    # 8. Reserva exitosa y confirmación de Sala (cálculo estándar con IVA 19%)
    reserva_1 = sistema.crear_reserva("RES-101", cliente_1, sala_juntas, duracion_horas=3)
    sistema.confirmar_reserva(reserva_1)

    # 9. Reserva exitosa y procesamiento completo de Equipos (sobrecarga con descuento 10%)
    reserva_2 = sistema.crear_reserva(
        "RES-102",
        cliente_2,
        equipos_dev,
        duracion_horas=5,
        impuesto=0.19,
        descuento=0.10,
        cargo_adicional=20000.0,
    )
    sistema.confirmar_reserva(reserva_2)
    sistema.procesar_reserva(reserva_2)

    # 10. Reserva fallida por servicio no disponible (encadenamiento de excepciones)
    if asesoria_cloud is not None:
        asesoria_cloud.disponible = False
    sistema.crear_reserva("RES-103", cliente_1, asesoria_cloud, duracion_horas=2)

    # 11. Operación no permitida: intentar cancelar una reserva ya PROCESADA
    sistema.cancelar_reserva(reserva_2, motivo="Cambio de agenda")

    # 12. Cálculo inconsistente: intentar reservar con descuento del 150% (1.5)
    if asesoria_cloud is not None:
        asesoria_cloud.disponible = True
    sistema.crear_reserva(
        "RES-104", cliente_2, asesoria_cloud, duracion_horas=2, descuento=1.5
    )

    sistema.generar_reporte_consola()


if __name__ == "__main__":
    ejecutar_simulaciones()