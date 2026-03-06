# Sales Conversation Strategy Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)](#)

> **Simulador avanzado de conversaciones de ventas que utiliza IA (Google Gemini) para generar y analizar estrategias de venta en tiempo real.**

Genera **10.000 conversaciones realistas** entre clientes y vendedores, extrae **15+ métricas cuantitativas** por conversación y proporciona análisis detallado para optimizar tácticas de venta.

---

## Características Principales

### Generación Inteligente de Datos
- Conversaciones realistas generadas con Google Gemini
- **50 perfiles de clientes únicos** con personalidades y preocupaciones distintas
- **20 estilos de vendedores diferentes** con estrategias variadas
- **Variabilidad controlada** mediante 10 repeticiones por combinación

### Extracción de Métricas Avanzada
Obtén 15+ indicadores cuantitativos por conversación:

```
Cliente Metrics:
├── Sentimiento promedio (-1.0 a 1.0)
├── Tasa de objeción (%)
├── Preguntas relevantes (%)
├── Palabras dudosas (%)
└── Frecuencia de preocupación principal (%)

Vendedor Metrics:
├── Tasa de preguntas abiertas (%)
├── Interrupciones (%)
└── Polaridad sentimiento (-1.0 a 1.0)

Resultado:
└── ÉXITO / FALLO
```

### Procesamiento de Alto Rendimiento
- **Paralelización inteligente** con 5 workers simultáneos (Se puede variar para mayor velocidad de simulación)
- **Thread-safe operations** para evitar corrupción de datos

### Análisis Completo
- Comparación de estrategias
- Rendimiento por vendedor y cliente
- Análisis de correlaciones

---

## Requisitos Previos

- **Python:** 3.8 o superior
- **API Key:** Google Generative AI (Gemini) - [Obtener gratis aquí](https://aistudio.google.com/app/apikeys)
- **Tiempo:** 90 - 120 minutos (Se hizo con 120 hilos)
- **Presupuesto:** 50€ en llamadas a la API con el modelo Gemini 2 Flash
- **Dependencias:** Ver `requirements.txt`

---

## Instalación Rápida

### 1️ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sales-conversation-strategy-analysis.git
cd sales-conversation-strategy-analysis
```

### 2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3 Configurar API Key

**Opción A: Variables de entorno (recomendado para producción)**

```bash
# Clave API de Google Generative AI (Gemini)
API_KEY = "YOUR_API_KEY_HERE"  # Reemplaza con tu clave real 
```
Modificar la línea 32 del archivo **simulator.py**

### 4 Ejecutar simulaciones

```bash
python main.py
```

Las simulaciones comenzarán a ejecutarse y verás el progreso en consola.

---

## Estructura del Proyecto

```
sales-conversation-strategy-analysis/
│
├── main.py                          # Punto de entrada
├── simulator.py                     # Motor de simulación
│
├── notebooks/
│   └── analysis.ipynb              # Análisis Jupyter
│
├── data/
│   ├── ClientesDataset.csv         # Perfiles de clientes (50)
│   ├── Vendedores Dataset.csv      # Perfiles de vendedores (20)
│   └── results/
│       └── simulated_conversations_data.csv  # Salida (10,000 filas)
│
│
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
```

---

## Cómo Usar

### Ejecutar Simulación Completa

```bash
python main.py
```

**Qué sucede:**
1. Carga 50 perfiles de clientes
2. Carga 20 perfiles de vendedores
3. Genera 10,000 combinaciones (50 × 20 × 10)
4. Ejecuta conversaciones en paralelo (5 simultáneas)
5. Extrae métricas con Gemini
6. Guarda resultados en `data/results/simulated_conversations_data.csv`

**Tiempo estimado:** 30-75 minutos (depende de velocidad de API y conexión, además el tiempo de ejecución es inversamente proporcional al número de hilos usados **MAX_WORKERS**)

---

### Analizar Resultados

Una vez completadas las simulaciones:

```bash
# Abrir Jupyter
jupyter notebook

# Navegar a: notebooks/analysis.ipynb
```

El notebook incluye:
- ✅ Exploración general de datos (EDA)
- ✅ Comparación de estrategias
- ✅ Análisis por vendedor y cliente
- ✅ Análisis de correlaciones

---

## Formato de Salida

El archivo CSV generado (`data/results/simulated_conversations_data.csv`) contiene:

| Columna | Tipo | Rango | Descripción |
|---------|------|-------|-------------|
| `id_conversacion` | int | 1-10.000 | Identificador único |
| `vendedor_nombre` | str | - | Nombre del vendedor |
| `cliente_nombre` | str | - | Nombre del cliente |
| `sentimiento_promedio_cliente` | float | -1.0 a 1.0 | Satisfacción del cliente |
| `tasa_objecion_cliente` | int | 0-100 | % de objeciones |
| `tasa_preguntas_relevantes_cliente` | int | 0-100 | % de preguntas inteligentes |
| `tasa_palabras_dudosas_cliente` | int | 0-100 | % de palabras de duda |
| `frecuencia_preocupacion_principal_cliente` | int | 0-100 | % de mención de preocupación |
| `tasa_preguntas_abiertas_vendedor` | int | 0-100 | % de preguntas abiertas |
| `tasa_interrupciones_vendedor` | int | 0-100 | % de interrupciones |
| `polaridad_sentimiento_vendedor` | float | -1.0 a 1.0 | Sentimiento positivo vendedor |
| `resultado_conversacion` | str | ÉXITO/FALLO | Resultado final |

### Ejemplo de Datos:

```csv
id_conversacion,vendedor_nombre,cliente_nombre,sentimiento_promedio_cliente,...,resultado_conversacion
1,Juan Pérez,María García,0.75,25,80,10,90,85,15,0.80,...,ÉXITO
2,Juan Pérez,Carlos López,-0.20,85,40,60,20,30,70,-0.15,...,FALLO
3,Ana García,María García,0.45,35,65,25,75,70,25,0.55,...,ÉXITO
```

---

## Configuración Avanzada

Edita `simulator.py` para personalizar la simulación:

```python
# PARÁMETROS DE SIMULACIÓN (línea 56-74)

MODEL_NAME = "gemini-2.0-flash"      # Modelo a usar
MAX_WORKERS = 5                       # Threads paralelos (↑ para más velocidad)
MAX_TURNS = 14                        # Profundidad conversación
REPETICIONES = 10                     # Reps por pair cliente-vendedor
TEMPERATURA_ALTA = 1.0                # Variabilidad (0=determinístico, 1=creativo)
```

### Ejemplos de Ajustes:

**Para máquina potente (más rápido):**
```python
MAX_WORKERS = 10  # Aumentar workers
REPETICIONES = 20  # Más datos
```

**Para máquina débil (más lento pero más confiable):**
```python
MAX_WORKERS = 2   # Menos threads
REPETICIONES = 5  # Menos datos
```

**Para conversaciones más profundas:**
```python
MAX_TURNS = 20    # 10 turnos por participante
```

---

## Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2024 Néstor Flores

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---


<div align="center">

**Hecho por Néstor Flores**

[⬆ Volver al inicio](#-sales-conversation-strategy-analyzer)

</div>
