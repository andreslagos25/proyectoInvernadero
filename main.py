import network, time, urequests
from machine import Pin, ADC, I2C
from utelegram import ubot
from bmp280 import BMP280
import ujson

tokenTelegram = "5988215449:AAEPT_NBFpjtJPo6ZC90TgMUiPJ8wQZM1N0"
urlThinkSpeak = "https://api.thingspeak.com/update?api_key=DPGMUYOQOEZKVA73"
sensorHumedad = ADC(Pin(35))
sensorHumedad.atten(ADC.ATTN_11DB)
bus = I2C(0, sda =Pin(21), scl=Pin(22))
bmp = BMP280(bus)
bot = ubot(tokenTelegram)

# Abrir archivo JSON y lee su contenido
with open('datos_red.json', 'r') as file:
    json_data = file.read()
#Decodifica el JSON en un objeto python
data = ujson.loads(json_data)
# Acceder a los valores
ssid = data['ssid']
password = data['password']
def conectaWifi (red, password):
    global miRed
    miRed = network.WLAN(network.STA_IF)
    try:
        if not miRed.isconnected():
            miRed.active(True)
            miRed.connect(red, password)
            timeout = time.time()
            while not miRed.isconnected(): 
                if(time.ticks_diff (time.time (), timeout) > 10):
                    raise Exception("No se pudo conectar a la red Wifi")
            return True
    except Exception as e:
        print("Error: ", str(e))
        return False
def porcentaje_humedad():
    lectura = sensorHumedad.read()
    #voltaje = (lectura / 4095) * 3.3
    porcentajeHumedad = (1 - (lectura/4095))*100
    return porcentajeHumedad

if conectaWifi(ssid, password):
    
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    temp = bmp.temperature
    porc = porcentaje_humedad()
    pres = bmp.pressure/100
    
    def start_handler(message):
        # Mensaje de bienvenida y opciones del menú
        menu_text = "¡Bienvenido! Por favor, elige una opción:\n" \
                    "/temperatura - Mostrar Temperatura 1\n" \
                    "/presion - Mostar Presion\n" \
                    "/humedad - Mostar Humedad"
        bot.send(message['message']['chat']['id'], menu_text)
    #handler para el comando /temperatura
    def opcion1_handler(message):
        # Acción correspondiente a la temperatura
        chat_id = message['message']['chat']['id']
        texto = 'Temperatura: ' + str(temp) + 'C°'
        bot.send(chat_id, texto)
        if temp < 10:
            bot.send(chat_id, "El ambiente está muy frio, revisar invernadero")

    # Handler para el comando /presion
    def opcion2_handler(message):
        #Accion correspondiente a la presion
        chat_id = message['message']['chat']['id']
        texto = 'Presion: ' + str(pres) + 'hPa'
        bot.send(chat_id, texto)

    # Handler para el comando /humedad
    def opcion3_handler(message):
        # Acción correspondiente a humedad
        chat_id = message['message']['chat']['id']
        texto = ' % Humedad: ' + str(porc) + '%'
        bot.send(chat_id, texto)
        if porcentaje_humedad() < 30:
            bot.send(chat_id, "El suelo esta muy seco, necesita riego")
        
    bot.register('/inicio', start_handler)
    bot.register('/temperatura', opcion1_handler)
    bot.register('/presion', opcion2_handler)
    bot.register('/humedad', opcion3_handler)
    while True:
        bot.read_once()
        request = urequests.get(urlThinkSpeak + "&field1="+ str(temp)+"&field2=" + str(pres) + "&field3="+str(porc))
        print(request.text)
        print(request.status_code)
        request.close()
        #if porc < 30:
        #    mensaje_humedad = "El suelo esta muy seco, necesita riego"
        #    bot.send(chat_id, mensaje_humedad)
        #if temp < 10:
        #    mensaje_temp = "El ambiente esta muy frio, revisar el invernadero"
        #    bot.send(chat_id, mensaje_temp)
        time.sleep(3)
else:
    print ("Imposible conectar")
    miRed.active (False)
    while True:
        porc = porcentaje_humedad()
        pres = str(bmp.pressure/100)
        temp = bmp.temperature
        print("Porcentaje de humedad: ", porc, '%')
        print("Temperatura: ", temp, " C°")
        print("Presion: ", pres, " hPa")
        if porc < 30:
            print("El suelo esta muy seco, necesita riego")
        if temp < 10:
            print("El ambiente esta muy frio, revisar el invernadero")
        time.sleep(3)

