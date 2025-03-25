import os
import pandas as pd
import nltk
import re

import torch
from nltk.tokenize import word_tokenize, sent_tokenize
import logging
import string
from nltk.corpus import stopwords
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import math


logging.getLogger('nltk').setLevel(logging.CRITICAL)

# Baixar pacotes necessários sem exibir logs
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def contar_palavras(texto):
    palavras = word_tokenize(texto)
    palavras = [p for p in palavras if p not in string.punctuation]
    return len(palavras)


# Função para verificar formalidade
def verificar_formalidade(texto):
    # Define palavras que indicam informalidade
    palavras_informais = [
        'vc', 'kkk', 'pq', 'mano', 'galera', 'tá', 'bicho', 'véi', 'mó', 'parada', 'rolê', 'bagulho', 'mó fita',
        'papo', 'tipo', 'festa', 'gato', 'caraca', 'brota', 'caralho', 'tô ligado', 'tá ligado', 'da hora', 'brisa',
        'se liga', 'migué', 'bora', 'tamo junto', 'sarrada', 'bancada', 'bagaceira', 'na moral', 'só na paz',
        'na boa', 'zueira', 'caô', 'firula', 'tirar onda', 'xaveco', 'foguete', 'banco', 'mó treta', 'cachorrada',
        'figura', 'lance', 'tá ligado', 'parada sinistra', 'rolêzão', 'bichão', 'se pá', 'tô de boa', 'suave', 'bala',
        'pode crer', 'tá tranquilo', 'fumar um', 'na moralzinha', 'girar', 'mandar ver', 'top', 'irado', 'filho da mãe',
        'mermão', 'meu chapa', 'fugir da rotina', 'dar um rolê', 'se der', 'caraca', 'morreu de rir', 'bicho',
        'pegar leve',
        'vibe', 'de boa', 'correr atrás', 'quebrar tudo', 'chave', 'tá zoando', 'só que não', 'balar',
        'vazou', 'só no sapatinho', 'marotagem', 'doideira', 'aí sim', 'pegar geral', 'mermão', 'fechou', 'zicar',
        'dar um gás', 'arrebentar', 'rolando', 'muito loco', 'quicar', 'trolar', 'deixa quieto', 'ferrar', 'vai na fé',
        'de boa', 'baixaria', 'bizarro', 'comédia', 'festa doida', 'morô', 'ferver', 'trem', 'catraca', 'balada',
        'bancada', 'do meu jeito', 'bagunça', 'bancando', 'ficar de boa', 'festa estranha', 'meu chapa', 'pior',
        'figuraça', 'sem noção', 'caindo na net', 'fazer o rolê', 'mandar bem', 'no grau', 'parada sinistra', 'focar',
        'mandar aquele gás', 'puxar o saco', 'irado', 'chegar junto',
        'tira onda',
        'arrebentar', 'tá caindo', 'rolando', 'pior que', 'desencanar', 'mó doideira', 'acelerar', 'botar pra quebrar',
        'não é mais', 'baixar', 'fora da curva', 'sem vergonha', 'banco de praça', 'dá-lhe', 'nóis', 'banco de praça',
        'só rindo', 'teu jeito', 'se liga', 'coisarada', 'sem noção', 'suave', 'só por cima', 'cabelo de boneca',
        'embromation', 'só nos 50', 'descer o pau', 'focar no que importa', 'zicar', 'na boca do povo', 'que barato',
        'começo de festa', 'quebra tudo', 'carinha de quem', 'trabalhar de graça', 'irado',
        'bagulho bom',
        'dormir de boa', 'balançar', 'gambiarra', 'rolar no chão', 'dar uns rolês', 'mistura boa', 'brincar',
        'morrer de rir',
        'amassar', 'cabeludo', 'cabeça de vento', 'não é brincadeira', 'banca de praça', 'fiado', 'só a zoeira',
        'tô contigo',
        'trem bom', 'bagulho', 'trabalhar pra dar certo', 'girar', 'deixa quieto', 'ficar esperto', 'quicar',
        'tá na boa',
        'na vibe', 'só brisa', 'top da balada', 'ficar com moral', 'se pá', 'ir pra casa', 'na moralzinha',
        'só uma ideia',
        'tá tranquilo', 'tá suave', 'vamos nessa', 'puxa', 'pode crer', 'mandar bala', 'brisa louca', 'rola',
        'melhor que nada',
        'sentir a vibe', 'zoando', 'caindo no palco', 'tirar onda', 'pôr no grau', 'arrebentando', 'se é assim',
        'só resenha',
        'descer o pau', 'ir no grau', 'mandar brasa', 'balada boa', 'ficar na paz', 'se não', 'do jeito que dá', 'zoar',
        'pular o muro', 'arrebentar a boca do balão', 'tá ligado', 'só os melhores', 'tá de boa', 'só o picote',
        'arrebenta',
        'festa fechada', 'quebra tudo', 'vai vendo', 'comer o pão que o diabo amassou', 'essa é a fita', 'tropa',
        'pesada',
        'bico', 'desce o barraco', 'tá batido', 'fui', 'não tá fácil', 'dá-lhe', 'parada', 'arranjar treta',
        'ver a galera',
        'rolê top', 'ficar de cara', 'brota na fita', 'se rolar', 'só no grau', 'mó cara de pau', 'pedir benção',
        'girar a parada'
    ]

    informal = any(re.search(rf'\b{re.escape(palavra)}\b', texto.lower()) for palavra in palavras_informais)

    if informal:
        return 'Informal'
    else:
        return 'Formal'


