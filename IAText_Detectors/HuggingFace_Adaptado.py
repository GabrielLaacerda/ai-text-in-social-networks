import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
import json
from torch import cuda

ACCESS_TOKEN = os.getenv('HUGGING_FACE_API_KEY')  # Certifique-se de definir a chave de API corretamente


# Função para dividir o texto em sentenças
def text_to_sentences(text):
    clean_text = text.replace('\n', ' ')
    return re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', clean_text)


# Função para dividir o texto em pedaços de 900 caracteres
def chunks_of_900(text, chunk_size=900):
    sentences = text_to_sentences(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk + sentence) <= chunk_size:
            if len(current_chunk) != 0:
                current_chunk += " " + sentence
            else:
                current_chunk += sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    chunks.append(current_chunk)
    return chunks


# Função para fazer a previsão
def predict(query, model, tokenizer, device):
    tokens = tokenizer.encode(query)
    tokens = tokens[:tokenizer.model_max_length - 2]
    tokens = torch.tensor([tokenizer.bos_token_id] + tokens + [tokenizer.eos_token_id]).unsqueeze(0)
    mask = torch.ones_like(tokens)

    with torch.no_grad():
        logits = model(tokens.to(device), attention_mask=mask.to(device))[0]
        probs = logits.softmax(dim=-1)

    fake, real = probs.detach().cpu().flatten().numpy().tolist()
    return real


# Função para calcular a probabilidade de um texto ser real
def findRealProb(text, model, tokenizer, device):
    chunksOfText = chunks_of_900(text)
    results = []
    for chunk in chunksOfText:
        output = predict(chunk, model, tokenizer, device)
        results.append([output, len(chunk)])

    ans = 0
    cnt = 0
    for prob, length in results:
        cnt += length
        ans = ans + prob * length
    realProb = ans / cnt
    return {"Real": realProb, "Fake": 1 - realProb}, results


# Função principal para processar o arquivo e gerar as probabilidades
def processar_comentarios_arquivo(nome_arquivo):
    device = 'cuda' if cuda.is_available() else 'cpu'

    # Carregar o modelo e tokenizer
    tokenizer = AutoTokenizer.from_pretrained("PirateXX/AI-Content-Detector", token=ACCESS_TOKEN)
    model = AutoModelForSequenceClassification.from_pretrained("PirateXX/AI-Content-Detector", token=ACCESS_TOKEN)
    model.to(device)

    # Ler o arquivo de comentários
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            comentarios = f.read().split("\n\n")  # Divide os comentários por linhas duplas
    except FileNotFoundError:
        raise ValueError(f"O arquivo '{nome_arquivo}' não foi encontrado.")

    resultados = []

    # Processar cada comentário
    for comentario in comentarios:
        comentario = comentario.strip()  # Remover espaços extras
        if comentario:  # Processa somente comentários não vazios
            probabilidade = findRealProb(comentario, model, tokenizer, device)
            real_prob = round(probabilidade[0]['Real'] * 100, 2)  # Probabilidade real
            fake_prob = round(100 - real_prob, 2)  # Probabilidade fake

            # Adicionar os resultados no formato desejado
            resultados.append({
                "comentario": comentario,
                "prob_humano": real_prob,
                "prob_IA": fake_prob
            })

    return resultados


# Função para salvar os resultados em um arquivo JSON
def salvar_resultados_json(resultados, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as json_file:
        json.dump(resultados, json_file, ensure_ascii=False, indent=4)
    print(f"Resultados salvos em '{nome_arquivo_saida}'.")


# Caminho para o arquivo de entrada
arquivo_entrada = '/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Comentarios_Filtrados/InteligenciaArtificial.txt'
arquivo_saida = '/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_HuggingFace/resultados_InteligenciaArtificial.json'

# Processar o arquivo e salvar os resultados
resultados = processar_comentarios_arquivo(arquivo_entrada)
salvar_resultados_json(resultados, arquivo_saida)
