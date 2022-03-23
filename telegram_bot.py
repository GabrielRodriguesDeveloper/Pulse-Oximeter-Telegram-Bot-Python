import logging
import values

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help_message():
    return """
1 - Coloque o seu dedo no sensor
2 - Aguarde 25 segundos e não retire o dedo do sensor enquanto este tempo não acabar
    """


def commands():
    return """
Comandos disponíveis:
/start - Mostra os comandos disponíveis
/iniciar - Inicia o sistema de alerta
/medir - Mostra os valores de batimentos cardíacos e oxigenação sanguínea
    """


def measure_messages(heart_rate, spo2):
    return f"""
Seu nível de oxigenação sanguínea está em: {spo2}%
Seu nível de batimentos cardíacos está em: {heart_rate}bpm
    """


def alert_messages(id = 0):
    if id == 1:
        return "Seu nível de oxigenação está muito baixo!"
    else:
        return "Seu nível de batimentos cardíacos está fora do normal!"


def measure(update: Update, context: CallbackContext) -> None:
    heart_rate_values, spo2_values = values.pickValues()
    max_heart_rate_value, max_spo2_value = values.getMaxValues(heart_rate_values, spo2_values)

    update.message.reply_text(measure_messages(max_heart_rate_value, max_spo2_value))


def init(update: Update, context: CallbackContext) -> None:
    help_message()
    heart_rate_values, spo2_values = values.pickValues()
    max_heart_rate_value, max_spo2_value = values.getMaxValues(heart_rate_values, spo2_values)

    if values.validHeartRateValue(max_heart_rate_value):
        update.message.reply_text(alert_messages())
    if values.validSpo2Value(max_spo2_value):
        update.message.reply_text(alert_messages(1))


def command_unavailable(update: Update, context: CallbackContext) -> None:
    string = "Ops! Tente usar os comandos disponíveis\n" + commands()
    update.message.reply_text(string)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(commands())


def manageBot() -> None:
    updater = Updater("2070614783:AAG6zkaI4tJmDwBtaEtXASMHWR0oJoPrfCc")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("iniciar", init))
    dispatcher.add_handler(CommandHandler("medir", measure))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, command_unavailable))

    updater.start_polling()

    updater.idle()
