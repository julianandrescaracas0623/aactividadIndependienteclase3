import asyncio
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from database import get_connection

app = FastAPI(title="Sistema de Citas Médicas")

class Paciente(BaseModel):
    nombre: str
    edad: int
    genero: str
    eps: str
    regimen: str


pacientes = []
paciente_id_counter = 1
citas_counter = 1


# Endpoint raíz
@app.get("/")
async def root():
    return {"mensaje": "¡Bienvenido al Sistema de Citas Médicas!"}


# Crear paciente
@app.post("/pacientes/crear", tags=["Pacientes"])
async def crear_paciente(paciente: Paciente):
    global paciente_id_counter

    nuevo_paciente = {
        "id": paciente_id_counter,
        "nombre": paciente.nombre,
        "edad": paciente.edad,
        "genero": paciente.genero,
        "eps": paciente.eps,
        "regimen": paciente.regimen,
        "fecha_registro": datetime.now().isoformat()
    }

    pacientes.append(nuevo_paciente)
    paciente_id_counter += 1

    return {
        "mensaje": "Paciente creado exitosamente",
        "paciente": nuevo_paciente
    }


# Listar pacientes
@app.get("/pacientes/listar", tags=["Pacientes"])
async def listar_pacientes():

    if not pacientes:
        return {
            "mensaje": "No hay pacientes registrados",
            "total": 0,
            "pacientes": []
        }

    return {
        "total": len(pacientes),
        "pacientes": pacientes
    }


# Buscar paciente por ID
@app.get("/pacientes/{paciente_id}", tags=["Pacientes"])
async def obtener_paciente(paciente_id: int):

    for paciente in pacientes:
        if paciente["id"] == paciente_id:
            return {"paciente": paciente}

    raise HTTPException(
        status_code=404,
        detail=f"Paciente con ID {paciente_id} no encontrado"
    )


# Crear cita
@app.post("/citas/crear", tags=["Citas"])
async def crear_cita(paciente: str, fecha: str):

    await asyncio.sleep(2)

    conn = await get_connection()
    cursor = await conn.cursor()

    query = """
INSERT INTO citas (paciente, fecha, estado) VALUES (%s, %s, %s)
"""

    await cursor.execute(query, (paciente, fecha, "Activa"))
    await conn.commit()

    await cursor.close()

    return {"mensaje": "cita creada correctamente"}


# Listar citas
@app.get("/citas/listar", tags=["Citas"])
async def listar_citas():

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas"

    await cursor.execute(query)
    citas = await cursor.fetchall()

    await cursor.close()
    conn.close()

    return citas


# Buscar citas por paciente
@app.get("/citas/paciente/{paciente}", tags=["Citas"])
async def buscar_citas_por_paciente(paciente: str):

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas WHERE paciente = %s"

    await cursor.execute(query, (paciente,))
    cita = await cursor.fetchall()

    await cursor.close()
    conn.close()

    if not cita:
        raise HTTPException(
            status_code=404,
            detail=f"Cita no encontrada"
        )

    return cita


# Cancelar cita
@app.delete("/citas/{id}", tags=["Citas"])
async def cancelar_cita(id: int):

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "UPDATE citas SET estado = 'Cancelada' WHERE id = %s"

    await cursor.execute(query, (id,))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "cita cancelada correctamente"}

# listar solo citas activas
@app.get("/citas/activas", tags=["Citas"])
async def citas_activas():
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas WHERE estado = 'Activa'"

    await cursor.execute(query)
    citas_activas = await cursor.fetchall()

    await cursor.close()
    conn.close()

    return citas_activas

# contar citas activas
@app.get("/citas/activas/count", tags=["Citas"])
async def contar_citas_activas():
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT COUNT(*) FROM citas WHERE estado = 'Activa'"

    await cursor.execute(query)
    count = await cursor.fetchone()

    await cursor.close()
    conn.close()

    return {"citas activas": count[0]}

# contar citas canceladas
@app.get("/citas/canceladas/count", tags=["Citas"])
async def contar_citas_canceladas():
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT COUNT(*) FROM citas WHERE estado = 'Cancelada'"

    await cursor.execute(query)
    count = await cursor.fetchone()

    await cursor.close()
    conn.close()

    return {"citas canceladas": count[0]}           

 # reactivar cita cancelada
@app.put("/citas/reactivar/{id}", tags=["Citas"])
async def reactivar_cita(id: int):

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "UPDATE citas SET estado = 'Activa' WHERE id = %s"

    await cursor.execute(query, (id,))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "cita reactivada correctamente"}

# actualizar fecha de cita
@app.put("/citas/actualizar/{id}", tags=["Citas"])
async def actualizar_fecha_cita(id: int, nueva_fecha: str):

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "UPDATE citas SET fecha = %s WHERE id = %s"

    await cursor.execute(query, (nueva_fecha, id))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "fecha de cita actualizada correctamente"}

# eliminar cita
@app.delete("/citas/eliminar/{id}", tags=["Citas"])
async def eliminar_cita(id: int):

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "DELETE FROM citas WHERE id = %s"

    await cursor.execute(query, (id,))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "cita eliminada correctamente"}

# listar citas por fecha
@app.get("/citas/fecha/{fecha}", tags=["Fecha"])
async def listar_citas_por_fecha(fecha: str):

    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas WHERE fecha = %s"

    await cursor.execute(query, (fecha,))
    citas_por_fecha = await cursor.fetchall()

    if not citas_por_fecha:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron citas para la fecha {fecha}"
        )

    await cursor.close()
    conn.close()

    return citas_por_fecha