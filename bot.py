import os
import telebot
from dotenv import load_dotenv
import requests

# Cargar variables de entorno desde .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hola 👋 Soy GsX InfoBin BOT.\n Tu bot de confianza para consultar bins V1.\n Owner: @TYRANTGsX")

# Comando /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """ℹ️ *Consutar bin: ".bin xxxxxx"*:

Envía un BIN en el siguiente formato:

`.bin 457173`

Y recibirás información como:
- Banco emisor
- Tipo de tarjeta
- Marca
- Nivel
- País de emisión

📌 Solo acepta BINs de 6 a 8 dígitos numéricos.

GsX InfoBin BOT
"""
    bot.reply_to(message, help_text)

# Función para obtener la información del BIN
def get_bin_info(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            return f"""💳 *Información del BIN: {bin_number}*
*Banco:* {data.get('bank', {}).get('name', 'Desconocido')}
*Tipo:* {data.get('type', 'Desconocido')}
*Marca:* {data.get('scheme', 'Desconocido').upper()}
*Nivel:* {data.get('brand', 'Desconocido')}
*País:* {data.get('country', {}).get('name', 'Desconocido')} {data.get('country', {}).get('emoji', '')}

GsX InfoBin BOT
"""
        else:
            return "❌ BIN no válido o no encontrado.\n\nGsX InfoBin BOT"
    except Exception as e:
        return f"⚠️ Error al buscar el BIN: {str(e)}\n\nGsX InfoBin BOT"

# Mensajes que no son comandos
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if text.lower().startswith(".bin "):
        bin_input = text[5:].strip()
        if bin_input.isdigit() and 6 <= len(bin_input) <= 8:
            info = get_bin_info(bin_input)
            bot.reply_to(message, info)
        else:
            bot.reply_to(message, "❌ Hey imbecil el BIN debe tener al menos 6 dígitos numéricos.")
    else:
        bot.reply_to(message, "ℹ️ Para consultar un BIN, escribe: .bin 457173")

# Iniciar el bot
print("✅ GsX InfoBin BOT está activo...")
bot.infinity_polling()
