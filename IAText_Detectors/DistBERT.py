import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, logging
import torch.nn.functional as F
import warnings

def probabilidade_IA(comentarios, modelos):
    warnings.filterwarnings("ignore")

    # Desabilitar logs do transformers (Hugging Face)
    logging.set_verbosity_error()

    # Caminho para o modelo treinado
    model_path = '/home/gabriel/TCC_GabrielVncs/trained_model_HC3'

    # Carregar o modelo e o tokenizer do DistilBERT
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    tokenizer = DistilBertTokenizer.from_pretrained(model_path)

    if not isinstance(comentarios, list):
        raise ValueError("O argumento 'comentarios' deve ser uma lista.")

    resultados = []

    for item in comentarios:
        if not isinstance(item, dict) or 'llm' not in item or 'comentarios' not in item:
            continue  # Pula itens inválidos

        modelo = item['llm']
        texto = item['comentarios']

        if modelo in modelos and isinstance(texto, str):
            frases = texto.split("\n\n")  # Divide pelo separador duplo de nova linha
            frases = [frase.strip() for frase in frases if frase.strip()]  # Remove espaços extras

            for frase in frases:
                # Tokeniza a frase
                inputs = tokenizer(frase, return_tensors="pt", truncation=True, max_length=64, padding=True)
                outputs = model(**inputs)

                logits = outputs.logits

                # Aplica softmax para obter as probabilidades
                probabilities = F.softmax(logits, dim=-1)

                # Obtém a probabilidade de ser IA e de ser humano em porcentagem
                prob_ia = probabilities[0][1].item() * 100  # Probabilidade de ser IA em porcentagem
                prob_humano = probabilities[0][0].item() * 100  # Probabilidade de ser humano em porcentagem

                # Adiciona os resultados no formato desejado
                resultados.append({
                    'llm': modelo,
                    'comentario': frase,
                    'prob_humano': round(prob_humano, 2),
                    'prob_IA': round(prob_ia, 2)
                })

    return resultados  # Retorna os resultados no formato desejado


def probabilidade_IA_frase(frase):

    warnings.filterwarnings("ignore")
    logging.set_verbosity_error()
    modelo_path = "/home/gabriel/TCC_GabrielVncs/trained_model_HC3"

    # Carregar o modelo e o tokenizer do DistilBERT
    model = DistilBertForSequenceClassification.from_pretrained(modelo_path)
    tokenizer = DistilBertTokenizer.from_pretrained(modelo_path)

    if not isinstance(frase, str):
        raise ValueError("O argumento 'frase' deve ser uma string.")

    # Tokeniza a frase
    inputs = tokenizer(frase, return_tensors="pt", truncation=True, max_length=64, padding=True)
    outputs = model(**inputs)

    logits = outputs.logits

    # Aplica softmax para obter as probabilidades
    probabilities = F.softmax(logits, dim=-1)

    # Obtém a probabilidade de ser IA e de ser humano em porcentagem
    prob_ia = probabilities[0][1].item() * 100  # Probabilidade de ser IA em porcentagem
    prob_humano = probabilities[0][0].item() * 100  # Probabilidade de ser humano em porcentagem

    # Retorna as probabilidades
    return {
        'prob_humano': round(prob_humano, 2),
        'prob_IA': round(prob_ia, 2),
        'comentario': frase
    }
