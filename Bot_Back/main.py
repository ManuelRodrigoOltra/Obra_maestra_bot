from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram.ext.dispatcher import run_async
import Bot_scraper.filmScraperScore as fc
from myDictionary import dictionaryPelis, dictionaryGente
import requests
import re

@run_async
def peli(update, context):

    titulo = ''
    for arg in context.args:
        titulo = titulo + arg + ' '

    titulo = titulo.strip()
    try:
        peli = fc.FilmScraperScore(titulo)
        evalue_score(peli, titulo, update, context)
    except:
        evalue_score([], titulo, update, context)

# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def evalue_score(pelicula, title, update, context):
    chat_id = update.message.chat_id

    #primero comprobamos las excepciones
    #   La pelicula es especial y está en mi diccionario
    #   El titulo es un nombre de persona y está en el diccionario
    #   La web no ha devuelto ninguna pelúcula por que algo ha ido mal con el titulo
    if title.lower() in dictionaryPelis:
        url = pelicula.picture
        update.message.reply_text(dictionaryPelis[title.lower()])
        context.bot.send_photo(chat_id=chat_id, photo=url)
    elif title.lower() in dictionaryGente:
        update.message.reply_text(dictionaryGente[title.lower()])
    elif not pelicula:
        evaluation = "Algo fue mal, con el titulo"
    else:
        #Si no hay ningúna excepción evaluamos la película
        #Obtenemos la puntuación y la imágen de la película
        score = float(pelicula.findScore[0].text)
        url = pelicula.picture


        if score >= 8 :
            evaluation = "Obra maestra ", + score
        else:
            evaluation = "Puta mierda ", + score


        if evaluation:
            try:
                url = pelicula.picture
                context.bot.send_photo(chat_id=chat_id, photo=url)
            except:
                pass
            update.message.reply_text(evaluation)
        else:
            update.message.reply_text("Algo fue mal")

def main():

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1230962206:AAHM3GrqAG9OIje4JWK7X-mKPsq39LelcmQ', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('peli', peli))
    # dp.add_handler(CommandHandler('start', start, pass_args=True))

    #echo command
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dp.add_handler(echo_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()




if __name__ == '__main__':
    main()