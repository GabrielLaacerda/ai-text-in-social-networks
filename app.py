import os
import json
import logging
from flask import Flask, render_template, request, send_file, session
from LLMs.Cohere import gerar_comentarios_para_posts as cohere
from LLMs.ChatGPT import gerar_comentarios_para_posts as chatGpt
from LLMs.Gemini import gerar_comentarios_para_posts as gemini
from LLMs.Llama import gerar_comentarios_para_posts as llama
from LLMs.MaritacaIA import gerar_comentarios_para_posts as maritaca
from LLMs.Mistral import gerar_comentarios_para_posts as mistral

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

        return render_template("index.html", comentarios=comentarios, file_path=file_path)

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

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor Flask: {str(e)}")