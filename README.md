Resumen Programa 

Descripción: Este programa permite el control de acceso mediante reconocimiento facial, registra usuarios y verifica su acceso basado en su rostro y horario permitido.

Registro de Usuarios:
Usa la función registrar_usuario(nombre_usuario, imagen, nivel_acceso, horas_permitidas).
La imagen debe ser clara y mostrar bien el rostro.
La información se almacena en usuarios_autorizados.json en formato JSON.

Verificación de Acceso:
Usa la función control_acceso_camara(nivel_acceso_requerido).
Captura video desde la cámara y verifica si el rostro coincide con los usuarios registrados.
Registra el acceso en registro_acceso.csv en formato CSV.

Formato de Almacenamiento:
usuarios_autorizados.json: Almacena el nombre del usuario, su codificación facial, nivel de acceso y horas permitidas.
registro_acceso.csv: Almacena el nombre del usuario, la fecha y hora de acceso, y el nivel de acceso.


Program Summary

Description: This program allows access control through facial recognition, it registers users and verifies their access based on their face and allowed hours.

User Registration:
Use the function registrar_usuario(nombre_usuario, imagen, nivel_acceso, horas_permitidas).
The image must be clear and show the face well.
Information is stored in usuarios_autorizados.json in JSON format.

Access Verification:
Use the function control_acceso_camara(nivel_acceso_requerido).
Captures video from the camera and checks if the face matches registered users.
Logs access in registro_acceso.csv in CSV format.

Storage Format:
usuarios_autorizados.json: Stores the user's name, facial encoding, access level, and allowed hours.
registro_acceso.csv: Stores the user's name, date and time of access, and access level.
