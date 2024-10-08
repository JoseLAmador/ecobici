# Patrón de uso Ecobici - Agosto 2024 🚴

Este estudio explora los patrones de uso del sistema Ecobici durante el mes de **agosto de 2024.** Se identifican **tendencias clave** relacionadas con el comportamiento de los usuarios, horarios y días más populares, distribución por género y edad, así como la demanda en diferentes ciclo estaciones. Los resultados ofrecen una base para futuros análisis que permitan seguir ajustando y evolucionando el servicio de movilidad urbana.

Se cuenta con **1,842,882** registros de viajes durante el mes de agosto 2024 y **677** ciclo estaciones disponibles

El conjunto de datos fue obtenido de [Ecobici - Datos Abiertos](https://ecobici.cdmx.gob.mx/datos-abiertos/).

## Prerequisitos

Antes de empezar, asegurate de tener los siguientes requerimientos:

- Tener un equipo _Windows/Linux/Mac_ con [Python 3.12.5+](https://www.python.org/).
- Tener actualizado [`pip`](https://pip.pypa.io/en/stable/installing/) and [`virtualenv`](https://virtualenv.pypa.io/en/stable/installation/) o `conda` ([Anaconda](https://www.anaconda.com/distribution/)).

- Descomprime los archivos: 2024-08.csv.zip | viajes_data_limpia.csv.zip

## Inicialización

Para instalar las dependencias necesarias, puedes seguir los siguientes pasos.

Clona el repositorio:

```bash
git clone https://github.com/JoseLAmador/ecobici.git
cd ecobici
```

Para crear y activar el entorno virtual, sigue los siguientes pasos:

**Usando `conda`**

```bash
$ conda create --name ecobici --file requerimientos.txt

# Activar entorno virtual:
$ conda activate ecobici

# Desactivar entorno virtual (cuando se requiera):
(ecobici)$ conda deactivate
```

**Using `virtualenv`**

```bash

$ virtualenv ecobici --python=python3

# Activar entorno virtual:
$ source ecobici/bin/activate

# Instala los requerimientos usando `pip`
(ecobici)$ pip install -r requerimientos.txt

# Desactivar entorno virtual (cuando se requiera):
(ecobici)$ deactivate
```

#### Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o deseas agregar nuevas funcionalidades, por favor, crea un issue o un pull request.

## Autor

- Jose Luis Amador

Copyright &copy; 2024 Jose Luis Amador
