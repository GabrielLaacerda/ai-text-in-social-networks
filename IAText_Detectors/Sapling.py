import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import matplotlib.pyplot as plt
import numpy as np

# Carregar o modelo GPT-2 e o tokenizer
model_name = 'gpt2'  # Pode usar 'gpt2-medium', 'gpt2-large', dependendo do seu hardware
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Colocar o modelo em modo de avaliação
model.eval()


def get_token_probs(text):
    """
    Função para obter as probabilidades de tokens usando GPT-2.
    """
    # Tokeniza o texto
    inputs = tokenizer(text, return_tensors='pt')

    # Obter as logits do modelo
    with torch.no_grad():
        outputs = model(**inputs)

    # Obter as probabilidades (softmax)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=-1)

    # Converter logits em probabilidades para os tokens
    token_probs = probs.squeeze().cpu().numpy()

    return token_probs


def plot_probs(text, token_probs):
    """
    Função para plotar as probabilidades dos tokens.
    """
    # Tokenizar novamente para obter as palavras e seus índices
    tokens = tokenizer.tokenize(text)

    # Plotando as probabilidades
    plt.figure(figsize=(12, 6))
    plt.bar(tokens, token_probs[:len(tokens)])
    plt.xticks(rotation=90)
    plt.xlabel('Tokens')
    plt.ylabel('Probabilidade')
    plt.title('Probabilidades das Palavras Geradas por GPT-2')
    plt.show()


# Texto de exemplo
text = "O cachorro correu pelo parque."

# Obter as probabilidades das palavras no texto
token_probs = get_token_probs(text)

# Visualizar as probabilidades
plot_probs(text, token_probs)
