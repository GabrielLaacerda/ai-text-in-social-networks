import warnings
import json
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

# Função para processar uma única frase
def probabilidade_frase_unica(frase, model, tokenizer):
    warnings.filterwarnings("ignore")

    # Desabilitar logs do transformers (Hugging Face)
    logging.set_verbosity_error()

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

# Função para processar o arquivo de comentários e calcular as probabilidades
def processar_comentarios_arquivo(nome_arquivo):
    warnings.filterwarnings("ignore")

    # Desabilitar logs do transformers (Hugging Face)
    logging.set_verbosity_error()

    # Define o repositório do modelo
    model_name = "roberta-large-openai-detector"

    # Baixa o modelo e o tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Abre o arquivo de comentários
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            comentarios = f.read().split("\n\n")  # Divide os comentários por linhas duplas

        resultados = []

        for comentario in comentarios:
            comentario = comentario.strip()  # Remove espaços extras no início e fim
            if comentario:  # Apenas processa comentários não vazios
                resultado = probabilidade_frase_unica(comentario, model, tokenizer)
                resultados.append(resultado)

        return resultados  # Retorna os resultados no formato desejado

    except FileNotFoundError:
        raise ValueError(f"O arquivo '{nome_arquivo}' não foi encontrado.")

# Função para salvar os resultados em um arquivo JSON
def salvar_resultados_em_json(resultados, nome_arquivo_saida):
    try:
        with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=4)
        print(f"Resultados_Roberta salvos em {nome_arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

# Processa o arquivo e calcula as probabilidades
comentarios_com_probabilidade = processar_comentarios_arquivo('/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Comentarios_Filtrados/Impostos.txt')

# Salva os resultados em um arquivo JSON
salvar_resultados_em_json(comentarios_com_probabilidade, '/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/Resultados_Roberta/resultados_Impostos.json')

# Exibir os resultados
for resultado in comentarios_com_probabilidade:
    print(f"Comentário: {resultado['comentario']}")
    print(f"Probabilidade de ser humano: {resultado['prob_humano']}%")
    print(f"Probabilidade de ser IA: {resultado['prob_IA']}%\n")
