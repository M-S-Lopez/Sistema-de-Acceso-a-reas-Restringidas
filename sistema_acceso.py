import pyttsx3  # convierte texto en voz
import face_recognition as fr # reconocimiento facial
import cv2 # procesamiento de imágenes y visión artificial
import os # manejar operaciones del sistema de archivos
import json #  lee y escribe archivos en formato JSON
from datetime import datetime # trabajar con fechas y horas
import csv # lee y escribe archivos en formato CSV

# Opciones de voz / idioma
# id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
# id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

# Texto a voz
def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)

    # Establecer una nueva velocidad (más baja)
    engine.setProperty('rate', 180) 

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Cargar la base de datos de usuarios autorizados
def cargar_usuarios_autorizados(archivo_json='usuarios_autorizados.json'):
    if not os.path.exists(archivo_json):
        # Si no existe el archivo, crearlo con un diccionario vacío
        with open(archivo_json, 'w') as file:
            json.dump({}, file)
        print(f"Archivo {archivo_json} creado.")

    try:
        with open(archivo_json, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error al leer el archivo {archivo_json}. Asegúrate de que esté bien formado.")
        return {}

# Registrar un nuevo usuario con nivel de acceso y horario
def registrar_usuario(nombre_usuario, imagen, nivel_acceso, horas_permitidas, archivo_json='usuarios_autorizados.json'):
    usuarios_conocidos = cargar_usuarios_autorizados(archivo_json)
    
    # Cargar y codificar la imagen del nuevo usuario
    imagen_usuario = fr.load_image_file(imagen)
    usuario_imagen_codificada = fr.face_encodings(imagen_usuario)
    
    if len(usuario_imagen_codificada) > 0:
        # Si se detectó al menos una cara, tomamos la primera
        usuario_codificado = usuario_imagen_codificada[0]
        
        # Guardar la codificación junto con nivel de acceso y horarios
        usuarios_conocidos[nombre_usuario] = {
            "codificado": usuario_codificado.tolist(),
            "nivel_acceso": nivel_acceso,  # Nivel de acceso
            "horas_permitidas": horas_permitidas # Horas permitidas (formato 24 horas)
        }
        
        # Guardar en archivo JSON
        with open(archivo_json, 'w') as file:
            json.dump(usuarios_conocidos, file)
        
        print(f"Usuario {nombre_usuario} registrado exitosamente con nivel de acceso {nivel_acceso}.")
    else:
        print(f"No se detectó ninguna cara en la imagen {imagen}. Asegúrate de que la imagen tenga un rostro reconocible.")

# Verificar si un usuario tiene acceso condicional basado en su horario
def acceso_horario(info_usuario):
    horario_actual = datetime.now().strftime("%H:%M")
    hora_inicio, hora_final = info_usuario["horas_permitidas"]
    
    if hora_inicio <= horario_actual <= hora_final:
        return True
    else:
        print(f"Acceso denegado para {info_usuario}, fuera del horario permitido.")
        return False

# Guardar el acceso en un archivo CSV
def archivo_registro(nombre_usuario, nivel_accedido, archivo_registro='registro_acceso.csv'):
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo_registro, 'a', newline='') as file:
        escribir = csv.writer(file)
        escribir.writerow([nombre_usuario, fecha_hora_actual, nivel_accedido])
    print(f"Acceso registrado al nivel {nivel_accedido} para {nombre_usuario} en {fecha_hora_actual}")

# Verificar el acceso del usuario basado en el nivel de acceso
def verificar_acceso(frame, usuarios_autorizados, nivel_acceso_requerido):
    # Convertir la imagen capturada (frame) a formato RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar caras y obtener codificaciones
    detectar_rostro = fr.face_locations(rgb_frame)
    rostros_codificados = fr.face_encodings(rgb_frame, detectar_rostro)
    
    for rostro_codificado in rostros_codificados:
        # Comparar cada cara detectada con las codificaciones de usuarios autorizados
        for nombre_usuario, info_usuario in usuarios_autorizados.items():
            coincide = fr.compare_faces([info_usuario["codificado"]], rostro_codificado)
            if coincide[0]:
                # Verificar si el usuario tiene el nivel de acceso necesario
                if info_usuario["nivel_acceso"] >= nivel_acceso_requerido:
                    # Verificar si el acceso está permitido por el horario
                    if acceso_horario(info_usuario):
                        hablar(f"Acceso concedido para {nombre_usuario}, Nivel de acceso: {info_usuario['nivel_acceso']}")
                        archivo_registro(nombre_usuario, nivel_acceso_requerido)  # Registrar el acceso en el CSV
                        return nombre_usuario
                    else:
                        hablar(f"Acceso denegado para {nombre_usuario}, fuera del horario permitido.")
                        return None
                else:
                    hablar(f"Acceso denegado para {nombre_usuario}, nivel de acceso insuficiente.")
                    return None
    
    hablar("Acceso denegado: Usuario no autorizado.")
    return None

# Configuración de la cámara
def control_acceso_camara(nivel_acceso_requerido):
    # Cargar usuarios autorizados
    usuarios_autorizados = cargar_usuarios_autorizados()
    
    # Capturar video desde la cámara
    video_captura = cv2.VideoCapture(0)
    #esta comentado porque saca fotos cada segundo, y el asistente de voz se vuelve medio loco
    """while True:
        # Capturar un frame del video
        ret, frame = video_captura.read()
        
        if not ret:
            print("Error al capturar la imagen.")
            break
        
        # Verificar acceso basado en el nivel y condiciones
        nombre_usuario = verify_access(frame, usuarios_autorizados, nivel_acceso_requerido)
        
        # Mostrar la imagen con el resultado en tiempo real
        cv2.imshow('Video', frame)
        
        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break """

    # Capturar un frame del video
    ret, frame = video_captura.read()
    
    if not ret:
        print("Error al capturar la imagen.")

    # Verificar acceso basado en el nivel y condiciones
    nombre_usuario = verificar_acceso(frame, usuarios_autorizados, nivel_acceso_requerido)   

    # Mostrar la imagen con el resultado en tiempo real
    cv2.imshow('Video', frame)   
        
    # Mantener ventana abierta
    cv2.waitKey(0)

    # Liberar la cámara y cerrar ventanas
    video_captura.release()
    cv2.destroyAllWindows()

# Ejemplo de uso:

# Registrar un nuevo usuario --> registrar_usuario(nombre del usuario, imagen, nivel de acceso, horas permitidas)
#(user_1, nivel_acceso=1,horas_permitidas=["00:00", "29:59"])
# Formato de allowed_hours: ["HH:MM", "HH:MM"] en formato 24 horas

registrar_usuario("Martin Lopez", "FotoA.jpeg", nivel_acceso=3, horas_permitidas=["08:00", "17:00"])
#registrar_usuario("Albert Castillo", "FotoB.png", nivel_acceso=3, horas_permitidas=["8:00", "15:59"])
#registrar_usuario("Joquin Sanchez", "FotoC.png", nivel_acceso=3, horas_permitidas=["00:00", "07:59"])

# Iniciar el control de acceso por cámara con un nivel de acceso requerido (ejemplo: 2)

control_acceso_camara(nivel_acceso_requerido=2)