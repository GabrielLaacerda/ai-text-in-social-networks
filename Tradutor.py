from googletrans import Translator


def traduzir_texto(texto, src='pt', dest='en'):

    translator = Translator()
    translated = translator.translate(texto, src=src, dest=dest)

    return translated.text