import os
import json
import logging
import glob
from logging import exception
import Funcoes.Retornar_Estatisticas as res
import IAText_Detectors.Roberta as roberta
import IAText_Detectors.Sapling as sapling
import IAText_Detectors.Radar as radar
import IAText_Detectors.HuggingFace as huggingface
import IAText_Detectors.DistBERT as distbert
import LLMs.Cohere as cohereUnic
import LLMs.Llama as llamaUnic
import LLMs.ChatGPT as gptUnic
import LLMs.MaritacaIA as maritacaIAUnic
import LLMs.Gemini as geminiIAUnic
import LLMs.Mistral as mistralUnic
import LLMs.DeepSeek as deepseekUnic
import IAText_Detectors.Binoculars as binoc

from flask import Flask, render_template, request, send_file, session
from LLMs.Cohere import gerar_comentarios_para_posts as cohere
from LLMs.ChatGPT import gerar_comentarios_para_posts as chatGpt
from LLMs.Gemini import gerar_comentarios_para_posts as gemini
from LLMs.Llama import gerar_comentarios_para_posts as llama
from LLMs.MaritacaIA import gerar_comentarios_para_posts as maritaca
from LLMs.Mistral import gerar_comentarios_para_posts as mistral
from IAText_Detectors.Roberta import probabilidade_IA as roberta_prob
from IAText_Detectors.Sapling import probabilidade_IA as sapling_prob
from IAText_Detectors.HuggingFace import probabilidade_IA as prob_hugging
from IAText_Detectors.DistBERT import probabilidade_IA as distbert_prob
from IAText_Detectors.Radar import probabilidade_IA as radar_prob
from LLMs.DeepSeek import gerar_comentarios_para_posts as deepseek
import warnings

