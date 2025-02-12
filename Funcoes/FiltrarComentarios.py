import pandas as pd
import re

df = pd.read_excel('./Comentarios_Originais_Twitter/Comentarios_InteligenciaArtificial.xlsx')

# Filtrar as linhas onde a primeira coluna contém o link específico
link = 'https://x.com/oatila/status/1264001512944132099'
df_filtrado = df[df.iloc[:, 0] == link]

# Extrair o texto da coluna N (índice 13)
coluna_n_textos = df_filtrado.iloc[:, 13].tolist()

# Remover o @usuario no começo de cada texto
texto_sem_usuario = [re.sub(r"^@\w+\s*", "", texto) for texto in coluna_n_textos]

# Armazenar os textos processados na variável
texto_variavel = "\n".join(texto_sem_usuario)

# Salvar o conteúdo com uma linha em branco entre os comentários
with open('/home/gabriel/TCC_GabrielVncs/Comentarios_Originais_Twitter/InteligenciaArtificial.txt', 'w', encoding='utf-8') as f:
    for comentario in texto_sem_usuario:
        f.write(comentario + "\n\n")  # Adiciona uma linha em branco após cada comentário

print("Comentários salvos em 'comentarios_com_linhas_vazias.txt'")


