# Sistema Medico Basico - API de Citas

API REST desarrollada con FastAPI para la gestion de pacientes y citas medicas.
El proyecto usa MySQL con `aiomysql` para operaciones asincronas.

## Tecnologias
- Python 3.10+
- FastAPI
- Uvicorn
- MySQL
- aiomysql

## Estructura del proyecto
```text
sistema_medico_basico/
|- README.md
|- citas_api/
|  |- main.py
|  |- database.py
```

## Requisitos previos
- Python instalado
- MySQL en ejecucion
- Base de datos `citas_db` creada
- Tabla `citas` creada (ejemplo de estructura abajo)

## Configuracion de base de datos
La conexion se configura en `citas_api/database.py`:

```python
DB_CONFIG = {
      "host": "localhost",
      "port": 3306,
      "user": "user",
      "password": "123",
      "db": "citas_db"
}
```

Ejemplo de tabla `citas`:

```sql
CREATE TABLE citas (
      id INT AUTO_INCREMENT PRIMARY KEY,
      paciente VARCHAR(120) NOT NULL,
      fecha VARCHAR(60) NOT NULL,
      estado VARCHAR(20) NOT NULL DEFAULT 'Activa'
);
```

## Instalacion
Desde la raiz del proyecto:

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn aiomysql
```

## Ejecucion
Ejecuta el servidor desde la carpeta `citas_api`:

```bash
cd citas_api
uvicorn main:app --reload
```

La API quedara disponible en:
- `http://127.0.0.1:8000`
- Documentacion Swagger: `http://127.0.0.1:8000/docs`

## Endpoints disponibles

### Generales
- `GET /` - Mensaje de bienvenida

### Pacientes
- `POST /pacientes/crear` - Crear paciente
- `GET /pacientes/listar` - Listar pacientes registrados en memoria
- `GET /pacientes/{paciente_id}` - Obtener paciente por ID

Ejemplo de body para crear paciente:

```json
{
   "nombre": "Ana Perez",
   "edad": 29,
   "genero": "F",
   "eps": "Sura",
   "regimen": "Contributivo"
}
```

### Citas
- `POST /citas/crear` - Crear cita (incluye delay simulado de 2 segundos)
- `GET /citas/listar` - Listar todas las citas
- `GET /citas/paciente/{paciente}` - Buscar citas por paciente
- `DELETE /citas/{id}` - Cancelar cita (estado = `Cancelada`)
- `GET /citas/activas` - Listar citas activas
- `GET /citas/activas/count` - Contar citas activas
- `GET /citas/canceladas/count` - Contar citas canceladas
- `PUT /citas/reactivar/{id}` - Reactivar una cita cancelada
- `PUT /citas/actualizar/{id}` - Actualizar fecha de cita
- `DELETE /citas/eliminar/{id}` - Eliminar cita de forma permanente
- `GET /citas/fecha/{fecha}` - Listar citas por fecha

Ejemplo para crear cita:

```bash
curl -X POST "http://127.0.0.1:8000/citas/crear?paciente=Ana%20Perez&fecha=2026-03-10%2010:00"
```

## Notas importantes
- Los pacientes se almacenan en memoria (`list` en `main.py`), por lo que se pierden al reiniciar el servidor.
- Las citas se almacenan en MySQL.
- Algunas rutas usan `Query Params` (por ejemplo `paciente` y `fecha` en `POST /citas/crear`).

