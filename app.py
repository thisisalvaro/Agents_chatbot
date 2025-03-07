import os
import requests
import streamlit as st
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API Key
model = ChatOpenAI(
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    streaming=True,
    temperature=0.7
)

weather_api_key = os.getenv("WEATHER_API_KEY")

# Función para obtener el clima
@tool("get_weather")
def get_weather(city: str) -> dict:
    """
    Obtiene el clima actual de una ciudad desde OpenWeatherMap.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=es"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto lanza un error si el status_code no es 200
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en la solicitud: {str(e)}"}
    except Exception as e:
        return {"error": f"Ocurrió un error inesperado: {str(e)}"}

# Función para formatear el reporte del clima
@tool("format_weather_report")
def format_weather_report(weather_data: dict) -> str:
    """
    Formatea los datos del clima en un formato amigable para el usuario.
    """
    if "error" in weather_data:
        return f"Error: {weather_data['error']}"
    
    city = weather_data.get("name", "Desconocida")
    temperature = weather_data.get("main", {}).get("temp", "N/A")
    description = weather_data.get("weather", [{}])[0].get("description", "N/A")
    
    return f"🌤️ El clima en {city} es actualmente {description} con una temperatura de {temperature}°C."

# Crear la aplicación en Streamlit
st.title("🌦️ Información Climática")
st.markdown("Ingresa el **nombre de la ciudad** para obtener el clima actual.")

# Entrada de usuario
city = st.text_input("🏙️ Ciudad:", "")

if city:
    with st.spinner("⏳ Obteniendo datos del clima..."):

        # Definir agentes
        weather_researcher = Agent(
            role="🌎 Investigador del Clima",
            goal=f"Obtener el clima actual de la ciudad {city}",
            backstory="Recopilas datos del clima usando la API de OpenWeatherMap.",
            allow_delegation=False,
            llm=model,
            tools=[get_weather],
            verbose=True
        )

        formatter = Agent(
            role="📝 Formateador de Clima",
            goal="Convertir la información del clima en un formato bonito para el usuario.",
            backstory="Convierte los datos crudos en un formato legible para el usuario.",
            allow_delegation=False,
            llm=model,
            tools=[format_weather_report],
            verbose=True
        )

        # Definir tareas
        get_weather_task = Task(
            description=f"Obtén el clima de la ciudad {city}",
            expected_output="🌤️ Información meteorológica detallada.",
            agent=weather_researcher,
        )

        format_weather_task = Task(
            description=f"Convierte los datos del clima a un formato bonito para {city}",
            expected_output="✅ Reporte de clima bien formateado.",
            agent=formatter,
        )

        # Crear el equipo
        crew = Crew(
            agents=[weather_researcher, formatter],
            tasks=[get_weather_task, format_weather_task],
            verbose=True
        )

        # Ejecución de la tarea
        st.subheader("🚀 Progreso en tiempo real")

        # Ejecutar CrewAI con seguimiento en tiempo real
        weather_report = crew.kickoff(inputs={"city": city})  # Ejecuta las tareas

        # Mostrar el resultado final
        st.subheader("📝 Reporte del Clima")
        st.markdown(weather_report, unsafe_allow_html=True)
