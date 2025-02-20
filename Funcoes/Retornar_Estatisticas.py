from collections import defaultdict
import os
import json
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
                                prob_humano = llm['prob_humano']  # Mantém a precisão exata
                                prob_IA = llm['prob_IA']  # Mantém a precisão exata
                                acerto = prob_IA  # O acerto é a probabilidade de IA detectada

                                item = {
                                    "detector": nome_diretorio[11:],
                                    # Exclui parte do nome do diretório conforme desejado
                                    "llm": llm['llm'],
                                    "prob_humano": prob_humano,  # Sem arredondamento
                                    "prob_IA": prob_IA,  # Sem arredondamento
                                    "tema": nome_arquivo[11:-5],  # Exclui parte do nome do arquivo conforme desejado
                                    "comentario": llm['comentario'],
                                    "acerto": acerto  # Sem arredondamento
                                }

                                dados_llms[llm['llm']].append(item)

                except Exception as e:
                    print(f"Erro ao processar o arquivo {caminho_completo}: {e}")

    lista_geral = []

    for llm in llms:
        if llm in dados_llms:
            lista_geral.extend(dados_llms[llm])


    return lista_geral


def calcular_acerto_por_llm(registros):
    acertos_por_llm = defaultdict(float)
    erros_por_llm = defaultdict(float)
    total_por_llm = defaultdict(int)

    for registro in registros:
        llm = registro['llm']
        prob_humano = registro['prob_humano']
        prob_IA = registro['prob_IA']

        # Soma os valores de probabilidade para cada LLM
        acertos_por_llm[llm] += prob_humano  # Quanto maior, mais eficaz a LLM
        erros_por_llm[llm] += prob_IA
        total_por_llm[llm] += 1

    # Calcula a média de acerto e erro para cada LLM
    medias_por_llm = {
        llm: {
            "acerto": acertos_por_llm[llm] / total_por_llm[llm],
            "erro": erros_por_llm[llm] / total_por_llm[llm]
        }
        for llm in acertos_por_llm
    }

    return medias_por_llm



def calcular_acerto_por_detector(registros):
    acertos_por_detector = defaultdict(float)
    erros_por_detector = defaultdict(float)
    total_por_detector = defaultdict(int)

    for registro in registros:
        detector = registro['detector']
        prob_humano = registro['prob_humano']
        prob_IA = registro['prob_IA']

        # Soma os valores de probabilidade para cada detector
        acertos_por_detector[detector] += prob_IA  # Quanto maior, mais eficaz o detector
        erros_por_detector[detector] += prob_humano
        total_por_detector[detector] += 1

    # Calcula a média de acerto e erro para cada detector
    medias_por_detector = {
        detector: {
            "acerto": acertos_por_detector[detector] / total_por_detector[detector],
            "erro": erros_por_detector[detector] / total_por_detector[detector]
        }
        for detector in acertos_por_detector
    }

    return medias_por_detector


def calcular_detector_tema(lista_geral):
    # Cria um dicionário para armazenar a soma dos acertos e total por detector e tema
    acertos_por_detector = {}

    # Preenche o dicionário com os dados de acertos por detector e tema
    for item in lista_geral:
        detector = item['detector']
        tema = item['tema']
        acerto = item['acerto']

        if detector not in acertos_por_detector:
            acertos_por_detector[detector] = {}

        if tema not in acertos_por_detector[detector]:
            acertos_por_detector[detector][tema] = {'total': 0, 'soma_acertos': 0}

        acertos_por_detector[detector][tema]['total'] += 1
        acertos_por_detector[detector][tema]['soma_acertos'] += acerto  # Soma a probabilidade de acerto

    # Agora, cria a lista de médias de efetividade por detector e tema
    lista_acertos = []
    for detector, temas in acertos_por_detector.items():
        for tema, dados in temas.items():
            total = dados['total']
            soma_acertos = dados['soma_acertos']
            media_efetividade = soma_acertos / total if total > 0 else 0
            lista_acertos.append({
                'detector': detector,
                'tema': tema,
                'media_efetividade': media_efetividade  # Média das probabilidades de acerto
            })

    # Ordena a lista por detector e depois por tema
    lista_acertos.sort(key=lambda x: (x['detector'], -x['media_efetividade']))


    return lista_acertos

def calcular_media_prob_humano_por_tema(resultado):
    # Dicionário para armazenar somatórios e contagens
    soma_prob_humano = {}
    contagem = {}

    # Itera sobre os registros
    for item in resultado:
        llm = item['llm']
        tema = item['tema']
        prob_humano = item['prob_humano']

        # Chave para o par (llm, tema)
        chave = (llm, tema)

        # Se a chave já existe, somamos e incrementamos a contagem
        if chave in soma_prob_humano:
            soma_prob_humano[chave] += prob_humano
            contagem[chave] += 1
        else:
            soma_prob_humano[chave] = prob_humano
            contagem[chave] = 1

    # Calcula a média de prob_humano para cada combinação de (llm, tema)
    medias = []
    for chave, soma in soma_prob_humano.items():
        llm, tema = chave
        media_prob_humano = soma / contagem[chave]
        medias.append({
            'llm': llm,
            'tema': tema,
            'media_prob_humano': media_prob_humano
        })

    # Ordena a lista pela LLM
    medias.sort(key=lambda x: x['llm'])

    return medias


def calcular_comentarios_proprios(dados):
    resultado = {}

    # Itera sobre cada detector e suas probabilidades
    for detector_data in dados:
        for detector in detector_data:
            nome_detector = detector['detector']
            probabilidades = detector['Probabilidades']

            # Inicializa as somas das probabilidades
            soma_acertos = 0
            soma_erros = 0

            # Itera sobre as probabilidades para somar acertos e erros separadamente
            for prob in probabilidades:
                soma_acertos += prob['prob_humano']  # Agora prob_humano é o acerto
                soma_erros += prob['prob_IA']  # Agora prob_IA é o erro

            # Calcula as médias de acerto e erro
            num_probabilidades = len(probabilidades)
            media_acerto = soma_acertos / num_probabilidades
            media_erro = soma_erros / num_probabilidades

            # Adiciona o resultado final para cada detector
            resultado[nome_detector] = {
                'acerto': media_acerto,
                'erro': media_erro
            }

    return resultado