# Configuração de logging
logging.basicConfig(
    level=logging.ERROR,
    filename="app_errors.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

app.secret_key = os.urandom(24)

arqs_temp = "Arquivos_Temporarios_LLMs/"
arqs_temp2 = "Arquivos_Temporarios_Detect/"

if not os.path.exists(arqs_temp):
    os.makedirs(arqs_temp)

if not os.path.exists(arqs_temp2):
    os.makedirs(arqs_temp2)

#Carregar JSONs de tema e de personas após escolha do usuário
#Salva os jsons na sessão
@app.route("/load_json")
def load_json():
    arquivo = request.args.get("file")
    if not arquivo:
        return {"error": "Nenhum arquivo especificado"}, 400

    json_temas = os.path.join("JSONS/Temas", arquivo)
    json_personas = os.path.join("JSONS/Personas", arquivo)

    try:
        with open(json_temas, "r", encoding="utf-8") as f:
            tema_json = json.load(f)
    except FileNotFoundError:
        return {"error": "Arquivo de tema não encontrado"}, 404
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar o arquivo de tema"}, 400

    try:
        with open(json_personas, "r", encoding="utf-8") as f:
            persona_json = json.load(f)
    except FileNotFoundError:
        return {"error": "Arquivo de persona não encontrado"}, 404
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar o arquivo de persona"}, 400

    # Armazenar os dados na sessão
    session['tema_json'] = tema_json
    session['persona_json'] = persona_json

    return {
        "temas": tema_json,
        "personas": persona_json
    }, 200

# Rota principal para escolha do tema e LLM para geração dos comentários
@app.route("/gerarComentarios", methods=["GET", "POST"])
def home():
    comentarios = []
    indices = list(range(1, 7))  # Lista de índices [1, 2, 3, 4, 5, 6]

    # Remover arquivos temporários
    for arquivo in glob.glob(os.path.join('./Arquivos_Temporarios_LLMs', "*")):
        if os.path.isfile(arquivo):
            os.remove(arquivo)

    for arquivo in glob.glob(os.path.join('./Arquivos_Temporarios_Detect', "*")):
        if os.path.isfile(arquivo):
            os.remove(arquivo)

    if request.method == "POST":

        ai_choice = request.form.get("ai")

        if not ai_choice:
            return {"error": "Escolha de IA não especificada"}, 400

        tema_json = session.get('tema_json')
        persona_json = session.get('persona_json')

        if not tema_json or not persona_json:
            return {"error": "JSONs não carregados na sessão"}, 400

        # Mapeamento das funções das LLMs
        llm_functions = {
            "cohere": cohere,
            "chatGpt": chatGpt,
            "gemini": gemini,
            "llama": llama,
            "maritacaIA": maritaca,
            "mistral": mistral,
            "deepseek": deepseek
        }

        # Verifica se a IA escolhida é válida
        llm_function = llm_functions.get(ai_choice)
        if not llm_function:
            return {"error": "IA inválida especificada"}, 400

        try:
            comentarios = llm_function(persona_json, tema_json)
        except Exception as error:
            logging.error(f"Erro ao gerar comentarios ({ai_choice}): {error}")
            return {"error": f"Erro ao gerar comentários: {str(error)}"}, 500

        # Criação do arquivo de saída
        file_name = f"{ai_choice.capitalize()}_{tema_json['Tema']}.txt"
        file_path = os.path.join(arqs_temp, file_name)

        try:
            with open(file_path, 'w', encoding="utf-8") as f:
                f.writelines(comentario + "\n" for comentario in comentarios)
        except IOError as error:
            logging.error(f"Erro ao salvar o arquivo ({file_name}): {error}")
            return {"error": f"Erro ao salvar o arquivo: {str(error)}"}, 500

        return render_template("gerar_comentarios_llm.html", comentarios=comentarios, file_path=file_path, ind=indices, zip=zip, tema=tema_json['Tema'],posts=tema_json['Posts'],llm=ai_choice.capitalize())

    return render_template("gerar_comentarios_llm.html", comentarios=comentarios)

#Rota para baixar o arquivo após a geração dos comentários
@app.route("/download")
def download():
    file_path = request.args.get('file_path')
    if not file_path:
        return "Caminho do arquivo não especificado", 400

    if not os.path.exists(file_path):
        return "Arquivo não encontrado", 404

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as error:
        logging.error(f"Erro ao enviar o arquivo: {str(error)}")
        return f"Erro ao enviar o arquivo: {str(e)}", 500


#Rota para a página de resultados gerais sobre as LLMs e os detectores
@app.route("/estatisticas", methods=["GET", "POST"])
def estatisticas():

    llms = ['Cohere', 'ChatGPT', 'DeepSeek', 'Gemini', 'Llama', 'MaritacaIA', 'Mistral']
    dir_base = "./Resultados"

    resultados = res.calcular_estatisticas_tabela(llms,dir_base)
    resultados_graficos = res.calcular_acerto_por_llm(resultados)
    resultados_barras = res.calcular_acerto_por_detector(resultados)
    resultados_detector_tema = res.calcular_detector_tema(resultados)
    resultados_llm_tema = res.calcular_media_prob_humano_por_tema(resultados)

    return render_template("estatisticas.html", resultados=resultados, resultados_graficos=resultados_graficos,resultados_barras=resultados_barras,
                           resultados_detector_tema=resultados_detector_tema,resultados_llm_tema=resultados_llm_tema)

@app.route("/analisarAutenticidadeGeral", methods=["GET", "POST"])
def analisarAutenticidadeGeral():
    if request.method == "POST":
        ai_choice = request.form.get("ai")
        theme_choice = request.form.get("themes")
        lista_llms = ['Cohere', 'ChatGPT', 'DeepSeek', 'Gemini', 'Llama', 'MaritacaIA', 'Mistral']
        processed_data = []
        file_path = ""

        # Mapeamento dos detectores para suas funções correspondentes
        ai_map = {
            "roberta": roberta_prob,
            "sapling": sapling_prob,
            "huggingface": prob_hugging,
            "distbert": distbert_prob,
            "radar": radar_prob,
            #"binoculars": binoc
        }

        if ai_choice in ai_map:
            # Carregar comentários
            lista_comentarios = [
                {"llm": llm, "comentarios": open(f"Comentarios_Gerados_PrimeiraEtapa/{llm}_{theme_choice[:-5]}.txt", "r", encoding="utf-8").read()}
                for llm in lista_llms
            ]

            # Processar os comentários com o detector escolhido
            resultados = ai_map[ai_choice](lista_comentarios, lista_llms)

            # Estruturar os dados para o JSON
            processed_data = [
                {
                    "llm": item["llm"],
                    "comentario": item["comentario"],
                    "detector": ai_choice.capitalize(),
                    "prob_humano": item["prob_humano"],
                    "prob_IA": item["prob_IA"],
                }
                for item in resultados
            ]

            file_path = f"Arquivos_Temporarios_Detect/resultados_{theme_choice}"

            try:
                with open(file_path, 'w', encoding="utf-8") as f:
                    json.dump(processed_data, f, ensure_ascii=False, indent=4)  # Salva como JSON formatado
            except IOError as error:
                logging.error(f"Erro ao salvar o arquivo ({file_path}): {error}")
                response = {"error": f"Erro ao salvar o arquivo: {str(error)}"}, 500

        return render_template("analisar_comentarios_gerais.html", msg="true", resultados=processed_data, file_path=file_path)

    return render_template("analisar_comentarios_gerais.html")


@app.route("/gerarComentario", methods=["GET", "POST"])
def gerarComentario():
    arquivo = "JSONS/Personas_Para_Comentarios_Personalizados/personas.json"

    personas = []

    # Função auxiliar para carregar personas do JSON
    def carregar_personas():
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data.get("Personas"), list):
                    return [
                        {
                            "Tema": p.get("Tema"),
                            "Nome": p.get("Nome"),
                            "Descrição": p.get("Descrição")
                        }
                        for p in data["Personas"]
                        if all(k in p for k in ["Tema", "Nome", "Descrição"])
                    ]
                print("'Personas' não encontrada ou não é uma lista.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar JSON: {e}")
        return []

    personas = carregar_personas()

    print(personas)

    if request.method == "POST":
        ai_choice = request.form.get("ai")
        tema = request.form.get("tema")
        persona = request.form.get("persona")
        post = request.form.get("post")
        full_comments = []

        ai_map = {
            "cohere": cohereUnic,
            "chatgpt": gptUnic,
            "gemini": geminiIAUnic,
            "llama": llamaUnic,
            #Desativado devido ao modelo não estar baixado
            #"deepseek": deepseekUnic,
            "maritacaIA": maritacaIAUnic,
            "mistral": mistralUnic
        }

        if not ai_choice:
            for llm in ai_map:
                comment = ai_map[llm].gerar_comentarios(persona, post, tema)
                probIA = roberta.probabilidade_frase_unica(comment)
                full_comments.append({"llm": llm.capitalize(), "comentario": comment, "probIA":  probIA["prob_IA"]})

            return render_template(
                "gerar_comentario_personalizado.html",
                full_comments=full_comments,
                tema=tema,
                post=post,
                personas=personas,
                zip=zip
            )


        if ai_choice in ai_map:
            resposta = ai_map[ai_choice].gerar_comentarios(persona, post, tema)
            prob_IA = roberta.probabilidade_frase_unica(resposta)

            return render_template(
                "gerar_comentario_personalizado.html",
                comentario=resposta,
                tema=tema,
                llm=ai_choice.capitalize(),
                post=post,
                personas=personas,
                probIA = prob_IA["prob_IA"]
            )

    return render_template("gerar_comentario_personalizado.html", personas=personas)



