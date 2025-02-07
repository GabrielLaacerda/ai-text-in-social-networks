import os
import json
import logging
import glob
import Funcoes.Retornar_Estatisticas as re
from flask import Flask, render_template, request, send_file, session, jsonify
from LLMs.Cohere import gerar_comentarios_para_posts as cohere
from LLMs.ChatGPT import gerar_comentarios_para_posts as chatGpt
from LLMs.Gemini import gerar_comentarios_para_posts as gemini
from LLMs.Llama import gerar_comentarios_para_posts as llama
from LLMs.MaritacaIA import gerar_comentarios_para_posts as maritaca
from LLMs.Mistral import gerar_comentarios_para_posts as mistral
from IAText_Detectors.Roberta import probabilidade_IA as roberta_prob
from IAText_Detectors.Sapling import probabilidade_IA as sapling_prob
from IAText_Detectors.huggingface import probabilidade_IA as prob_hugging
from IAText_Detectors.BERT import probabilidade_IA as bert_prob
from IAText_Detectors.Radar import probabilidade_IA as radar_prob


# Configuração de logging
logging.basicConfig(
    level=logging.ERROR,
    filename="app_errors.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

app.secret_key = os.urandom(24)

# Diretório de saída
output_directory = "Arquivos_Temporarios/"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

@app.route("/load_json")
def load_json():
    file_name = request.args.get("file")
    if not file_name:
        return {"error": "Nenhum arquivo especificado"}, 400

    file_path_temas = os.path.join("JSONS/Temas", file_name)
    file_path_persona = os.path.join("JSONS/Personas", file_name)

    try:
        with open(file_path_temas, "r") as f:
            tema_json = json.load(f)
    except FileNotFoundError:
        return {"error": "Arquivo de tema não encontrado"}, 404
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar o arquivo de tema"}, 400

    try:
        with open(file_path_persona, "r") as f:
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

@app.route("/", methods=["GET", "POST"])
def home():
    comentarios = []
    indices = [1,2,3,4,5,6]

    for arquivo in glob.glob(os.path.join('./Arquivos_Temporarios', "*")):
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

        try:
            if ai_choice == "cohere":
                comentarios = cohere(persona_json, tema_json)
            elif ai_choice == "chatgpt":
                comentarios = chatGpt(persona_json, tema_json)
            elif ai_choice == "gemini":
                comentarios = gemini(persona_json, tema_json)
            elif ai_choice == "llama":
                comentarios = llama(persona_json, tema_json)
            elif ai_choice == "maritacaIA":
                comentarios = maritaca(persona_json, tema_json)
            elif ai_choice == "mistral":
                comentarios = mistral(persona_json, tema_json)
            else:
                return {"error": "IA inválida especificada"}, 400
        except Exception as e:
            logging.error(f"Erro ao gerar comentários: {str(e)}")
            return {"error": f"Erro ao gerar comentários: {str(e)}"}, 500

        # Definindo o caminho do arquivo no novo diretório
        file_name = f"{ai_choice.capitalize()}_{tema_json['Tema']}.txt"
        file_path = os.path.join(output_directory, file_name)

        try:
            with open(file_path, 'w') as f:
                for comentario in comentarios:
                    f.write(comentario + "\n")
        except IOError as e:
            logging.error(f"Erro ao salvar o arquivo: {str(e)}")
            return {"error": f"Erro ao salvar o arquivo: {str(e)}"}, 500

        return render_template("index.html", comentarios=comentarios, file_path=file_path, ind=indices, zip=zip, tema = tema_json['Tema'])

    return render_template("index.html", comentarios=comentarios)

@app.route("/download")
def download():
    file_path = request.args.get('file_path')
    if not file_path:
        return "Caminho do arquivo não especificado", 400

    if not os.path.exists(file_path):
        return "Arquivo não encontrado", 404

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Erro ao enviar o arquivo: {str(e)}")
        return f"Erro ao enviar o arquivo: {str(e)}", 500



@app.route("/estatisticas", methods=["GET", "POST"])
def estatisticas():

    llms = ['Cohere', 'ChatGPT', 'Gemini', 'Llama', 'MaritacaIA', 'Mistral']
    dir_base = "./Resultados"
    resultados = re.calcular_estatisticas_tabela(llms,dir_base)
    resultados_graficos = re.calcular_acerto_por_llm(resultados)
    resultados_barras = re.calcular_acerto_por_detector(resultados)

    return render_template("estatisticas.html", resultados=resultados, resultados_graficos=resultados_graficos,resultados_barras=resultados_barras)


@app.route("/testar_llms", methods=["GET", "POST"])
def testar_llms():
    if request.method== 'POST':
        ai_choice = request.form.get('ai')
        lista_llms = ['Cohere', 'ChatGPT', 'Gemini', 'Llama', 'MaritacaIA', 'Mistral']

        if ai_choice == "roberta":
            theme_choice = request.form.get('themes')
            lista_comentarios = []

            for llm in lista_llms:
                with open(f"Comentarios_Gerados_SegundaEtapa/{llm}_{theme_choice[:-5]}.txt", 'r', encoding='utf-8') as file:
                    content = file.read()
                    lista_comentarios.append({'llm': llm, 'comentarios': content})

            result_roberta = roberta_prob(lista_comentarios, lista_llms)

            processed_data = [
                {
                    'llm': item['llm'],
                    'comentario': item['comentario'],
                    'prob_humano': item['prob_humano'],
                    'prob_IA': item['prob_IA']
                }
                for item in result_roberta
            ]

            with open(f"Resultados/Resultados_Roberta/resultados_{theme_choice[:-5]}.json", 'w', encoding='utf-8') as json_file:
                json.dump(processed_data, json_file, ensure_ascii=False, indent=4)


            return jsonify({"success": True, "message": "Arquivo gerado com sucesso!"})

        elif ai_choice == "sapling":
            theme_choice = request.form.get('themes')
            lista_comentarios = []

            for llm in lista_llms:
                with open(f"Comentarios_Gerados_SegundaEtapa/{llm}_{theme_choice[:-5]}.txt", 'r', encoding='utf-8') as file:
                    content = file.read()
                    lista_comentarios.append({'llm': llm, 'comentarios': content})

            result_sapling = sapling_prob(lista_comentarios, lista_llms)

            processed_data_sap = [
                {
                    'llm': item['llm'],
                    'comentario': item['comentario'],
                    'prob_humano': item['prob_humano'],
                    'prob_IA': item['prob_IA']
                }
                for item in result_sapling
            ]

            # Salvar os resultados em um arquivo JSON
            with open(f"Resultados/Resultados_Sapling/resultados_{theme_choice[:-5]}.json", 'w', encoding='utf-8') as json_file:
                json.dump(processed_data_sap, json_file, ensure_ascii=False, indent=4)

            # Retornar uma resposta JSON indicando sucesso
            return jsonify({"success": True, "message": "Arquivo gerado com sucesso!"})

        elif ai_choice == "huggingface":
            theme_choice = request.form.get('themes')
            lista_comentarios = []

            for llm in lista_llms:
                with open(f"Comentarios_Gerados_SegundaEtapa/{llm}_{theme_choice[:-5]}.txt", 'r',
                          encoding='utf-8') as file:
                    content = file.read()
                    lista_comentarios.append({'llm': llm, 'comentarios': content})

            print(lista_comentarios)
            print(lista_llms)
            result_hugging = prob_hugging(lista_comentarios, lista_llms)


            processed_data_sap = [
                {
                    'llm': item['llm'],
                    'comentario': item['comentario'],
                    'prob_humano': item['prob_humano'],
                    'prob_IA': item['prob_IA']
                }
                for item in result_hugging
            ]

            # Salvar os resultados em um arquivo JSON
            with open(f"Resultados/Resultados_HuggingFace/resultados_{theme_choice[:-5]}.json", 'w', encoding='utf-8') as json_file:
                json.dump(processed_data_sap, json_file, ensure_ascii=False, indent=4)

            # Retornar uma resposta JSON indicando sucesso
            return jsonify({"success": True, "message": "Arquivo gerado com sucesso!"})

        elif ai_choice == "bert":

            theme_choice = request.form.get('themes')
            lista_comentarios = []

            for llm in lista_llms:
                with open(f"Comentarios_Gerados_SegundaEtapa/{llm}_{theme_choice[:-5]}.txt", 'r',
                          encoding='utf-8') as file:
                    content = file.read()
                    lista_comentarios.append({'llm': llm, 'comentarios': content})

            result_bert = bert_prob(lista_comentarios, lista_llms)

            processed_data_sap = [
                {
                    'llm': item['llm'],
                    'comentario': item['comentario'],
                    'prob_humano': item['prob_humano'],
                    'prob_IA': item['prob_IA']
                }
                for item in result_bert
            ]

            # Salvar os resultados em um arquivo JSON
            with open(f"Resultados/Resultados_BERT/resultados_{theme_choice[:-5]}.json", 'w', encoding='utf-8') as json_file:
                json.dump(processed_data_sap, json_file, ensure_ascii=False, indent=4)

            # Retornar uma resposta JSON indicando sucesso
            return jsonify({"success": True, "message": "Arquivo gerado com sucesso!"})

        elif ai_choice == "radar":

            theme_choice = request.form.get('themes')
            lista_comentarios = []

            for llm in lista_llms:
                with open(f"Comentarios_Gerados_SegundaEtapa/{llm}_{theme_choice[:-5]}.txt", 'r',
                          encoding='utf-8') as file:
                    content = file.read()
                    lista_comentarios.append({'llm': llm, 'comentarios': content})

            result_radar = radar_prob(lista_comentarios, lista_llms)

            processed_data_sap = [
                {
                    'llm': item['llm'],
                    'comentario': item['comentario'],
                    'prob_humano': item['prob_humano'],
                    'prob_IA': item['prob_IA']
                }
                for item in result_radar
            ]

            # Salvar os resultados em um arquivo JSON
            with open(f"Resultados/Resultados_Radar/resultados_{theme_choice[:-5]}.json", 'w', encoding='utf-8') as json_file:
                json.dump(processed_data_sap, json_file, ensure_ascii=False, indent=4)

            # Retornar uma resposta JSON indicando sucesso
            return jsonify({"success": True, "message": "Arquivo gerado com sucesso!"})

        # Se nenhuma das condições foi atendida, retornar erro
        return jsonify({"success": False, "message": "Erro ao processar."})

    # Se for um GET, retorna o template
    return render_template("testar_llms.html")


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor Flask: {str(e)}")