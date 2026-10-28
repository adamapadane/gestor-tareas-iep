# Guion para video (4-5 minutos)

**0:00-0:35 | Problema.** Presentar la dificultad de registrar, priorizar y seguir tareas de un equipo pequeno. Objetivo: una aplicacion sencilla y extensible.

**0:35-1:20 | Demostracion.** Ejecutar `python app.py agregar "Preparar entrega" --prioridad alta`; agregar otra tarea; mostrar `listar --orden prioridad`; completar la primera y volver a listar.

**1:20-2:15 | Factory Method.** Explicar `FabricaTareas.crear`: valida titulo y prioridad y concentra la construccion. Beneficio: consistencia y menos duplicacion.

**2:15-3:10 | Observer.** Explicar suscripcion del notificador y eventos de creacion y finalizacion. Beneficio: integrar en el futuro correo o registro sin modificar las operaciones principales.

**3:10-4:00 | Strategy.** Mostrar los ordenamientos por identificador y prioridad. Beneficio: cambiar el criterio sin alterar la logica del gestor.

**4:00-4:40 | Calidad y cierre.** Mostrar pruebas automatizadas y persistencia JSON. Indicar limitaciones: prototipo monousuario; un entorno empresarial requeriria base de datos, autenticacion y concurrencia. Cerrar con los beneficios de mantenibilidad y extensibilidad.

Subir el video a YouTube y colocar su enlace publico en el informe antes de la entrega.
