import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Sistema de Citas Médicas")

class Paciente(BaseModel):
    nombre: str
    edad: int
    genero: str
    eps: str
    regimen: str

class Cita(BaseModel):
    paciente_id: int
    medico: str
    fecha: str  # Formato: "YYYY-MM-DD HH:MM"
    razon: str

pacientes = []
citas = []
paciente_id_counter = 1
cita_id_counter = 1

# 
@app.get("/") # Endpoint raíz para verificar que la API está funcionando
async def root():
    return {"mensaje": "¡Bienvenido al Sistema de Citas Médicas!"}


@app.post("/pacientes/crear") # Endpoint para crear un nuevo paciente
async def crear_paciente(paciente: Paciente):
    """Crear un nuevo paciente"""
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
    return {"mensaje": "Paciente creado exitosamente", "paciente": nuevo_paciente}

@app.get("/pacientes/listar") # Endpoint para listar todos los pacientes registrados
async def listar_pacientes():
    """Listar todos los pacientes registrados"""
    if not pacientes:
        return {"mensaje": "No hay pacientes registrados", "total": 0, "pacientes": []}
    return {"total": len(pacientes), "pacientes": pacientes}

@app.get("/pacientes/{paciente_id}")
async def obtener_paciente(paciente_id: int):
    """Buscar un paciente por su ID"""
    for paciente in pacientes:
        if paciente["id"] == paciente_id:
            return {"paciente": paciente}
    raise HTTPException(status_code=404, detail=f"Paciente con ID {paciente_id} no encontrado")


@app.post("/citas/crear") # Endpoint para crear una nueva cita médica con delay de 2 segundos
async def crear_cita(cita: Cita):
    """Crear una nueva cita médica con delay de 2 segundos"""
    # Validar que el paciente existe
    paciente_existe = any(p["id"] == cita.paciente_id for p in pacientes)
    if not paciente_existe:
        raise HTTPException(status_code=404, detail=f"Paciente con ID {cita.paciente_id} no encontrado")
    
    # Simular delay de 2 segundos
    await asyncio.sleep(2)
    
    global cita_id_counter
    nueva_cita = {
        "id": cita_id_counter,
        "paciente_id": cita.paciente_id,
        "medico": cita.medico,
        "fecha": cita.fecha,
        "razon": cita.razon,
        "estado": "programada",
        "fecha_creacion": datetime.now().isoformat()
    }
    citas.append(nueva_cita)
    cita_id_counter += 1
    return {"mensaje": "Cita creada exitosamente", "cita": nueva_cita}

@app.get("/citas/listar") # Endpoint para listar todas las citas médicas
async def listar_citas():
    """Listar todas las citas médicas"""
    if not citas:
        return {"mensaje": "No hay citas registradas", "total": 0, "citas": []}
    return {"total": len(citas), "citas": citas}

@app.get("/citas/paciente/{paciente_id}") # Endpoint para buscar citas de un paciente específico
async def buscar_citas_por_paciente(paciente_id: int):
    """Buscar citas de un paciente específico"""
    # Validar que el paciente existe
    paciente_existe = any(p["id"] == paciente_id for p in pacientes)
    if not paciente_existe:
        raise HTTPException(status_code=404, detail=f"Paciente con ID {paciente_id} no encontrado")
    
    citas_paciente = [c for c in citas if c["paciente_id"] == paciente_id]
    
    if not citas_paciente:
        return {"mensaje": f"No hay citas para el paciente {paciente_id}", "total": 0, "citas": []}
    
    return {"total": len(citas_paciente), "paciente_id": paciente_id, "citas": citas_paciente}

@app.delete("/citas/{cita_id}/cancelar") # Endpoint para cancelar una cita médica
async def cancelar_cita(cita_id: int):
    """Cancelar una cita médica"""
    for cita in citas:
        if cita["id"] == cita_id:
            if cita["estado"] == "cancelada":
                raise HTTPException(status_code=400, detail="La cita ya fue cancelada")
            cita["estado"] = "cancelada"
            cita["fecha_cancelacion"] = datetime.now().isoformat()
            return {"mensaje": "Cita cancelada exitosamente", "cita": cita}
    
    raise HTTPException(status_code=404, detail=f"Cita con ID {cita_id} no encontrada")

       





