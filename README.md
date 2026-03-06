# 🎯 Sales Conversation Strategy Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)](#)

> **Simulador avanzado de conversaciones de ventas que utiliza IA (Google Gemini) para generar y analizar estrategias de venta en tiempo real.**

Genera **9,500+ conversaciones realistas** entre clientes y vendedores, extrae **15+ métricas cuantitativas** por conversación y proporciona análisis detallado para optimizar tácticas de venta.

---

## 📊 Características Principales

### 🤖 Generación Inteligente de Datos
- Conversaciones realistas generadas con Google Gemini
- **50 perfiles de clientes únicos** con personalidades y preocupaciones distintas
- **19 estilos de vendedores diferentes** con estrategias variadas
- **Variabilidad controlada** mediante 10 repeticiones por combinación

### 📈 Extracción de Métricas Avanzada
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
└── ÉXITO / FALLO / NEUTRO
```

### ⚡ Procesamiento de Alto Rendimiento
- **Paralelización inteligente** con 5 workers simultáneos
- **Thread-safe operations** para evitar corrupción de datos
- Manejo robusto de errores y retry automático

### 📊 Análisis Completo
- Comparación de estrategias (Estática vs Dinámica)
- Rendimiento por vendedor y cliente
- Análisis de correlaciones
- Visualizaciones profesionales con Matplotlib y Seaborn

---

## 📋 Requisitos Previos

- **Python:** 3.8 o superior
- **API Key:** Google Generative AI (Gemini) - [Obtener gratis aquí](https://aistudio.google.com/app/apikeys)
- **Tiempo:** 30-75 minutos para ejecución completa (9,500 conversaciones)
- **Dependencias:** Ver `requirements.txt`

---

## 🚀 Instalación Rápida

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sales-conversation-strategy-analysis.git
cd sales-conversation-strategy-analysis
```

### 2️⃣ Crear ambiente virtual (recomendado)

```bash
# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar API Key

**Opción A: Variables de entorno (recomendado para producción)**

```bash
# Crear archivo .env en la raíz del proyecto
echo "GOOGLE_API_KEY=tu-api-key-aqui" > .env
```

**Opción B: Modificar directamente**

```bash
# Editar .env con tu editor favorito
nano .env
# O abrir directamente en VS Code
code .env
```

### 5️⃣ Ejecutar simulaciones

```bash
python main.py
```

✨ Las simulaciones comenzarán a ejecutarse y verás el progreso en consola.

---

## 📊 Estructura del Proyecto

```
sales-conversation-strategy-analysis/
│
├── main.py                          # 📌 Punto de entrada
├── simulator.py                     # 🔧 Motor de simulación
│
├── notebooks/
│   └── analysis.ipynb              # 📊 Análisis Jupyter
│
├── data/
│   ├── ClientesDataset.csv         # 👥 Perfiles de clientes (50)
│   ├── Vendedores Dataset.csv      # 💼 Perfiles de vendedores (19)
│   └── results/
│       └── simulated_conversations_data.csv  # 📈 Salida (9,500 filas)
│
├── tests/                          # 🧪 Suite de tests
│   ├── __init__.py
│   ├── test_simulator.py
│   └── test_data_loading.py
│
├── logs/                           # 📝 Archivos de log
│
├── requirements.txt                # 📦 Dependencias
├── .env.example                    # 🔐 Template de variables
├── .gitignore                      # 🚫 Archivos ignorados
├── README.md                       # 📖 Este archivo
└── LICENSE                         # ⚖️ Licencia MIT
```

---

## 🎓 Cómo Usar

### Ejecutar Simulación Completa

```bash
python main.py
```

**Qué sucede:**
1. Carga 50 perfiles de clientes
2. Carga 19 perfiles de vendedores
3. Genera 9,500 combinaciones (50 × 19 × 10)
4. Ejecuta conversaciones en paralelo (5 simultáneas)
5. Extrae métricas con Gemini
6. Guarda resultados en `data/results/simulated_conversations_data.csv`

**Tiempo estimado:** 30-75 minutos (depende de velocidad de API y conexión)

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
- ✅ Visualizaciones profesionales
- ✅ Conclusiones y recomendaciones

---

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ -v --cov=simulator --cov-report=html

# Test específico
pytest tests/test_simulator.py::TestCallLlm -v
```

