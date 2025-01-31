import json
import re


def parse_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Expressão regular para capturar os comentários, percentual de IA e LLM
    pattern = re.compile(r'("?.+?"?)\n(\d+)%IA\n(\w+)')
    matches = pattern.findall(content)

    data = []
    for comment, prob_ia, llm in matches:
        prob_ia = float(prob_ia)
        prob_humano = round(100 - prob_ia, 2)

        data.append({
            "llm": llm,
            "comentario": comment,
            "prob_humano": prob_humano,
            "prob_IA": prob_ia
        })

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Arquivo JSON '{output_file}' gerado com sucesso!")


parse_file('teste.txt', 'resultados_Streaming.json')