# Função para detectar a presença de gírias
def verificar_girias(texto):
    girias = [
        'grana', 'rolê', 'bagulho', 'mó', 'papo', 'parada', 'mano', 'véi', 'migué', 'zueira', 'caô', 'firula',
        'festa', 'gato', 'caraca', 'brota', 'caralho', 'tô ligado', 'tá ligado', 'tipo', 'da hora', 'bagaceira',
        'na moral', 'se liga', 'bora', 'tamo junto', 'rolando', 'sarrada', 'bora lá', 'vibe', 'se pá', 'mó fita',
        'só que não', 'xaveco', 'chave', 'foguete', 'banco', 'mó treta', 'cachorrada', 'brisa', 'figura', 'lance',
        'só na paz', 'parada', 'suave', 'barraco', 'safado', 'enrolar', 'mermão', 'barato', 'se pá', 'morô', 'dá-lhe',
        'zoeira', 'na moralzinha', 'bichão', 'dorgas', 'quicar', 'tirar onda', 'foda-se', 'irado', 'batalha', 'tiração',
        'linda', 'pegar o bonde', 'arrebentar', 'jogar na cara', 'parada sinistra', 'tiro certo', 'chave de cadeia',
        'taca-lhe pau', 'top', 'vazou', 'rolou', 'de boa', 'curtindo', 'burrice', 'bunda', 'pesada', 'balada',
        'sente o drama', 'ferrar', 'pode crer', 'neura', 'sujeira', 'chapar', 'bizarro', 'trem', 'talarico',
        'ficar de boa', 'tá na boca do povo', 'meu chapa', 'treta', 'gritar', 'beber', 'catraca', 'farra', 'pô',
        'daquele jeito', 'pegar geral', 'correr atrás', 'arrebentando', 'chato', 'fofoca', 'encher o saco', 'bagunça',
        'chapado', 'tropa', 'morreu de rir', 'doideira', 'lavagem', 'disfarçado', 'trolar', 'marotagem', 'futucar',
        'balançar', 'puxar o saco', 'comédia', 'maroto', 'tocar o terror', 'puxar', 'girar', 'deve ser', 'se acende',
        'não é mais', 'caindo na net', 'rolêzão', 'zicar', 'sem noção', 'banca', 'conversinha', 'perrengue', 'galera',
        'playboy', 'batalha de rima', 'mandar bem', 'chegar junto', 'bagunçar', 'esquecer', 'dar uma moral', 'estourar',
        'ficar suave', 'esquentar a cabeça', 'tá suave', 'da hora', 'dar o fora', 'mandar bala', 'tá ligado', 'mermão',
        'que rolê', 'dar um gás', 'dar um perdido', 'se pá', 'amassar', 'tá de sacanagem', 'zicar', 'mandar ver',
        'entrar na onda', 'dar uma de louco', 'mandar um salve', 'na fita', 'rolo', 'bancada', 'topzera', 'pagar mico',
        'tirar onda', 'dar fuga', 'vibe boa', 'não é brinquedo', 'cair na net', 'mó confusão', 'ficar na paz',
        'caô', 'barraco', 'grana preta', 'ficar de cara', 'zoando', 'se amarrou', 'bancar', 'ficar de boa',
        'passar pano',
        'no sapatinho', 'ficar na zueira', 'na pegada', 'caindo na real', 'tirar sarro', 'zoeira leve',
        'rolar aquele papo',
        'de boas', 'marolar', 'descer o pau', 'fazer o trampo', 'mandar o salve', 'gambiarra', 'puxar uma brisa',
        'arrebentar no role', 'não curtir', 'ligar o foda-se', 'mandar parar', 'jogar o charme', 'se perder',
        'chutar o balde',
        'bancando', 'tá fraco', 'bancada de rua', 'dar o perdido', 'rolando a boa', 'meu chapa', 'se liga no rolê',
        'marotar', 'mandar bala', 'não dar moral', 'deixa quieto', 'fazer o trampo', 'girar a parada', 'zicar o rolê',
        'sem dó', 'atrasado', 'pular fora', 'mó relax', 'ficar relax', 'ficar no corre', 'pedir benção', 'sem mais',
        'se der', 'dar no pente', 'rebolar', 'encostar', 'caindo na boca do povo', 'só na zoeira', 'dar risada',
        'só na confiança', 'dar uma acalmada', 'na moralzinha', 'dar aquela moral', 'chamar no rolê', 'vai nessa',
        'dar no saco', 'mó perrengue', 'vai dar bom', 'bancando o rolê', 'se amarrar', 'puxar o saco', 'enrolar',
        'tava junto', 'tá com moral', 'caindo fora', 'mandar ver', 'ficar com moral', 'ficar esperto', 'dar no grau'
    ]

    return any(giria in texto.lower() for giria in girias)


