"""Módulo de configuración del sistema de registro de eventos y errores (Logs)."""

import logging
from pathlib import Path


def configurar_logger(nombre_logger: str = "SoftwareFJ") -> logging.Logger:
    """Configura y retorna un logger que escribe en archivo y consola.

    Args:
        nombre_logger: Identificador del logger del sistema.

    Returns:
        Instancia configurada de logging.Logger.
    """
    ruta_logs = Path("logs")
    ruta_logs.mkdir(parents=True, exist_ok=True)
    archivo_log = ruta_logs / "software_fj.log"

    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.INFO)

    # Evita duplicar manejadores si la función se invoca múltiples veces
    if not logger.handlers:
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        manejador_archivo = logging.FileHandler(archivo_log, encoding="utf-8")
        manejador_archivo.setLevel(logging.INFO)
        manejador_archivo.setFormatter(formato)

        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(formato)

        logger.addHandler(manejador_archivo)
        logger.addHandler(manejador_consola)

    return logger