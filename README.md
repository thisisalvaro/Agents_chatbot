# 🌦️ Proyecto: Agentes Inteligentes para Información del Clima

## 📌 Descripción
Este proyecto utiliza **CrewAI** para coordinar múltiples agentes que obtienen y formatean información meteorológica desde **OpenWeatherMap API**. La interacción con el usuario se realiza a través de **Streamlit**, proporcionando un reporte del clima en tiempo real de manera clara y estructurada.

## 🚀 Tecnologías Utilizadas
- Python 3.10+
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Streamlit](https://streamlit.io/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Langchain OpenAI](https://python.langchain.com/docs/integrations/chat/openai)

## 📂 Estructura del Proyecto

```
📁 Model-Agents/
│── 📄 app.py # Script principal que ejecuta la aplicación en Streamlit
│── 📄 .env # Variables de entorno (API Keys)
│── 📄 requirements.txt # Dependencias del proyecto
│── 📄 README.md # Documentación del proyecto
```

## 🔧 Instalación y Configuración
### 1️⃣ Clonar el Repositorio

```
git clone https://github.com/tu_usuario/Model-Agents.git
cd Model-Agents
```

### 2️⃣ Crear un Entorno Virtual

```
python -m venv IAenv
source IAenv/bin/activate  # En macOS/Linux
IAenv\Scripts\activate     # En Windows
```
### 3️⃣ Instalar Dependencias

``` pip install -r requirements.txt 
```

### 4️⃣ Configurar Variables de Entorno
**Crea un archivo .env en el directorio principal y agrega:**

```
OPENAI_API_KEY=tu_openai_api_key
WEATHER_API_KEY=tu_openweathermap_api_key 
```
### 5️⃣ Ejecutar la Aplicación
```
streamlit run app.py
```
## 🎯 Funcionamiento
- Usuario ingresa una ciudad en la interfaz de Streamlit.
- Agente Investigador consulta el clima en OpenWeatherMap.
- Agente Formateador da formato a la información.
- Interfaz muestra el reporte final.

