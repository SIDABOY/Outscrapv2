#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import pdfkit
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import tabula
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os




try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version . To view the "
        f" version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import Updater


config = pdfkit.configuration()






# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.





async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    response = requests.get("https://outlettecnologico.cl/listaPrecios.pdf")
    file = open("metadata.pdf", "wb")
    file.write(response.content)
    file.close()

    tabula.convert_into('metadata.pdf', "nuevo.csv", output_format="csv", pages='all')
    nuevo=pd.read_csv('nuevo.csv',header=[0],encoding ="ISO-8859-1") 

    tabula.convert_into('listaPrecios.pdf', "antiguo.csv", output_format="csv", pages='all')
    antiguo=pd.read_csv('antiguo.csv',header=[0],encoding ="ISO-8859-1")

    result = nuevo[~(nuevo.SKU.isin(antiguo.SKU))]
    result2 = antiguo[~(antiguo.SKU.isin(nuevo.SKU))]

    print(len(result))
    result.to_html("test.html")
    result2.to_html("test2.html")

    #PDF
    pdfkit.from_file('test.html', 'Lista.pdf')
    pdfkit.from_file('test2.html', 'Vendido.pdf')

    document = open('Lista.pdf', 'rb')

    if len(result) == 0:
        os.remove("metadata.pdf")
    else:
        os.remove("listaPrecios.pdf")
        os.rename("metadata.pdf", "listaPrecios.pdf")    
        os.remove("nuevo.csv")
        os.remove("antiguo.csv")     
        await context.bot.send_document('-1001900358349', document)
        await context.bot.send_message(chat_id='-1001900358349', text='Enviado')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6699364920:AAFvlrP7_g1xGEKMzdPpDnL_IOmn4jRyw98").build()
    job_queue = application.job_queue
    job_minute = job_queue.run_repeating(callback_minute, interval=60, first=10)


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()