import os
from ollama import chat


# Função que recebe as informações e monta o prompt para o modelo
def gerar_comentarios(persona, post, tema):

    prompt = (
        f"Tema: {tema}\n"
        f"Post no Twitter: {post}\n\n"
        "Escreva um comentário curto e informal, como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível e não use aspas ao redor das frases."
    )

    try:
        # Envia o prompt para o modelo "deepseek-coder-v2"
        response = chat(model='deepseek-coder-v2', messages=[
            {
                "role": "system",
                "content": (
                    f"Você é {persona}. Seu papel é comentar postagens de forma breve, informal e natural. "
                    f"Adapte seu comentário ao estilo da persona, mantendo-o curto, como algo que seria dito por uma pessoa em uma conversa real."
                )
            },
            {"role": "user", "content": prompt}
        ])

        # Verifica se a resposta foi gerada corretamente
        if response and 'message' in response:
            comentario = response['message']['content'].strip()
            return comentario

    except Exception as erro:
        print(f"Erro ao interagir com o modelo: {erro}")

    return None


def gerar_comentarios_para_posts(personas_file, posts_file):

    if not personas_file or not posts_file:
        exit(1)

    save = []

    for i in range(len(posts_file["Posts"])):
        comentario = gerar_comentarios(personas_file["Persona"]["Descrição"], posts_file["Posts"][i]["Descrição"], personas_file["Persona"]["Tema"])

        if comentario:
            save.append(f"{comentario}\n")

    return save

