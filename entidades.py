"""Módulo de entidades base y gestión encapsulada de clientes."""

from abc import ABC, abstractmethod
from datetime import datetime
import re
from excepciones import DatosInvalidosError, ParametroFaltanteError


class EntidadSistema(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, entidad_id: str) -> None:
        if not entidad_id or not str(entidad_id).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        self._id: str = str(entidad_id).strip()
        self._fecha_creacion: datetime = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora de creación de la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Devuelve una representación legible de la entidad."""

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Verifica que el estado interno de la entidad sea consistente."""


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones."""

    def __init__(
        self,
        cliente_id: str,
        documento: str,
        nombre: str,
        correo: str,
        telefono: str,
    ) -> None:
        super().__init__(cliente_id)
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._activo: bool = True

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El documento de identidad es obligatorio.")
        doc_limpio = str(valor).strip()
        if not doc_limpio.isdigit() or len(doc_limpio) < 6:
            raise DatosInvalidosError(
                f"Documento inválido '{valor}': debe contener al menos 6 dígitos."
            )
        self._documento = doc_limpio

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(str(valor).strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, str(valor).strip()):
            raise DatosInvalidosError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = str(valor).strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono de contacto es obligatorio.")
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or not (7 <= len(tel_limpio) <= 15):
            raise DatosInvalidosError(
                f"Teléfono inválido '{valor}': debe tener entre 7 y 15 dígitos."
            )
        self._telefono = tel_limpio

    @property
    def activo(self) -> bool:
        return self._activo

    def desactivar(self) -> None:
        """Marca al cliente como inactivo dentro del sistema."""
        self._activo = False

    def validar_integridad(self) -> bool:
        """Confirma que el cliente esté activo y tenga sus atributos completos."""
        return bool(self._activo and self._documento and self._nombre and self._correo)

    def obtener_resumen(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente [{self.id}] - {self.nombre} (Doc: {self.documento}, "
            f"Email: {self.correo}, Estado: {estado})"
        )