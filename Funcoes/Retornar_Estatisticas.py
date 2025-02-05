from collections import defaultdict

import os
import json

def calcular_estatisticas_tabela(llms, dir_base):
    lista_geral = []

    # Estrutura de armazenamento para os LLMs com seus itens
    dados_llms = {llm: [] for llm in llms}

    for raiz, _, arquivos in os.walk(dir_base):
        for nome in arquivos:
            caminho_completo = os.path.join(raiz, nome)
            diretorio_atual = os.path.dirname(caminho_completo)  # Pega o diretório do caminho completo
            nome_diretorio = os.path.basename(diretorio_atual)
            nome_arquivo = os.path.basename(nome)

            if nome.endswith(".json"):
                try:
                    with open(caminho_completo, "r", encoding="utf-8") as f:
                        dados = json.load(f)

                        for llm in dados:
                            # Verifica se as chaves existem no item antes de acessar
                            if llm.get('llm') in llms and 'prob_humano' in llm and 'prob_IA' in llm:
                                item = {
                                    "detector": nome_diretorio[11:],
                                    "llm": llm['llm'],
                                    "prob_humano": llm['prob_humano'],
                                    "prob_IA": llm['prob_IA'],  # Quanto maior, melhor a detecção de IA
                                    "tema": nome_arquivo[11:-5],
                                    "comentario": llm['comentario'],
                                    "acerto": llm['prob_IA']  # O acerto é a probabilidade de IA detectada
                                }

                                dados_llms[llm['llm']].append(item)

                except Exception as e:
                    print(f"Erro ao processar o arquivo {caminho_completo}: {e}")

    # Agora, ordenamos os itens dentro de cada LLM por tema
    for llm in dados_llms:
        dados_llms[llm].sort(key=lambda x: x['tema'])  # Ordena por 'tema' dentro de cada LLM

    # Agora, reordenamos a lista geral para garantir a ordem de LLMs: ['Cohere', 'ChatGPT', 'Gemini', 'Llama', 'MaritacaIA', 'Mistral']
    lista_geral = []

    for llm in llms:
        if llm in dados_llms:
            lista_geral.extend(dados_llms[llm])

    # Ordena a lista geral primeiro por detector, depois por LLM e por maior acerto (prob_IA)
    lista_geral.sort(key=lambda x: (x['detector'], llms.index(x['llm'])), reverse=False)
    lista_geral.sort(key=lambda x: x['acerto'], reverse=True)  # Ordena do maior para o menor acerto

    return lista_geral


def calcular_acerto_por_detector(registros):
    acertos_por_detector = defaultdict(float)
    erros_por_detector = defaultdict(float)
    total_por_detector = defaultdict(int)

    for registro in registros:
        detector = registro['detector']
        prob_humano = registro['prob_humano']
        prob_IA = registro['prob_IA']

        # A acurácia do detector é baseada na probabilidade atribuída à IA
        acertos_por_detector[detector] += prob_IA
        erros_por_detector[detector] += prob_humano
        total_por_detector[detector] += 1

    # Calcula a porcentagem de acerto e erro média de cada detector
    resultado = {
        detector: {
            "acerto": (acertos_por_detector[detector] / total_por_detector[detector]),
            "erro": (erros_por_detector[detector] / total_por_detector[detector])
        }
        for detector in acertos_por_detector
    }

    return resultado