---

## 📊 Formato de Salida

El archivo CSV generado (`data/results/simulated_conversations_data.csv`) contiene:

| Columna | Tipo | Rango | Descripción |
|---------|------|-------|-------------|
| `id_conversacion` | int | 1-9500 | Identificador único |
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
| `resultado_conversacion` | str | ÉXITO/FALLO/NEUTRO | Resultado final |

### Ejemplo de Datos:

```csv
id_conversacion,vendedor_nombre,cliente_nombre,sentimiento_promedio_cliente,...,resultado_conversacion
1,Juan Pérez,María García,0.75,25,80,10,90,85,15,0.80,...,ÉXITO
2,Juan Pérez,Carlos López,-0.20,85,40,60,20,30,70,-0.15,...,FALLO
3,Ana García,María García,0.45,35,65,25,75,70,25,0.55,...,NEUTRO
```

---

## 🔧 Configuración Avanzada

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

## 📈 Análisis de Resultados

Después de ejecutar, puedes:

### 1. Comparar Estrategias
```python
# En el notebook
estatico = df[df['estrategia'] == 'Estático']
dinamico = df[df['estrategia'] == 'Dinámico']

tasa_exito_estatico = (estatico['resultado_conversacion'] == 'ÉXITO').sum() / len(estatico) * 100
tasa_exito_dinamico = (dinamico['resultado_conversacion'] == 'ÉXITO').sum() / len(dinamico) * 100

print(f"Estrategia Estática: {tasa_exito_estatico:.1f}%")
print(f"Estrategia Dinámica: {tasa_exito_dinamico:.1f}%")
```

### 2. Identificar Mejores Vendedores
```python
vendedor_stats = df.groupby('vendedor_nombre').agg({
    'resultado_conversacion': lambda x: (x == 'ÉXITO').sum() / len(x) * 100,
    'sentimiento_promedio_cliente': 'mean'
}).sort_values('resultado_conversacion', ascending=False)

print(vendedor_stats.head(5))
```

### 3. Analizar Correlaciones
```python
# Qué factores impulsan el éxito
correlacion = df.corr()['exito_binario'].sort_values(ascending=False)
print(correlacion)
```

---

## 🧪 Testing

El proyecto incluye una suite de tests para garantizar confiabilidad:

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ver cobertura
pytest tests/ --cov=simulator --cov-report=term-missing

# Generar reporte HTML
pytest tests/ --cov=simulator --cov-report=html
# Abrir: htmlcov/index.html
```

**Tests incluidos:**
- ✅ Carga correcta de CSVs
- ✅ Manejo de errores de API
- ✅ Parsing de JSON
- ✅ Thread-safety de escritura

---

## 🔐 Seguridad

### Proteger tu API Key

```bash
# 1. Nunca commits tu .env
✅ .gitignore contiene .env

# 2. Para GitHub, usar Secrets
# Settings → Secrets and variables → Actions
# Agregar: GOOGLE_API_KEY

# 3. Variables de entorno en producción
export GOOGLE_API_KEY="tu-clave"
python main.py
```

### Validación de Datos

El código incluye validación automática de:
- Formatos de CSV
- Respuestas API
- Parseo JSON
- Thread-safety

---

## 📊 Escalabilidad

### Proyecto Actual
- **Clientes:** 50
- **Vendedores:** 19
- **Conversaciones:** 9,500
- **Tiempo:** 30-75 minutos

### Escalable a:

```python
# Fácil agregar más perfiles
# Ejemplo: 100 clientes × 30 vendedores × 10 reps = 30,000 conversaciones

# Solo necesitas:
# 1. Agregar filas a ClientesDataset.csv
# 2. Agregar filas a Vendedores Dataset.csv
# 3. Aumentar MAX_WORKERS según hardware
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! 

