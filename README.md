# Sistema de Citas Médicas (Microservicio)

Microservicio desarrollado con **FastAPI** para gestionar citas médicas.

## Funcionalidades solicitadas
- Crear cita
- Listar citas
- Buscar cita por paciente
- Cancelar cita

## Requisitos técnicos
- Uso de **FastAPI**
- Endpoints **async**
- Manejo de errores con **HTTPException**
- Simulación de delay de **2 segundos** al crear una cita

## Ejecución
1. Instalar dependencias:
   ```bash
   pip install fastapi uvicorn
   ```
2. Ejecutar el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Documentación interactiva
Abrir en el navegador:
- `http://127.0.0.1:8000/docs`

