import warnings
from transformers import AutoModelForSequenceClassification, AutoTokenizer, logging
import torch.nn.functional as F
import torch



def probabilidade_IA(comentarios, modelos):
    # Desabilitar avisos e logs desnecessários
    warnings.filterwarnings("ignore")
    logging.set_verbosity_error()

    # Configuração do modelo
    model_id = "TrustSafeAI/RADAR-Vicuna-7B"
    device = "cpu"

    # Carregar modelo e tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model.eval()
    model.to(device)

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
                with torch.no_grad():
                    inputs = tokenizer(frase, return_tensors="pt", truncation=True, max_length=512)
                    inputs = {k: v.to(device) for k, v in inputs.items()}
                    logits = model(**inputs).logits

                    # Aplica softmax para obter as probabilidades
                    probabilities = F.softmax(logits, dim=-1)

                    # Obtém a probabilidade de ser IA e de ser humano em porcentagem
                    prob_ia = probabilities[0][0].item() * 100  # Probabilidade de ser IA em porcentagem
                    prob_human = (1 - probabilities[0][0].item()) * 100  # Probabilidade de ser humano em porcentagem

                    # Adiciona os resultados no formato desejado
                    resultados.append({
                        'llm': modelo,
                        'comentario': frase,
                        'prob_humano': round(prob_human, 2),
                        'prob_IA': round(prob_ia, 2)
                    })

    return resultados  # Retorna os resultados no formato desejado
