# handlers.py
import time
import datetime
from telegram.ext import CallbackContext
from telegram import Update
from openai import OpenAI

from .config import assistant_id, client_api_key
from .utils import get_message_count, update_message_count, save_qa


client = OpenAI(api_key=client_api_key)


async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="¡Hola y bienvenido/a a nuestro servicio de asistencia médica virtual! 🏥 Mi nombre es MediBot, y estoy aquí para ayudarte a navegar por tus inquietudes de salud. 🩺 Puedo ofrecerte información general sobre síntomas, enfermedades, primeros auxilios y consejos de bienestar. Recuerda, soy un asistente virtual diseñado para brindar apoyo informativo y no puedo reemplazar una consulta médica profesional. 🚫 Si tienes una emergencia médica, te insto a que te pongas en contacto con servicios de emergencia locales 🚑 o visites a un médico. ¿Cómo puedo asistirte hoy? 🤖"
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🆘 Comando /help - ¡Estoy aquí para ayudarte! 🆘\n\n¿Necesitas una mano? ¡Has llegado al lugar correcto! Aquí te dejo una lista de los comandos que puedes usar para navegar por nuestro chatbot de asistencia médica:\n\n/start 🚀: Inicia una nueva conversación conmigo. ¡Dame un saludo inicial y te guiaré en lo que necesites!",
    )


def get_answer(message_str) -> None:
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=message_str
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(run.status)
        if run.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.dict()["data"][0]["content"][0]["text"]["value"]
    return response


async def process_message(update: Update, context: CallbackContext) -> None:
    message_data = get_message_count()
    count = message_data["count"]
    date = message_data["date"]
    today = str(datetime.date.today())

    if date != today:
        count = 0
    if count >= 100:
        return

    answer = get_answer(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    update_message_count(count + 1)
    save_qa(
        update.effective_user.id,
        update.effective_user.username,
        update.message.text,
        answer,
    )
