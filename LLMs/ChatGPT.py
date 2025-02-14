import openai
import os
import time

#Autenticação da API
openai.api_key = os.getenv("GPT_API_KEY")

#Função que recebe as informações para montar o prompt que será enviado via API para a LLM
def gerar_comentarios(persona, post, tema):

    #Prompt a ser enviado
    prompt = (
        f"Tema: {tema}\n"
        f"Post no Twitter: {post}\n\n"
        "Escreva um comentário curto e informal, como se fosse algo que uma pessoa diria espontaneamente em uma conversa ou tweet. "
        "Mantenha um tom autêntico, sem explicações longas ou formalidade. Use linguagem cotidiana para parecer o mais humano possível."
    )

    try:

        #Envia o promp para o model especifico e retorna a resposta
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
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
        return completion['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        return None


# Recebe a persona e os posts do twitter que servirão de base na geração
def gerar_comentarios_para_posts(personas_file, posts_file):

    if not personas_file or not posts_file:
        exit(1)

    print(f'Comentários:\n\n')
    save = []

    limite_requisicoes_por_minuto = 3
    requisicoes_realizadas = 0

    #Passa as informações para a função gerar_comentarios, responsável pela geração
    for i in range(len(posts_file["Posts"])):
        if requisicoes_realizadas >= limite_requisicoes_por_minuto:
            print(f"Limite de requisições atingido. Aguardando...")
            time.sleep(60)  # Aguardar 60 segundos (ajuste conforme o limite da API)
            requisicoes_realizadas = 0  # Reseta a contagem de requisições

        try:
            comentario = gerar_comentarios(personas_file["Persona"]["Descrição"], posts_file["Posts"][i]["Descrição"],
                                           personas_file["Persona"]["Descrição"])

            if comentario:
                print(f"[{i+1}]: {comentario}\n\n")

                #Após cada retorno de comentário, este é adicionado a lista (save)
                save.append(f"{comentario}\n")

            requisicoes_realizadas += 1
            time.sleep(5)  # Aguardar um intervalo entre as requisições

        except Exception as e:
            print(f"Erro ao gerar comentário para o post {i}: {e}")
            time.sleep(10)

    #Retorna os comentários gerados
    return save
