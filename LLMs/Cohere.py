import os
import cohere

#Autenticação da API
api_key = os.getenv('COHERE_API_KEY')
co = cohere.ClientV2(api_key=api_key)

#Função que recebe as informações para montar o prompt que será enviado via API para a LLM
def gerar_comentarios(persona, post, tema):

    prompt = (
        f"Tema: {tema}\n"
        f"Post no Twitter: {post}\n\n"
        "Escreva um comentário curto e informal, como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível e não use aspas ao redor das frases."
    )

    # Envia o promp para o model especifico e retorna a resposta
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

# Recebe a persona e os posts do twitter que servirão de base na geração
def gerar_comentarios_para_posts(personas_file, posts_file):

    if not personas_file or not posts_file:
        exit(1)

    save = []

    # Passa as informações para a função gerar_comentarios, responsável pela geração
    for i in range(len(posts_file["Posts"])):
        comentario = gerar_comentarios(personas_file["Persona"]["Descrição"], posts_file["Posts"][i]["Descrição"], personas_file["Persona"]["Descrição"])

        if comentario:
            save.append(f"{comentario}\n")

    # Retorna os comentários gerados
    return save