@app.route("/analisarAutenticidade", methods=["GET", "POST"])
def analisar_comentario():
    if request.method == "POST":
        ai_choice = request.form.get("ai")
        comentario = request.form["comentario"]

        # Dicionário mapeando cada IA ao seu respectivo método
        ai_map = {
            "roberta": roberta.probabilidade_frase_unica,
            "sapling": sapling.probabilidade_frase_unica,
            "radar": radar.probabilidade_frase_unica,
            "huggingface": huggingface.probabilidade_frase_unica,
            "distbert": distbert.probabilidade_IA_frase,
            #"binoculars": binoc.probabilidade_IA_frase
        }

        if ai_choice in ai_map:
            resposta = ai_map[ai_choice](comentario)
            return render_template("analisar_comentario_personalizado.html", resposta=resposta, llm=ai_choice.capitalize())

    return render_template("analisar_comentario_personalizado.html")

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        return render_template("index.html")

    except Exception as error:
       logging.error(f"{error}")


def calcular_media_acerto_erro(dados):
    total_acerto = 0
    total_erro = 0
    total_comentarios = len(dados)

    for item in dados:
        total_acerto += item['prob_humano']
        total_erro += item['prob_IA']

    media_acerto = total_acerto / total_comentarios if total_comentarios else 0
    media_erro = total_erro / total_comentarios if total_comentarios else 0

    return media_acerto, media_erro

@app.route("/gerarEstatisticasPersonalizadas", methods=["GET", "POST"])
def gerarEstatisticasPersonalizadas():

    probabilidades = []

    if request.method == "GET":
        return render_template("estatisticas_personalizadas.html")  # Renderiza a página quando acessada via GET

    if request.method == "POST":

        detector_map = {
            "roberta": roberta,
            "radar": radar,
            "sapling": sapling,
            "huggingface": huggingface,
            #"binoculars": binoc
            "distbert": distbert,
        }

        comentarios = []
        file = request.files["txtFile"]
        conteudo = file.read().decode("utf-8")
        results = []

        linhas_nao_vazias = [linha.strip() for linha in conteudo.splitlines() if linha.strip()]

        for linha in linhas_nao_vazias:
            comentarios.append(linha)

        for chave, funcao in detector_map.items():
            results.append([{"detector": str(chave) , "Probabilidades": funcao.probabilidade_IA_comentarios_proprios(comentarios)}])
            print(results)
            
        probabilidades = res.calcular_comentarios_proprios(results)

        return render_template("estatisticas_personalizadas.html", probabilidades=probabilidades)

    return render_template("estatisticas_personalizadas.html", probabilidades=probabilidades)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor Flask: {str(e)}")