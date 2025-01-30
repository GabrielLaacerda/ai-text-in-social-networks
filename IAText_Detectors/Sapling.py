import requests
import warnings

def probabilidade_IA(comentarios, modelos):
    warnings.filterwarnings("ignore")

    # Define a chave da API e o endpoint
    api_key = "ELC1FVXZVPSCUJJB2N4P6WFHC9272EOO"
    url = "https://api.sapling.ai/api/v1/aidetect"

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
                # Chama a API da Sapling para detecção de IA
                response = requests.post(
                    url,
                    json={
                        "key": api_key,
                        "text": frase
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    prob_ia = result['score'] * 100  # Probabilidade de ser IA
                    prob_human = (1 - result['score']) * 100  # Probabilidade de ser humano

                    # Adiciona os resultados no formato desejado
                    resultados.append({
                        'llm': modelo,
                        'comentario': frase,
                        'prob_humano': round(prob_human, 2),
                        'prob_IA': round(prob_ia, 2)
                    })
                else:
                    print(f"Erro ao chamar a API: {response.status_code}")

    return resultados  # Retorna os resultados no formato desejado

