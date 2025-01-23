import os
import cohere

API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.ClientV2(api_key=os.getenv('COHERE_API_KEY'))

def gerar_comentarios(persona, post, tema):

    prompt = (
        f"Tema: {tema}\n"
        f"Post no Twitter: {post}\n\n"
        "Escreva um comentário curto e informal, como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível e não use aspas ao redor das frases."
    )

    res = co.chat(
        model="command-r-plus-04-2024",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Você é {persona}. Seu papel é comentar postagens de forma breve, informal e natural. "
                    f"Adapte seu comentário ao estilo da persona, mantendo-o curto, como algo que seria dito por uma pessoa em uma conversa real."
                )
            },
            {"role": "user", "content": prompt}
        ],
    )

    # Remover quebras de linha e garantir uma resposta mais direta
    comentario = res.message.content[0].text.replace("\n", " ").strip()
    return comentario

def gerar_comentarios_para_posts(personas_file, posts_file):

    if not personas_file or not posts_file:
        exit(1)

    print(f'Comentários:\n\n')
    save = []

    for i in range(len(posts_file["Posts"])):
        comentario = gerar_comentarios(personas_file["Persona"]["Descrição"], posts_file["Posts"][i]["Descrição"], personas_file["Persona"]["Descrição"])

        if comentario:
            print(f"[{i + 1}]: {comentario}\n")
            save.append(f"{comentario}\n")

    return save
