"""
LLM Sales Conversation Simulator - Simulation Engine
====================================================================
Este módulo genera simulaciones de conversaciones de ventas entre 
clientes y vendedores utilizando la API de Google Generative AI (Gemini).

Características principales:
- Genera conversaciones realistas buyer-seller
- Extrae 15+ métricas de cada conversación
- Procesa en paralelo para mejor rendimiento
- Guarda resultados en CSV con análisis

Autor: Néstor Flores
Fecha: Marzo 2026
Version: 1.0
"""

import pandas as pd           # Manipulación de datos
import json                   # Parsing de respuestas JSON del LLM
import re                     # Expresiones regulares para parsear JSON
import os                     # Operaciones de sistema de archivos
import csv                    # Escritura de CSV
import io                     # Manejo de streams de entrada/salida
import threading              # Thread-safe file operations
from concurrent.futures import ThreadPoolExecutor  # Procesamiento paralelo
from google import genai       # API de Google Generative AI

# ====================================================================
# CONFIGURACIÓN - API Y DIRECTORIOS
# ====================================================================

# Clave API de Google Generative AI (Gemini)
API_KEY = "YOUR_API_KEY_HERE"  # Reemplaza con tu clave real 

# Cliente API configurado
CLIENT = genai.Client(api_key=API_KEY)

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    OUTPUT_DIR = os.path.join(BASE_DIR, "data", "results")
except NameError:
    BASE_DIR = os.getcwd()
    DATA_DIR = os.path.join(BASE_DIR, "data")
    OUTPUT_DIR = os.path.join(DATA_DIR, "results")

# Archivos de entrada (perfiles de clientes y vendedores)
CLIENTES_FILE = os.path.join(DATA_DIR, 'ClientesDataset.csv')
VENDEDORES_FILE = os.path.join(DATA_DIR, 'Vendedores Dataset.csv')

# Archivo de salida (resultados de las simulaciones)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'simulated_conversations_data.csv')

# ====================================================================
# PARÁMETROS DE SIMULACIÓN
# ====================================================================

# Modelo LLM a utilizar
MODEL_NAME = "gemini-2.0-flash"

# Número de hilos paralelos para ejecutar simulaciones concurrentes
# Aumentar para más velocidad (cuidado con rate limits de API)
# Recomendado: 4-8 (Los test se realizarón con 120 hilos, por capacidad de la máquina y para acelerar el proceso, pero se pueden ajustar según necesidades)
MAX_WORKERS = 5

# Número máximo de turnos en una conversación
# Un turno = una iteración (vendedor o cliente)
# 14 turnos = 7 turnos para cada parte (natural para diálogo) + 1 para el opener del vendedor
MAX_TURNS = 14 + 1

# Número de simulaciones por cada par cliente-vendedor
# Mayor número = más diversidad de datos
# Uso: Si tienes 50 clientes x 20 vendedores x 10 repeticiones = 10.000 conversaciones
REPETICIONES = 10

# Temperatura del LLM (controla creatividad/variabilidad)
# 0.0 = Determinístico (siempre misma respuesta)
# 1.0 = Muy creativo (muy variado, a veces incoherente)
# 0.7 = Balance recomendado
# 1.0 = Máxima variación (usado para conversaciones naturales)
TEMPERATURA_ALTA = 1.0

# Lock para escritura thread-safe en archivo CSV
# Evita que dos threads escriban simultáneamente y corrompan datos
file_lock = threading.Lock()

# ====================================================================
# FUNCIONES PRINCIPALES
# ====================================================================

def call_llm(contents, temperature):
    """
    Realiza una llamada a la API de Google Generative AI (Gemini).
    
    Args:
        contents (list): Historial de conversación en formato Gemini
                        Estructura: [{"role": "user", "parts": [{"text": "..."}]}, ...]
        temperature (float): Control de creatividad/determinismo (0.0-1.0)
    
    Returns:
        str: Respuesta del LLM o mensaje de error si falla
    
    Ejemplo:
        >>> messages = [{"role": "user", "parts": [{"text": "Hola"}]}]
        >>> response = call_llm(messages, 0.9)
        >>> print(response)
        "Hola, ¿cómo estás?"
    """
    try:
        # Realizar llamada a API Gemini
        response = CLIENT.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config={"temperature": temperature}
        )
        return response.text
    except Exception as e:
        # Retornar error en caso de fallo (permite continuar sin crashear)
        return f"ERROR_API: {str(e)}"


