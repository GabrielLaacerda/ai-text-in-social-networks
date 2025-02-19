import json
import re


def parse_file(input_file, output_file):
    llm_sequence = ['Cohere', 'ChatGPT', 'DeepSeek', 'Gemini', 'Llama', 'MaritacaIA', 'Mistral']
    llm_index = 0
    comments = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    i = 0
    while i < len(lines) - 1:
        comentario = lines[i].strip()
        match = re.search(r'(\d+\.?\d*)%?IA', lines[i + 1])

        if match:
            prob_ia = float(match.group(1))
            prob_humano = 100.0 - prob_ia

            comments.append({
                "llm": llm_sequence[llm_index],
                "comentario": comentario,
                "prob_humano": prob_humano,
                "prob_IA": prob_ia
            })

            if len(comments) % 6 == 0:
                llm_index = (llm_index + 1) % len(llm_sequence)

            i += 2  # Pula para o próximo comentário
        else:
            i += 1  # Se não encontrar um match, continua para a próxima linha

    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(comments, out_file, indent=4, ensure_ascii=False)


# Exemplo de uso
parse_file('apostas.txt', 'resultados_CasasDeApostas.json')