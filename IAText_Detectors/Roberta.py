import warnings
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging
import torch.nn.functional as F
import torch

# Função comum para calcular as probabilidades
def calcular_probabilidade(frase, model, tokenizer):
    inputs = tokenizer(frase, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)

    logits = outputs.logits

    # Aplica softmax para obter as probabilidades
    probabilities = F.softmax(logits, dim=-1)

    # Obtém a probabilidade de ser IA e de ser humano em porcentagem
    prob_ia = probabilities[0][1].item() * 100  # Probabilidade de ser IA em porcentagem
    prob_human = probabilities[0][0].item() * 100  # Probabilidade de ser humano em porcentagem

    return round(prob_human, 2), round(prob_ia, 2)

# Função para processar a lista de comentários
def probabilidade_IA(comentarios, modelos):
    warnings.filterwarnings("ignore")

    # Desabilitar logs do transformers (Hugging Face)
    logging.set_verbosity_error()

    # Define o repositório do modelo
    model_name = "roberta-large-openai-detector"

    # Baixa o modelo e o tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

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
                # Chama a função comum para calcular as probabilidades
                prob_human, prob_ia = calcular_probabilidade(frase, model, tokenizer)

                # Adiciona os resultados no formato desejado
                resultados.append({
                    'llm': modelo,
                    'comentario': frase,
                    'prob_humano': prob_human,
                    'prob_IA': prob_ia
                })

    return resultados  # Retorna os resultados no formato desejado

def probabilidade_IA_comentarios_proprios(comentarios):
    warnings.filterwarnings("ignore")

    # Desabilitar logs do transformers (Hugging Face)
    logging.set_verbosity_error()

    # Define o repositório do modelo
    model_name = "roberta-large-openai-detector"

    # Baixa o modelo e o tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if not isinstance(comentarios, list):
        raise ValueError("O argumento 'comentarios' deve ser uma lista.")

    resultados = []

    for item in comentarios:
        if item:
            prob_human, prob_ia = calcular_probabilidade(item, model, tokenizer)

            resultados.append({
                'prob_humano': prob_human,
                'prob_IA': prob_ia
            })

    return resultados  # Retorna os resultados no formato desejado

# Função para processar uma única frase
def probabilidade_frase_unica(frase):
    warnings.filterwarnings("ignore")

    # Desabilitar logs do transformers (Hugging Face)
    logging.set_verbosity_error()

    # Define o repositório do modelo
    model_name = "roberta-large-openai-detector"

    # Baixa o modelo e o tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if not isinstance(frase, str):
        raise ValueError("O argumento 'frase' deve ser uma string.")

    # Chama a função comum para calcular as probabilidades
    prob_human, prob_ia = calcular_probabilidade(frase, model, tokenizer)

    # Retorna os resultados no formato desejado
    return {
        'comentario': frase,
        'prob_humano': prob_human,
        'prob_IA': prob_ia
    }