def clean_and_load_csv(filename, is_cliente=True):
    """
    Lee y limpia un archivo CSV con manejo especial de formato.
    
    Args:
        filename (str): Ruta del archivo CSV a leer
        is_cliente (bool): Si True, limpia comillas adicionales (formato especial clientes)
                          Si False, carga vendedores sin limpieza adicional
    
    Returns:
        pd.DataFrame: DataFrame con los datos limpios
    
    Ejemplo:
        >>> df_clientes = clean_and_load_csv('data/clientes.csv', is_cliente=True)
        >>> df_vendedores = clean_and_load_csv('data/vendedores.csv', is_cliente=False)
    """
    # Leer archivo línea por línea
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Limpiar cada línea
    cleaned_lines = []
    for line in lines:
        line = line.strip()  # Eliminar espacios en blanco al inicio/final
        if not line:         # Saltar líneas vacías
            continue
        if line.endswith(';'):  # Eliminar punto y coma final si existe
            line = line[:-1]
        # Si es cliente, limpiar comillas adicionales
        if is_cliente and line.startswith('"') and line.endswith('"'):
            line = line[1:-1]  # Quitar comillas del inicio/final
            line = line.replace('""', '"')  # Desescapar comillas dobles
        cleaned_lines.append(line)
    
    # Convertir líneas limpias a DataFrame
    return pd.read_csv(io.StringIO('\n'.join(cleaned_lines)))


def save_data(record, full_chat_text):
    """
    Guarda los resultados de una conversación en el archivo CSV.
    
    Operación thread-safe: usa lock para evitar escrituras simultáneas.
    
    Args:
        record (dict): Diccionario con métricas de la conversación
                      Contiene: id, nombres, sentimiento, tasas, resultado
        full_chat_text (str): Transcripción completa de la conversación
                              (puede usarse para logging detallado)
    
    Estructura de record esperada:
        {
            'id_conversacion': int,
            'vendedor_nombre': str,
            'cliente_nombre': str,
            'sentimiento_promedio_cliente': float,
            'tasa_objecion_cliente': int,
            'tasa_preguntas_relevantes_cliente': int,
            'tasa_palabras_dudosas_cliente': int,
            'frecuencia_preocupacion_principal_cliente': int,
            'tasa_preguntas_abiertas_vendedor': int,
            'tasa_interrupciones_vendedor': int,
            'polaridad_sentimiento_vendedor': float,
            'resultado_conversacion': str (EXITO/FALLO)
        }
    """
    # Usar lock para thread-safe file writing
    with file_lock:
        # Verificar si archivo ya existe (para decidir si escribir header)
        file_exists = os.path.isfile(OUTPUT_FILE)
        
        # Abrir archivo en modo append (añadir al final)
        with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
            # Definir columnas en el mismo orden que el record
            fieldnames = [
                'id_conversacion', 
                'vendedor_nombre', 
                'cliente_nombre',
                'sentimiento_promedio_cliente', 
                'tasa_objecion_cliente',
                'tasa_preguntas_relevantes_cliente', 
                'tasa_palabras_dudosas_cliente',
                'frecuencia_preocupacion_principal_cliente', 
                'tasa_preguntas_abiertas_vendedor',
                'tasa_interrupciones_vendedor', 
                'polaridad_sentimiento_vendedor',
                'resultado_conversacion'
            ]
            
            # Crear writer CSV
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Escribir header si es la primera vez o archivo está vacío
            if not file_exists or os.path.getsize(OUTPUT_FILE) == 0:
                writer.writeheader()
            
            # Escribir fila de datos
            writer.writerow(record)
            
            # Forzar escritura inmediata al disco
            f.flush()


