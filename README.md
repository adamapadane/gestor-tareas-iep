# Gestor de tareas con patrones de diseño

Requisitos: Python 3.10 o superior. Sin dependencias externas.

Desde esta carpeta:

```bash
python app.py agregar "Preparar informe" --prioridad alta
python app.py agregar "Revisar pruebas" --prioridad media
python app.py listar --orden prioridad
python app.py completar 1
python app.py listar
python -m unittest discover -v
```

El archivo `tareas.json` se crea automaticamente en el directorio de ejecucion.

Patrones: Factory Method (FabricaTareas), Observer (Observador y NotificadorConsola) y Strategy (EstrategiaOrden y sus implementaciones). La persistencia es local JSON, adecuada para demostracion; para despliegue multiusuario se recomienda sustituirla por una base de datos y agregar control de concurrencia.
