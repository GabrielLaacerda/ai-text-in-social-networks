import requests
import warnings
import time

# Função comum para calcular a probabilidade usando a API
# Função para calcular a probabilidade e medir o tempo de chamada da API
def calcular_probabilidade_api(frase, api_key, url):
    inicio = time.time()  # Marca o início da requisição

    response = requests.post(
        url,
        json={
            "key": api_key,
            "text": frase
        }
    )

    fim = time.time()  # Marca o fim da requisição
    tempo_execucao = fim - inicio  # Calcula o tempo de execução da API

    if response.status_code == 200:
        result = response.json()
        prob_ia = result['score'] * 100  # Probabilidade de ser IA
        prob_human = (1 - result['score']) * 100  # Probabilidade de ser humano
        return round(prob_human, 2), round(prob_ia, 2), tempo_execucao
    else:
        print(f"Erro ao chamar a API: {response.status_code}")
        return None, None, None  # Retorna None em caso de erro na API

# Função para processar a lista de comentários
def probabilidade_IA(comentarios, modelos):
    warnings.filterwarnings("ignore")

    # Define a chave da API e o endpoint
    api_key = "1JIQU55BWAMDEXSZ0QZONSVZR2KWZRCQ"
    url = "https://api.sapling.ai/api/v1/aidetect"

    if not isinstance(comentarios, list):
        raise ValueError("O argumento 'comentarios' deve ser uma lista.")

    resultados = []
    tempos_execucao = []  # Lista para armazenar os tempos de requisição da API

    for item in comentarios:
        if not isinstance(item, dict) or 'llm' not in item or 'comentarios' not in item:
            continue  # Pula itens inválidos

        modelo = item['llm']
        texto = item['comentarios']

        if modelo in modelos and isinstance(texto, str):
            frases = texto.split("\n\n")  # Divide pelo separador duplo de nova linha
            frases = [frase.strip() for frase in frases if frase.strip()]  # Remove espaços extras

            for frase in frases:
                # Chama a API e mede o tempo de execução
                prob_human, prob_ia, tempo_execucao = calcular_probabilidade_api(frase, api_key, url)

                if prob_human is not None and prob_ia is not None:
                    tempos_execucao.append(tempo_execucao)  # Armazena o tempo de execução

                    # Adiciona os resultados no formato desejado
                    resultados.append({
                        'llm': modelo,
                        'comentario': frase,
                        'prob_humano': prob_human,
                        'prob_IA': prob_ia
                    })

    # Calcula a média do tempo de requisição por inferência
    media_tempo = sum(tempos_execucao) / len(tempos_execucao) if tempos_execucao else 0
    print(f"Média de tempo por requisição API: {media_tempo:.6f} segundos")

    return resultados  # Retorna os resultados no formato desejado

def probabilidade_IA_comentarios_proprios(comentarios):
    warnings.filterwarnings("ignore")

    # Define a chave da API e o endpoint
    api_key = "1JIQU55BWAMDEXSZ0QZONSVZR2KWZRCQ"
    url = "https://api.sapling.ai/api/v1/aidetect"

    if not isinstance(comentarios, list):
        raise ValueError("O argumento 'comentarios' deve ser uma lista.")

    resultados = []

    for item in comentarios:
        if item:
            prob_human, prob_ia = calcular_probabilidade_api(item, api_key, url)

            if prob_human is not None and prob_ia is not None:
                # Adiciona os resultados no formato desejado
                resultados.append({
                    'prob_humano': prob_human,
                    'prob_IA': prob_ia
                })

    return resultados  # Retorna os resultados no formato desejado

# Função para processar uma única frase
def probabilidade_frase_unica(frase):
    warnings.filterwarnings("ignore")

    # Define a chave da API e o endpoint
    api_key = "ELC1FVXZVPSCUJJB2N4P6WFHC9272EOO"
    url = "https://api.sapling.ai/api/v1/aidetect"

    if not isinstance(frase, str):
        raise ValueError("O argumento 'frase' deve ser uma string.")

    # Chama a função comum para calcular as probabilidades via API
    prob_human, prob_ia = calcular_probabilidade_api(frase, api_key, url)

    if prob_human is not None and prob_ia is not None:
        # Retorna os resultados no formato desejado
        return {
            'comentario': frase,
            'prob_humano': prob_human,
            'prob_IA': prob_ia
        }
    else:
        return None
