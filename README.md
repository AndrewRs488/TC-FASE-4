# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para el componente práctico **Fase 4** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción General

Aplicación desarrollada en Python bajo el paradigma de **Programación Orientada a Objetos (POO)**, sin motores de bases de datos, diseñada para gestionar clientes, catálogo de servicios y reservas de la empresa **Software FJ**. El sistema opera en memoria mediante colecciones internas y garantiza continuidad operativa ante fallos mediante una jerarquía de excepciones personalizadas, bloques `try/except/else/finally`, encadenamiento de excepciones (`raise ... from ...`) y auditoría continua en archivo de logs.

## Principios y Arquitectura Implementada

* **Abstracción y Herencia:** Clase base abstracta `EntidadSistema` y clase abstracta `Servicio` de la cual heredan tres servicios especializados (`ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`).
* **Polimorfismo y Sobrecarga:** Sobrescritura de los métodos `validar_parametros()`, `describir_servicio()` y `calcular_costo_base()`, junto con el método sobrecargado mediante parámetros opcionales `calcular_costo_total()` (impuestos, descuentos y cargos adicionales).
* **Encapsulación:** Protección de atributos mediante propiedades (`@property`) y *setters* con validación estricta en `Cliente`, `Servicio` y `Reserva`.
* **Manejo Avanzado de Excepciones y Logs:** Jerarquía propia derivada de `SoftwareFJError` (`DatosInvalidosError`, `ParametroFaltanteError`, `OperacionNoPermitidaError`, `ReservaInvalidaError`, `ServicioNoDisponibleError`, `CalculoInconsistenteError`) con registro automático en `logs/software_fj.log`.

## Estructura del Repositorio

```text
TC-FASE-4/
├── logger_config.py     # Configuración centralizada de auditoría en consola y archivo
├── excepciones.py       # Jerarquía de excepciones personalizadas (SoftwareFJError)
├── entidades.py         # Clase abstracta EntidadSistema y clase encapsulada Cliente
├── servicios.py         # Clase abstracta Servicio y 3 subclases polimórficas
├── reserva.py           # Clase Reserva con gestión de estados y encadenamiento
├── sistema_gestion.py   # Controlador principal en memoria (_clientes, _servicios, _reservas)
├── main.py              # Script principal con 12 simulaciones válidas e inválidas
├── logs/                # Directorio generado automáticamente con software_fj.log
├── .gitignore           # Exclusión de caché y archivos temporales de Python
└── README.md            # Documentación técnica del proyecto