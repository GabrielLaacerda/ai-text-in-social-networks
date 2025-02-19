import os
from mistralai import Mistral
import time

api_key = os.getenv("MISTRAL_API_KEY")

def gerar_comentarios(persona, post, tema):

    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)

    prompt = (
        f"Tema: {tema}\n"
        f"Post no Twitter: {post}\n\n"
        "Escreva um comentário curto e informal, como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível."
        "Não repita respostas"
    )

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    f"Você é {persona}. Seu papel é comentar postagens de forma breve, informal e natural. "
                    f"Adapte seu comentário ao estilo da persona, mantendo-o curto, como algo que seria dito por uma pessoa em uma conversa real."
                )
            },
            {"role": "user", "content": prompt}
        ]
    )


    return chat_response.choices[0].message.content


def gerar_comentarios_para_posts(personas_file, posts_file):

    if not personas_file or not posts_file:
        exit(1)

    save = []

    limite_requisicoes_por_minuto = 3
    requisicoes_realizadas = 0

    for i in range(len(posts_file["Posts"])):  # Vai de 0 até 4
        if requisicoes_realizadas >= limite_requisicoes_por_minuto:
            print(f"Limite de requisições atingido. Aguardando...")
            time.sleep(60)  # Aguardar 60 segundos (ajuste conforme o limite da API)
            requisicoes_realizadas = 0  # Reseta a contagem de requisições

        try:
            comentario = gerar_comentarios(personas_file["Persona"]["Descrição"], posts_file["Posts"][i]["Descrição"],
                                           personas_file["Persona"]["Tema"])

            if comentario:
                save.append(f"{comentario}\n")

            requisicoes_realizadas += 1
            time.sleep(5)  # Aguardar um intervalo entre as requisições

        except Exception as e:
            print(f"Erro ao gerar comentário para o post {i}: {e}")
            time.sleep(10)

    return save


