import os
from ollama import chat, ChatResponse


def interagir_com_modelo():
    # Mensagem inicial para o modelo
    prompt = "Oi, como você está? Responda em português, por favor."

    try:
        # Envia a requisição para o modelo "deepseek-r1:7b" com o prompt
        response: ChatResponse = chat(model='deepseek-coder-v2', messages=[
            {
                "role": "system",
                "content": "Você deve responder sempre em português, independentemente do idioma da pergunta."
            },
            {"role": "user", "content": prompt}
        ])

        # Verifica se a resposta existe e extrai somente o conteúdo da resposta (ignorando <think>)
        if response and 'message' in response:
            resposta = response['message']['content']
            # Filtra e retorna apenas a parte relevante da resposta
            resposta_filtrada = ''.join([linha for linha in resposta.split('\n') if not linha.startswith('<think>')])
            # Exibe apenas a resposta sem a parte de pensamento
            print("Resposta do modelo:", resposta_filtrada.strip().split("\n")[-1])
        else:
            print("Erro: Não foi possível gerar a resposta.")

    except Exception as erro:
        print(f"Erro na interação com o modelo: {erro}")


# Chama a função para interagir com o modelo
interagir_com_modelo()