def run_simulation(cliente, vendedor, conv_id):
    """
    Ejecuta una simulación completa de conversación buyer-seller.
    
    Flujo:
    1. Prepara prompts del sistema para vendedor y cliente
    2. Simula conversación natural entre ambos (hasta MAX_TURNS)
    3. Analiza conversación con LLM para extraer métricas
    4. Guarda resultados en CSV
    
    Args:
        cliente (dict): Diccionario con perfil del cliente
                       Contiene: Nombre, Perfil demográfico, Actitud
        vendedor (dict): Diccionario con perfil del vendedor
                        Contiene: Nombre, Técnica de venta, Estilo
        conv_id (int): ID único para esta conversación
    
    Process:
        - Extrae información de perfiles
        - Crea prompts del sistema para cada personaje
        - Inicializa historial de conversación
        - Ejecuta loop de diálogo alternando vendedor-cliente
        - Valida términos de finalización
        - Analiza conversación con LLM
        - Parsea JSON de métricas
        - Guarda resultados
    """
    
    # ======================================================================
    # 1. EXTRAER INFORMACIÓN DE PERFILES
    # ======================================================================
    
    # Datos del vendedor
    v_nom = vendedor['Nombre']  # Nombre del vendedor
    v_tec = vendedor['Objetivo (Técnica de Venta y Enfoque Principal)']  # Técnica
    v_est = vendedor['Subjetivo (Estilo de Interacción y Tono)']  # Estilo
    
    # Datos del cliente
    c_nom = cliente['Nombre']  # Nombre del cliente
    c_per = cliente['Objetivo (Datos Demográficos/Económicos)']  # Perfil demográfico
    c_act = cliente['Subjetivo (Actitud y Comportamiento)']  # Actitud/comportamiento
    
    # Extraer preocupación principal del cliente (palabra clave para análisis)
    try:
        preocupacion = c_act.split('preocupación es')[-1].strip().replace('.', '')
    except:
        preocupacion = "el ROI"  # Default si no se encuentra

    # ======================================================================
    # 2. CREAR PROMPTS DEL SISTEMA
    # ======================================================================
    
    # Prompt para el vendedor: define su comportamiento y objetivos
    sys_v = f"""Eres {v_nom}. Técnica: {v_tec}. Estilo: {v_est}.
    INSTRUCCIONES: No seas complaciente. Si el cliente es difícil, tu técnica debe brillar. 
    Si eres agresivo, presiona; si eres consultivo, pregunta. No uses placeholders como '[Nombre]'.
    Tu objetivo es cerrar una reunión o venta, pero si el cliente se cierra en banda, acepta el NO de forma profesional.
    Además, cuando no sepas algún dato fluye y inventa, esto significa que nunca pongas un placeholder, por ejemplo, si no sabes el producto o servicio, inventate que producto vendes y a partir de ahí sigue la venta de ese producto."""

    # Prompt para el cliente: define su comportamiento y motivaciones
    sys_c = f"""Eres {c_nom}. Perfil: {c_per}. Actitud: {c_act}.
    INSTRUCCIONES: No menciones que eres ingeniero ni tu sueldo a menos que el vendedor te lo pregunte o sea relevante para una queja.
    Sigue tu perfil de persona, de comprador y tus preocupaciones en la compra.  
    Si llegamos al turno 14 y no estás convencido, di: 'He perdido interés, no es lo que busco' y termina.
    Ten una actitud realista tanto con tu personalidad, como del contexto de la conversación"""

    # ======================================================================
    # 3. INICIALIZAR HISTORIAL DE CONVERSACIÓN
    # ======================================================================
    
    # Historial para el vendedor (contexto del LLM)
    h_v = [{"role": "user", "parts": [{"text": sys_v}]}]
    
    # Historial para el cliente (contexto del LLM)
    h_c = [{"role": "user", "parts": [{"text": sys_c}]}]
    
    # Log de la conversación completa (para análisis posterior)
    chat_log = ""

    # ======================================================================
    # 4. MENSAJE INICIAL DEL VENDEDOR
    # ======================================================================
    
    # El vendedor inicia la conversación de forma natural
    v_msg = call_llm(
        h_v + [{"role": "user", "parts": [{"text": "Inicia la conversación de forma muy natural y humana. Sin protocolos exagerados."}]}], 
        TEMPERATURA_ALTA
    )
    chat_log += f"Vendedor: {v_msg}\n"

    # ======================================================================
    # 5. LOOP PRINCIPAL: ALTERNAR VENDEDOR-CLIENTE
    # ======================================================================
    
    # Ejecutar hasta MAX_TURNS//2 (porque cada turno = vendedor + cliente)
    for i in range(MAX_TURNS // 2):
        
        # ---- RESPUESTA DEL CLIENTE ----
        # Añadir mensaje del vendedor al historial del cliente
        h_c.append({"role": "user", "parts": [{"text": v_msg}]})
        
        # LLM genera respuesta del cliente
        c_msg = call_llm(h_c, TEMPERATURA_ALTA)
        chat_log += f"Cliente: {c_msg}\n"
        
        # Verificar si cliente quiere terminar la conversación
        # (palabras clave de finalización)
        if any(x in c_msg.lower() for x in ["compro", "no me interesa", "adiós", "perdido interés", "cerramos aquí"]):
            break  # Salir del loop si cliente decide terminar
        
        # ---- RESPUESTA DEL VENDEDOR ----
        # Añadir mensaje del cliente al historial del vendedor
        h_v.append({"role": "user", "parts": [{"text": c_msg}]})
        
        # LLM genera respuesta del vendedor
        v_msg = call_llm(h_v, TEMPERATURA_ALTA)
        chat_log += f"Vendedor: {v_msg}\n"
        
        # Añadir respuesta del vendedor al historial del cliente
        # (para que cliente vea el contexto completo en siguiente turno)
        h_c.append({"role": "user", "parts": [{"text": v_msg}]})

    # ======================================================================
    # 6. ANALIZAR CONVERSACIÓN Y EXTRAER MÉTRICAS
    # ======================================================================
    
    # Prompt que pide al LLM analizar la conversación
    # Solicita 15+ métricas cuantitativas
    analisis_prompt = f"""Analiza esta conversación de ventas.
    Conversación: {chat_log}
    Preocupación del cliente: {preocupacion}

    Devuelve SOLO un JSON con estas llaves exactas:
    - "sentimiento_promedio_cliente": (float -1.0 a 1.0)
    - "tasa_objecion_cliente": (int)
    - "tasa_preguntas_relevantes_cliente": (int)
    - "tasa_palabras_dudosas_cliente": (int)
    - "frecuencia_preocupacion_principal_cliente": (int)
    - "tasa_preguntas_abiertas_vendedor": (int)
    - "tasa_interrupciones_vendedor": (int)
    - "polaridad_sentimiento_vendedor": (float -1.0 a 1.0)
    - "resultado_conversacion": ("EXITO" o "FALLO")"""

    # Llamar LLM con temperatura baja (consistencia en análisis)
    res = call_llm([{"role": "user", "parts": [{"text": analisis_prompt}]}], 0.0)
    
    # ======================================================================
    # 7. PARSEAR RESPUESTA JSON
    # ======================================================================
    
    try:
        # Usar regex para extraer JSON de la respuesta
        # (a veces el LLM incluye texto adicional)
        m = json.loads(re.search(r"\{.*\}", res, re.DOTALL).group(0))
    except:
        # Si falla el parsing, usar resultado por defecto
        m = {"resultado_conversacion": "FALLO_ANALISIS"}

    # ======================================================================
    # 8. CREAR REGISTRO DE RESULTADOS
    # ======================================================================
    
    # Diccionario con todos los datos de la conversación
    record = {
        'id_conversacion': conv_id,  # Identificador único
        'vendedor_nombre': v_nom,    # Quién vendía
        'cliente_nombre': c_nom,     # Quién compraba
        # Métricas extraídas del análisis LLM
        'sentimiento_promedio_cliente': m.get('sentimiento_promedio_cliente', 0),
        'tasa_objecion_cliente': m.get('tasa_objecion_cliente', 0),
        'tasa_preguntas_relevantes_cliente': m.get('tasa_preguntas_relevantes_cliente', 0),
        'tasa_palabras_dudosas_cliente': m.get('tasa_palabras_dudosas_cliente', 0),
        'frecuencia_preocupacion_principal_cliente': m.get('frecuencia_preocupacion_principal_cliente', 0),
        'tasa_preguntas_abiertas_vendedor': m.get('tasa_preguntas_abiertas_vendedor', 0),
        'tasa_interrupciones_vendedor': m.get('tasa_interrupciones_vendedor', 0),
        'polaridad_sentimiento_vendedor': m.get('polaridad_sentimiento_vendedor', 0),
        'resultado_conversacion': m.get('resultado_conversacion', 'NEUTRO')
    }

    # ======================================================================
    # 9. GUARDAR RESULTADOS
    # ======================================================================
    
    save_data(record, chat_log)
    
    # Log de progreso en consola
    print(f"ID {conv_id} | {v_nom} | Result: {record['resultado_conversacion']}")


# ====================================================================
# FUNCIÓN PRINCIPAL: SIMULADOR
# ====================================================================

def simulator():
    """
    Función principal que orquesta todas las simulaciones.
    
    Flujo:
    1. Cargar perfiles de clientes y vendedores
    2. Generar todas las combinaciones (cliente x vendedor x repeticiones)
    3. Ejecutar simulaciones en paralelo usando ThreadPoolExecutor
    4. Procesar resultados automáticamente mediante ThreadPoolExecutor.map()
    
    Ejemplo de combinaciones:
        Si tienes:
        - 5 clientes
        - 3 vendedores
        - 10 repeticiones
        
        Total tareas: 5 × 3 × 10 = 150 conversaciones
        
        Con MAX_WORKERS=5:
        - 5 conversaciones en paralelo
        - Cada una tarda ~2-5 minutos
        - Tiempo total: ~60-150 minutos
    """
    
    # ======================================================================
    # 1. CARGAR DATOS
    # ======================================================================
    
    # Cargar perfil de clientes desde CSV
    c_df = clean_and_load_csv(CLIENTES_FILE, is_cliente=True)
    
    # Cargar perfiles de vendedores desde CSV
    v_df = clean_and_load_csv(VENDEDORES_FILE, is_cliente=False)
    
    # ======================================================================
    # 2. GENERAR TAREAS (COMBINACIONES)
    # ======================================================================
    
    tasks = []  # Lista de tareas a ejecutar
    idx = 1     # Contador de ID de conversación
    
    # Triple loop: cliente × vendedor × repeticiones
    for _, c in c_df.iterrows():  # Para cada cliente
        cliente_dict = c.to_dict()  # Convertir fila a diccionario
        
        for _, v in v_df.iterrows():  # Para cada vendedor
            vendedor_dict = v.to_dict()  # Convertir fila a diccionario
            
            # Repetir la simulación varias veces para diversidad
            for _ in range(REPETICIONES):
                # Añadir tarea: (cliente, vendedor, id_único)
                tasks.append((cliente_dict, vendedor_dict, idx))
                idx += 1

    # ======================================================================
    # 3. EJECUTAR SIMULACIONES EN PARALELO
    # ======================================================================
    
    # Log informativo
    print(f"Iniciando {len(tasks)} simulaciones cruzadas ({len(c_df)} Clientes vs {len(v_df)} Vendedores x {REPETICIONES} repeticiones)...")
    
    # ThreadPoolExecutor: ejecuta múltiples tareas en paralelo
    # max_workers: número de threads simultáneos
    # executor.map(): aplica función a cada tarea manteniendo orden
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Ejecutar run_simulation para cada tarea
        # Lambda desempaqueta tuple (cliente, vendedor, id) en argumentos
        executor.map(lambda p: run_simulation(*p), tasks)
    
    # ======================================================================
    # 4. FINALIZACIÓN
    # ======================================================================
    
    # El archivo OUTPUT_FILE ahora contiene todas las conversaciones
    # Próximo paso: análisis con analysis.ipynb
    print(f"Simulaciones completadas. Resultados en: {OUTPUT_FILE}")