def verificar_emojis(texto):
    emojis = re.findall(
        r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]|[\U00002700-\U000027BF]',
        texto)
    return bool(emojis)


def extrair_tema(nome_arquivo):
    partes = nome_arquivo.split('_')
    return partes[1] if len(partes) > 1 else 'Desconhecido'


def processar_comentarios(diretorio):
    resultados = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(diretorio, arquivo)

            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                texto = file.read()

            # Dividindo o conteúdo do arquivo em comentários, considerando que cada linha é um comentário
            comentarios = texto.split('\n')

            # Inicializa as listas para armazenar as características de cada comentário
            tamanhos = []
            formalidades = []
            girias = []
            emojis = []
            complexidade = []
            lexical = []
            stopW = []
            perplexidade = []

            for comentario in comentarios:
                if comentario.strip():  # Ignora comentários vazios
                    tamanhos.append(contar_palavras(comentario))
                    formalidades.append(verificar_formalidade(comentario))  # Aqui coleta a formalidade para cada comentário
                    girias.append(verificar_girias(comentario))
                    emojis.append(verificar_emojis(comentario))
                    complexidade.append(flesch_kincaid(comentario))
                    lexical.append(riqueza_lexical(comentario))
                    stopW.append(frequencia_stopwords(comentario))
                    #perplexidade.append(calcular_perplexidade(comentario))


            # Calcula as médias das características de todos os comentários
            tamanho_medio = sum(tamanhos) / len(tamanhos) if tamanhos else 0

            # Cálculo da formalidade média agora como uma média numérica (1 para formal, 0 para informal)
            formalidade_numerica = [1 if f == 'Formal' else 0 for f in formalidades]
            formalidade_media = sum(formalidade_numerica) / len(formalidade_numerica) if formalidade_numerica else 0

            # Convertendo a média numérica para o valor "Formal" ou "Informal"
            formalidade_resultado = 'Formal' if formalidade_media >= 0.5 else 'Informal'

            giria_media = sum(girias) / len(girias) if girias else 0
            emoji_media = sum(1 for e in emojis if e) / len(emojis) if emojis else 0

            # Extrai o tema e LLM do nome do arquivo
            tema = extrair_tema(arquivo)
            llm = arquivo.split('_')[0]  # O nome do LLM é a primeira parte do nome do arquivo

            complexidadeMedia = sum(complexidade) / len(complexidade)
            lexicalMedia = sum(lexical) / len(lexical)
            stopWMedia= sum(stopW) / len(stopW)
            #perplexidadeMedia = sum(perplexidade) / len(perplexidade)

            # Adiciona os dados ao resultado
            resultados.append({
                'llm': llm,
                'tema': tema[:-4],
                'tamanho_medio': tamanho_medio,
                'formalidade': formalidade_resultado,
                'giria_media': f"{giria_media*100:.2f}%",
                'emoji_media': f"{emoji_media*100:.2f}%",
                'Complexidade de Leitura (Flesch-Kincaid)': complexidadeMedia,
                'Riqueza Lexical' : lexicalMedia,
                'Frequencia StopWords' : stopWMedia,
                #'Perplexidade': perplexidadeMedia
            })

    # Cria um DataFrame com os resultados
    df_resultados = pd.DataFrame(resultados)
    return df_resultados

