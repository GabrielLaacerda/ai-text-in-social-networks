import os
from ollama import chat
from ollama import ChatResponse

# Função para gerar comentários
def gerar_comentarios(persona, post, tema, stream=False):
    prompt = (
        f"Tema: {tema}\n"
        f"Post no Twitter: {post}\n\n"
        "Escreva um comentário curto e informal, como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível."
    )

    try:
        # Enviar requisição para o modelo Llama 3.2 usando Ollama
        response: ChatResponse = chat(model='llama3.2', messages=[
            {
                "role": "system",
                "content": (
                    f"Você é {persona}. Seu papel é comentar postagens de forma breve, informal e natural. "
                    f"Adapte seu comentário ao estilo da persona, mantendo-o curto, como algo que seria dito por uma pessoa em uma conversa real."
                )
            },
            {"role": "user", "content": prompt}])

        if response and 'message' in response:
            # Retorna a resposta do modelo
            return response['message']['content']
        else:
            print("Erro: Não foi possível gerar a resposta.")
            return None

    except Exception as erro:
        print(f"Não foi possível gerar o comentário: {erro}")
        return None


# Função para gerar comentários para posts a partir de arquivos
def gerar_comentarios_para_posts(personas_file, posts_file):

    if not personas_file or not posts_file:
        exit(1)

    save = []

    for i in range(len(posts_file["Posts"])):
        comentario = gerar_comentarios(personas_file["Persona"]["Descrição"], posts_file["Posts"][i]["Descrição"],
                                       personas_file["Persona"]["Tema"])

        if comentario:
            save.append(f"{comentario}\n")

    return save