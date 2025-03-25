import os
import google.generativeai as genai

api_key = os.getenv('OPENAI_API_KEY')

def gerar_comentarios(persona, post, tema, stream=False):

    prompt = (
        f"Tema: {tema}\n"
        f"Você é {persona}. Seu papel é comentar postagens de forma breve, informal e natural."
        f"Escreva um comentário curto e informal sobre o post {post} como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível. "
        "Adapte seu comentário ao estilo da persona, mantendo-o curto, como algo que seria dito por uma pessoa em uma conversa real."
    )

    try:
        if not api_key:
            print("Erro: A chave da API não foi configurada corretamente.")
            exit(1)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt, stream=stream)

        if not stream:
            return response.text

        resultado = ""
        for chunk in response:
            resultado += chunk.text

        return resultado

    except Exception as erro:
        print(f"Não foi possível gerar o comentário: {erro}")
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


