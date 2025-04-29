from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

TOKEN = "AAF6upNwQhBrIxtMIjTUX8SslvouHcSCu9k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola 👋 Soy GsX InfoBin BOT.\nEnvíame un BIN con el formato: `.bin 457173`")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """ℹ️ *Cómo usar GsX InfoBin BOT*:

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
    await update.message.reply_text(help_text, parse_mode="Markdown")

def get_bin_info(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            return f"""💳 Información del BIN: {bin_number}
Banco: {data.get('bank', {}).get('name', 'Desconocido')}
Tipo: {data.get('type', 'Desconocido')}
Marca: {data.get('scheme', 'Desconocido').upper()}
Nivel: {data.get('brand', 'Desconocido')}
País: {data.get('country', {}).get('name', 'Desconocido')} {data.get('country', {}).get('emoji', '')}

GsX InfoBin BOT
"""
        else:
            return "❌ BIN no válido o no encontrado.\n\nGsX InfoBin BOT"
    except Exception as e:
        return f"⚠️ Error al buscar el BIN: {str(e)}\n\nGsX InfoBin BOT"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.lower().startswith(".bin "):
        bin_input = text[5:].strip()

        if bin_input.isdigit() and 6 <= len(bin_input) <= 8:
            info = get_bin_info(bin_input)
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("❌ El BIN debe tener entre 6 y 8 dígitos numéricos.")
    else:
        await update.message.reply_text("ℹ️ Para consultar un BIN, escribe: .bin 457173")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("GsX InfoBin BOT está activo...")
    app.run_polling()

if __name__ == "__main__":
    main()
