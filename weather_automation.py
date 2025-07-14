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

{'request': {'type': 'City', 'query': 'Madrid, Spain', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'Madrid', 'country': 'Spain', 'region': 'Madrid', 'lat': '40.400', 'lon': '-3.683', 'timezone_id': 'Europe/Madrid', 'localtime': '2025-07-12 13:27', 'localtime_epoch': 1752326820, 'utc_offset': '2.0'}, 'current': {'observation_time': '11:27 AM', 'temperature': 24, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'], 'weather_descriptions': ['Sunny'], 'astro': {'sunrise': '06:55 AM', 'sunset': '09:46 PM', 'moonrise': '11:14 PM', 'moonset': '08:13 AM', 'moon_phase': 'Waning Gibbous', 'moon_illumination': 98}, 'air_quality': {'co': '212.75', 'no2': '6.105', 'o3': '81', 'so2': '1.665', 'pm2_5': '8.325', 'pm10': '14.985', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 15, 'wind_degree': 222, 'wind_dir': 'SW', 'pressure': 1013, 'precip': 0, 'humidity': 47, 'cloudcover': 25, 'feelslike': 24, 'uv_index': 8, 'visibility': 10, 'is_day': 'yes'}}

# TAREA 4: Función para formatear el reporte
# - Crear un string bonito con toda la información
# - Incluir fecha, temperatura, condiciones
# - Usar emojis para hacerlo más visual

# TAREA 5: Función principal
# - Coordinar todas las funciones
# - Mostrar progreso al usuario
# - Manejar errores generales

"""
#======================FUNCTIONS===================================
#We will use the Weather Description, the sunrise and sunset, windspeed, humidity
def obtainWeather(city, api_key):
    URL = f"https://api.weatherstack.com/current?access_key={api_key}"
    querystring = {"query": city}
    response = requests.get(URL, params=querystring)
    data = response.json()
    #print(data)
    lat = float(data["location"]["lat"])
    lon = float(data["location"]["lon"])

    #Accessing data
    weatherInfo = data["current"]["weather_descriptions"][0]
    weatherIcon = data["current"]["weather_icons"]
    sunrise = data["current"]["astro"]["sunrise"]
    sunset = data["current"]["astro"]["sunset"]
    windSpeed = data["current"]["wind_speed"] #km/h 
    
    #Finding temperatures from other API
    temps = findTemperatures(lat, lon)
    finalEmail = temps + f"It will be {weatherInfo} mainly, the sunrise is at {sunrise}, and the sunset will be at {sunset}. Today's windspeed is {windSpeed} km/h!"
    return [finalEmail, weatherIcon, weatherInfo] #Return the email and the weather icon to use in the email

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

    date = str(datetime.now()).split(" ")[0]
    email = "Today is " + date + " and the highest temperature will be " + str(HighestTemp) + ", the lowest will be " + str(lowestTemp) + ", and the daily average will be " + str(averageTemp) + "! "
    return email

#====================MAIN===============================

#weather_Madrid = obtainWeather("Madrid", APIKEY)
#weather_Atlanta = obtainWeather("Atlanta", APIKEY)
#print(weather_Atlanta)
#print(weather_Madrid)

#====================================================
#                   EMAIL SENDER
import smtplib, ssl                        # Para enviar emails
from email.mime.text import MIMEText    # Para crear el contenido del email
from email.mime.multipart import MIMEMultipart  # Para emails con múltiples partes
from email.mime.base import MIMEBase    # Para adjuntos (opcional)
from email import encoders              # Para codificar adjuntos
from email.message import EmailMessage
def messageHeader(info):
    pass

def mensaje_clima_html(datos_clima): #UNA LISTA CON EL TEXTO EN POS 0 Y LA IMG EN POS 1
    """
    Crear un HTML bonito con los datos del clima
    Usar CSS inline para estilos
    """
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🌤️ Pronóstico del Tiempo</h2>
            <!-- Aquí tu contenido HTML -->
        </body>
    </html>
    """
    return html
def enviarEmail(appPassword, smtp_server, port, sender_email, receiver_email, APIKEY):
    appPassword = "fsub yvnp zwuc fkhx"
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = "jaimejr.alonso67@gmail.com"
    receiver_email = "jaimejr.alonso@gmail.com"
    info = obtainWeather("Madrid", APIKEY) # [2] is header info for the email subject
    msg = EmailMessage()
    msg["Subject"] = messageHeader(info[2])
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(mensaje_clima_html)

    context = ssl.create_default_context() #To encrypt
    html_message = mensaje_clima_html()
    msg.add_alternative(html_message, subtype="html", charset="utf-8") #utf 8 to avoid any problems with special characters


    print(html_message)

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, appPassword)
        server.send_message(msg)
        print("Email was sent successfully!")
    #FUNCIONA!!!!!!!!!!!!!!!


# 4. Finalmente formatea todo bonito TODO
# 5. Prueba cada función por separado antes de juntarlas TODO

weather_Madrid = obtainWeather("Madrid", APIKEY)
print(weather_Madrid)