def frequencia_stopwords(texto):
    # Obter a lista de stopwords do NLTK para o idioma português
    stopwords_pt = stopwords.words('portuguese')
    # Tokenizar o texto em palavras
    palavras = word_tokenize(texto.lower())
    # Remover palavras que não são alfabéticas
    palavras = [p for p in palavras if p.isalpha()]
    # Contar as stopwords
    stopwords_encontradas = [p for p in palavras if p in stopwords_pt]
    # Calcular a frequência de stopwords
    num_stopwords = len(stopwords_encontradas)
    num_palavras = len(palavras)
    frequencia_stopwords = num_stopwords / num_palavras if num_palavras > 0 else 0
    return frequencia_stopwords

def riqueza_lexical(texto):
    # Tokenizar o texto em palavras
    palavras = word_tokenize(texto.lower())
    # Obter a lista de stopwords
    stop_words = set(stopwords.words('portuguese'))
    # Remover palavras que não são alfabéticas ou stopwords
    palavras = [p for p in palavras if p.isalpha() and p not in stop_words]
    # Calcular a riqueza lexical
    num_palavras = len(palavras)
    num_palavras_unicas = len(set(palavras))  # set() para pegar palavras únicas
    riqueza_lexical = num_palavras_unicas / num_palavras if num_palavras > 0 else 0
    return riqueza_lexical


def calcular_perplexidade(texto):
    model_name = "gpt2"  # Pode-se usar outros modelos como "gpt2-medium", "gpt2-large", etc.
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    # Tokenizar o texto
    inputs = tokenizer(texto, return_tensors="pt")

    # Obter as probabilidades logarítmicas dos tokens
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        log_likelihood = outputs.loss.item()

    # Calcular a perplexidade
    perplexidade = math.exp(log_likelihood)
    return perplexidade


def flesch_kincaid(texto):
    palavras = word_tokenize(texto)
    sentencas = sent_tokenize(texto)
    total_palavras = len(palavras)
    total_sentencas = len(sentencas)
    total_silabas = sum([len(re.findall(r'[aeiouáéíóúãõâêîôûà]', palavra, re.IGNORECASE)) for palavra in palavras])

    # Fórmula Flesch-Kincaid
    RE = 206.835 - (1.015 * (total_palavras / total_sentencas)) - (84.6 * (total_silabas / total_palavras))
    return RE

# Diretório onde estão os arquivos
diretorio = '/home/gabriel/TCC_GabrielVncs/Comentarios_Gerados_PrimeiraEtapa'


df_resultados = processar_comentarios(diretorio)
df_resultados_ordenado = df_resultados.sort_values(by=['llm'])

print(df_resultados_ordenado)

