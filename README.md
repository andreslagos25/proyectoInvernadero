# Proyecto Invernadero
#### Este proyecto usa una placa esp32 a la que se le instaló Micropython. La placa necesita dos sensores, uno que mida la humedad del suelo y otro que mida presión atmosferica y temperatura.

#### Para la humedad del suelo se usó un sensor FC-28 y para la temperatura y presión un BMP280. Para poder usar el sensor BMP280 se necesitó la ayuda de una librería.

#### Por otro lado, también envía mensajes via Telegram con el notificará al usuario cuando haya baja humedad o una baja temperatura. Se necesitó también la ayuda de una libería.

Librería sensor BMP280: https://github.com/dafvid/micropython-bmp280
Librería Telegram: https://github.com/jordiprats/micropython-utelegram
