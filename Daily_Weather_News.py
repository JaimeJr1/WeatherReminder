#====================IMPORTS==================================
import requests      # Para hacer peticiones HTTP a APIs
from datetime import datetime, timedelta  # Para fechas y horas   
import smtplib, ssl                     # Para enviar emails
from email.mime.text import MIMEText    # Para crear el contenido del email
from email.mime.multipart import MIMEMultipart  # Para emails con múltiples partes
from email.mime.base import MIMEBase    # Para adjuntos (opcional)
from email import encoders              # Para codificar adjuntos
from email.message import EmailMessage
import os

# ============================================================

#We will use two API's to get all the information we need, because if not the information would be incomplete
#I will also include an inspirational quote with the weather email
#We will use the Weather Description, the sunrise and sunset, windspeed, humidity

#======================HELPER METHODS==============================

def messageHeader(weatherCode):
    # FOR INFO: weather_code_dict = {"113": ["Sunny", "Clear"], "116": ["Partly Cloudy", "Partly Cloudy"], "119" : ["Cloudy", "Cloudy"], "122" : ["Overcast", "Overcast"], "143" : ["Mist", "Mist"], "176" : ["Patchy Rain", "Patchy Rain"], "179" : ["Patchy Snow", "Patchy Snow"], "182" : ["Patchy Sleet", "Patchy Sleet"], "185" : ["Patchy Freezi", "Patchy Freezi"], "200" : ["Thundery outbreaks possible", "Thundery outbreaks possible"], "227" : ["Blowing snow", "Blowing snow"], "230" : ["Blizzard", "Blizzard"], "248" : ["Fog", "Fog"], "260" : ["Freezing Fog", "Freezing Fog"], "263" : ["Light Drizzle", "Light Drizzle"], "266" : ["Light Drizzle", "Light Drizzle"], "281" : ["Freezing Drizzle", "Freezing Drizzle"], "284" : ["Heavy Drizzle", "Heavy Drizzle"], "293" : ["Light Rain", "Light Rain"], "296" : ["Light Rain", "Light Rain"], "299" : ["Moderate Rain", "Moderate Rain"], "302" : ["Moderate Rain", "Moderate Rain"], "305" : ["Heavy Rain", "Heavy Rain"], "308" : ["Heavy Rain", "Heavy Rain"], "311" : ["Light Freezing Rain", "Light Freezing Rain"]}
    if weatherCode in [113, 116, 119, 122, 143, 248, 260] :
        return ("No rain in sight!", "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDRodHhua3ZxMGVwMzY1Z3Q0eDI0d3F2cWMyaW5sYTg3d2ptNmF4NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wNipYAoZ3iaEE/giphy.gif")
    elif weatherCode in [176, 185, 263, 266, 281, 284, 293, 296, 299, 302, 305, 308, 311]:
        return ("Remember to bring your umbrella!", "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWJzaDBpazV3Mmd4eHBjY3k1aTRuOTI1M2ZvcWFrenp1NmNnOHRybiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4NL5RJnYihpihzAhlX/giphy.gif")
    else:
        return ("[WARNING] Watch out for weather conditions!", "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHFvNWxmdWl2enJucHd6eXN5bWpmc3V5NjhkanNuM2hubWFrNjM2MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/EeofceO0vyYKvqJKHH/giphy.gif")
    

def msg_html(info):
    #Creates a simple HTML for the email
    quote = inspirationalQuote()
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather</title>
    </head>
    <body style="text-align: center; font-family: Arial; padding: 20px;">
        <h1 style="font-size: 48px;">Daily Weather News!</h1>
        
        <img src="{info[1][1]}" alt="Weather" style="width: 300px; height: 300px;"> 

        <div style="font-size: 16px; margin: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 10px; max-width: 600px; margin: 20px auto;">
        <p style="line-height: 1.6; margin: 0;">{info[0]}</p>
        </div>
        
        <p style="font-size: 18px; font-style: italic; margin-top: 30px;">
            {quote}
        </p>
    </body>
    </html>
    """
    return html

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
    email = "Today is " + date + " and the highest temperature will be " + str(HighestTemp) + "°C, the lowest will be " + str(lowestTemp) + "°C, and the daily average will be " + str(averageTemp) + "°C! "
    return email

def inspirationalQuote():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url)
    data = response.json()
    quote = data[0]["q"]
    author = data[0]["a"]
    return (quote + "\n" + author)

#====================================================================================


#==============================WEATHER FINDER INFO===================================
#We will use the Weather Description, the sunrise and sunset, windspeed, humidity

def obtainWeather(city, api_key):
    URL = f"https://api.weatherstack.com/current?access_key={api_key}"
    querystring = {"query": city}
    response = requests.get(URL, params=querystring)
    data = response.json()
    lat = float(data["location"]["lat"])
    lon = float(data["location"]["lon"])

    #Accessing data
    weatherInfo = data["current"]["weather_descriptions"][0].strip()
    weatherCode = data["current"]["weather_code"]
    weatherGIF = messageHeader(weatherCode)
    sunrise = data["current"]["astro"]["sunrise"]
    sunset = data["current"]["astro"]["sunset"]
    windSpeed = data["current"]["wind_speed"] #km/h 
    
    #Finding temperatures from other API
    temps = findTemperatures(lat, lon)
    finalEmail = temps + f"The day will be {weatherInfo}, the sunrise is at {sunrise}, and the sunset will be at {sunset}. {city}'s windspeed is {windSpeed} km/h!"
    return [finalEmail, weatherGIF, weatherCode] #Return the email and the weather icon to use in the email

#================================================================


#=========================EMAIL SENDER===========================

def enviarEmail(city, appPassword, sender_email, receiver_emails, APIKEY):
    #For Gmails (These settings may vary for outlook and other email services):
    smtp_server = "smtp.gmail.com"
    port = 465

    info = obtainWeather(city, APIKEY) # [0] is info, [1] is GIF, [2] is weather code for the email subject
    
    for receiver_email in receiver_emails:
        msg = EmailMessage()
        msg["Subject"] = info[1][0] #Using weatherCode
        msg["From"] = sender_email
        msg["To"] = receiver_email

        context = ssl.create_default_context() #To encrypt
        html_message = msg_html(info)
        msg.add_alternative(html_message, subtype="html", charset="utf-8") #utf 8 to avoid any problems with special characters

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, appPassword)
            server.send_message(msg)
            print("Email was sent successfully!")

#======================================================


#======================MAIN============================

def main():
    cityName = os.environ.get("CITY_NAME", "Atlanta")
    appPassword = os.environ.get('APP_PASSWORD')
    senderEmail = os.environ.get('SENDER_EMAIL')
    receiverEmails = os.environ.get('RECEIVER_EMAIL')
    receiverEmails = json.loads(receiverEmails)
    apiKey = os.environ.get('WEATHER_API_KEY')
    enviarEmail(cityName, appPassword, senderEmail, receiverEmails, apiKey)

main()
