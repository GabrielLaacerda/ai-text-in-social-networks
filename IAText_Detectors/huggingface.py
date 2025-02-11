from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch import cuda
import os
import re

ACCESS_TOKEN = os.getenv('HUGGING_FACE_API_KEY')

def probabilidade_IA(comentarios, modelos):

    device = 'cuda' if cuda.is_available() else 'cpu'
    tokenizer = AutoTokenizer.from_pretrained("PirateXX/AI-Content-Detector", token=ACCESS_TOKEN)
    model = AutoModelForSequenceClassification.from_pretrained("PirateXX/AI-Content-Detector", token=ACCESS_TOKEN)
    model.to(device)

    def text_to_sentences(text):
        clean_text = text.replace('\n', ' ')
        return re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', clean_text)

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

    def predict(query):
        tokens = tokenizer.encode(query)
        tokens = tokens[:tokenizer.model_max_length - 2]
        tokens = torch.tensor([tokenizer.bos_token_id] + tokens + [tokenizer.eos_token_id]).unsqueeze(0)
        mask = torch.ones_like(tokens)

        with torch.no_grad():
            logits = model(tokens.to(device), attention_mask=mask.to(device))[0]
            probs = logits.softmax(dim=-1)

        fake, real = probs.detach().cpu().flatten().numpy().tolist()
        return real

    def findRealProb(text):
        chunksOfText = chunks_of_900(text)
        results = []
        for chunk in chunksOfText:
            output = predict(chunk)
            results.append([output, len(chunk)])

        ans = 0
        cnt = 0
        for prob, length in results:
            cnt += length
            ans = ans + prob * length
        realProb = ans / cnt
        return {"Real": realProb, "Fake": 1-realProb}, results

    result = []
    for item in comentarios:
        if not isinstance(item, dict) or 'llm' not in item or 'comentarios' not in item:
            continue  # Pula itens inválidos

        modelo = item['llm']
        texto = item['comentarios']

        if modelo in modelos and isinstance(texto, str):
            frases = texto.split("\n\n")  # Divide pelo separador duplo de nova linha
            frases = [frase.strip() for frase in frases if frase.strip()]

            for frase in frases:
                probabilidade = findRealProb(frase)  # Obtém a probabilidade de ser "real"
                real_prob = probabilidade[0]['Real']  # A probabilidade "real"
                fake_prob = 1 - real_prob  # A probabilidade de ser "fake"

                # Adiciona o comentário e as probabilidades no formato desejado
                result.append({
                    "llm": modelo,
                    "comentario": frase,
                    "prob_humano": real_prob * 100,  # Multiplicado por 100 para porcentagem
                    "prob_IA": fake_prob * 100  # Multiplicado por 100 para porcentagem
                })

    return result
