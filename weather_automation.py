# PROYECTO: Automatizador de Pronóstico del Tiempo
# ================================================

# IMPORTS NECESARIOS
import requests      # Para hacer peticiones HTTP a APIs
import json         # Para manejar datos JSON
from datetime import datetime, timedelta  # Para fechas y horas
import os           # Para operaciones del sistema operativo (crear carpetas, archivos)
APIKEY = "30dbb2b2fdd187e8d9bccfd80c29145d"
# ============================================

#We will use two API's to get all the information we need, because if not the information would be incomplete
#I will also include an inspirational quote with the weather email
#We will use the Weather Description, the sunrise and sunset, windspeed, humidity

"""
# FUNCTIONS:
# ==========================



# TAREA 4: Función para formatear el reporte
# - Crear un string bonito con toda la información
# - Incluir fecha, temperatura, condiciones
# - Usar emojis para hacerlo más visual

# TAREA 5: Función principal
# - Coordinar todas las funciones
# - Mostrar progreso al usuario
# - Manejar errores generales

"""

#We will use the Weather Description, the sunrise and sunset, windspeed, humidity
def obtainWeather(city, api_key):
    URL = f"https://api.weatherstack.com/current?access_key={api_key}"
    querystring = {"query": city}
    response = requests.get(URL, params=querystring)
    lat = float(response["location"]["lat"])
    lon = float(response["location"]["lon"])

    #Accessing data
    weatherInfo = response["weather_descriptions"]
    weatherIcon = response["weather_icons"]
    sunrise = response["astro"]["sunrise"]
    sunset = response["astro"]["sunset"]
    windSpeed = response["wind_speed"]
    
    #Finding temperatures from other API
    temps = findTemperatures(lat, lon)

def findTemperatures(lat, lon):
    lowestTemp = 100
    HighestTemp = 0.0
    averageTemp = 0.0
    #24hrs in a day so until 24
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m")
    data = response.json()

    #This will give the lowest, highest, and average temperature of the day it is sent
    for i in range(24):
        temperature = data["hourly"]["temperature_2m"][i]
        if temperature > HighestTemp:
            HighestTemp = temperature
        elif temperature < lowestTemp:
            lowestTemp = temperature
        averageTemp += temperature
    averageTemp = averageTemp // 24
    #print(lowestTemp, HighestTemp, averageTemp)

    date = str(datetime.now()).split(" ")[0]
    email = "Today is " + date + " and the highest temperature will be " + str(HighestTemp) + ", the lowest will be " + str(lowestTemp) + ", and the daily average will be " + str(averageTemp) + "!"
    return email

weather_Madrid = obtainWeather("Madrid", APIKEY)
weather_Atlanta = obtainWeather("Atlanta", APIKEY)

# def guardar_reporte(contenido, nombre_archivo):
#     # Tu código aquí
#     pass

# def formatear_reporte(datos_clima):
#     # Tu código aquí
#     pass

# def main():
#     # Tu código aquí
#     pass

# if __name__ == "__main__":
#     main()


# TIPS:
# =====
# 1. Empieza haciendo una petición simple y imprime el resultado
# 2. Luego extrae solo los datos que necesitas
# 3. Después implementa el guardado en archivo
# 4. Finalmente formatea todo bonito
# 5. Prueba cada función por separado antes de juntarlas

#print("Empieza por obtener tu API key y hacer tu primera peticion!")
#print("Tip: Imprime el JSON completo primero para ver qué datos tienes disponibles")
