from Binoculars.binoculars.detector import Binoculars
import warnings

def probabilidade_IA(comentarios, modelos):
    # Desabilitar avisos desnecessários
    warnings.filterwarnings("ignore")

    # Inicializa o Binoculars
    bino = Binoculars()

    if not isinstance(comentarios, list):
        raise ValueError("O argumento 'comentarios' deve ser uma lista.")

    resultados = []
    i = 1

    for item in comentarios:
        if not isinstance(item, dict) or 'llm' not in item or 'comentarios' not in item:
            continue  # Pula itens inválidos

        modelo = item['llm']
        texto = item['comentarios']

        if modelo in modelos and isinstance(texto, str):
            frases = texto.split("\n\n")  # Divide pelo separador duplo de nova linha
            frases = [frase.strip() for frase in frases if frase.strip()]  # Remove espaços extras

            for frase in frases:
                score = bino.compute_score(frase)  # Calcula a "probabilidade" com Binoculars

                prob_ia = max(0, min(score * 100, 100))  # Garante que prob_IA não ultrapasse 100%
                prob_human = max(0, 100 - prob_ia)  # Complemento correto de prob_IA

                resultados.append({
                    'llm': modelo,
                    'comentario': frase,
                    'prob_humano': round(prob_human, 2),
                    'prob_IA': round(prob_ia, 2)
                })
                print(f"{i} de 36:  {resultados}")
                i = i + 1

    return resultados  # Retorna os resultados no formato desejado


def probabilidade_IA_frase(frase):

    warnings.filterwarnings("ignore")
    modelo_binoculars = Binoculars()

    if not isinstance(frase, str):
        raise ValueError("O argumento 'frase' deve ser uma string.")

    # Calcula a "probabilidade" com Binoculars
    score = modelo_binoculars.compute_score(frase)

    prob_ia = max(0, min(score * 100, 100))  # Garante que prob_IA não ultrapasse 100%
    prob_human = max(0, 100 - prob_ia)  # Complemento correto de prob_IA

    # Retorna as probabilidades
    return {
        'prob_humano': round(prob_human, 2),
        'prob_IA': round(prob_ia, 2)
    }