### Para contribuir:

1. **Fork** el proyecto
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

### Ideas para contribuir:
- 🔧 Nuevos modelos de IA
- 📊 Análisis estadístico avanzado
- 📈 Dashboard interactivo (Streamlit/Dash)
- 🧪 Más tests
- 📚 Documentación mejorada

---

## 📝 Licencia

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

## 🐛 Problemas Comunes

### Error: "GOOGLE_API_KEY not found"
```bash
# Solución: Asegúrate de que .env existe con tu API key
ls -la .env
cat .env  # Debe contener: GOOGLE_API_KEY=tu-clave-aqui
```

### Error: "Rate limit exceeded"
```bash
# Solución: Reduce MAX_WORKERS o espera unos minutos
MAX_WORKERS = 2  # Reducir
```

### Error: "File not found: data/ClientesDataset.csv"
```bash
# Solución: Asegúrate de estar en la carpeta correcta
pwd
ls data/
```

### Conversación se queda atascada
```bash
# Solución: Es normal, el API a veces tarda
# Aumenta timeout o revisa conexión a internet
```

---

## 📚 Recursos Adicionales

- 📖 [Documentación de Google Gemini API](https://ai.google.dev/docs)
- 🐍 [Documentación de Python](https://docs.python.org/3/)
- 📊 [Pandas Documentation](https://pandas.pydata.org/docs/)
- 🎨 [Matplotlib & Seaborn Docs](https://matplotlib.org/)
- 🧪 [Pytest Documentation](https://docs.pytest.org/)

---

## 🎯 Casos de Uso

Este proyecto es ideal para:

### 📊 Investigación
- Análisis de estrategias de venta
- Estudio de comportamiento de clientes
- Evaluación de técnicas de comunicación

### 🎓 Académico
- Tesis sobre IA y ventas
- Proyectos de maestría
- Investigación de mercado

### 💼 Empresarial
- Entrenamiento de vendedores
- Identificación de mejores prácticas
- Optimización de procesos de venta
- Benchmarking de estrategias

### 🤖 ML/IA
- Dataset para entrenamiento
- Análisis de modelos LLM
- Investigación en NLP

---

## 📈 Roadmap Futuro

- [ ] Dashboard interactivo (Streamlit)
- [ ] Análisis estadístico avanzado (scipy)
- [ ] Predicción con ML (scikit-learn)
- [ ] Soporte para múltiples idiomas
- [ ] API REST (FastAPI)
- [ ] Base de datos (PostgreSQL)
- [ ] Visualización 3D de datos
- [ ] Exportación a PowerPoint
- [ ] Integración con CRM (Salesforce, HubSpot)

---

## 📞 Soporte & Contacto

- 📧 **Email:** tu-email@example.com
- 🐦 **Twitter:** [@tu-usuario](https://twitter.com/tu-usuario)
- 💼 **LinkedIn:** [tu-perfil](https://linkedin.com/in/tu-perfil)
- 🐙 **GitHub Issues:** [Report a bug](https://github.com/tu-usuario/sales-conversation-strategy-analysis/issues)

---

## 🙏 Agradecimientos

- **Google** - Por Google Generative AI (Gemini)
- **Comunidad Python** - Por herramientas increíbles
- **Pandas, NumPy, Matplotlib, Seaborn** - Por librerías indispensables
- **Todos los contribuidores** - ¡Gracias por mejorar este proyecto!

---

## 📊 Estadísticas del Proyecto

```
Lines of Code:      494 (simulator.py)
Functions:          6
Classes:            0
Test Coverage:      >80%
Documentation:      100%
Supported Python:   3.8+
Last Updated:       March 2024
Contributors:       Open for contributions!
```

---

## 🌟 Si te resultó útil

⭐ **Dale una estrella** si te ayudó  
🍴 **Fork el proyecto** para tus propias mejoras  
📢 **Comparte** con tu comunidad  

---

<div align="center">

**Hecho con ❤️ por Néstor Flores**

[⬆ Volver al inicio](#-sales-conversation-strategy-analyzer)

</div>
