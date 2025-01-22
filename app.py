import os
import json
from flask import Flask, render_template, request, send_file, session
from LLMs.Cohere import gerar_comentarios_para_posts as cohere
from LLMs.ChatGPT import gerar_comentarios_para_posts as chatGpt
from LLMs.Gemini import gerar_comentarios_para_posts as gemini
from LLMs.Llama import gerar_comentarios_para_posts as llama
from LLMs.MaritacaIA import gerar_comentarios_para_posts as maritaca

app = Flask(__name__)

tema_json = None
persona_json = None
file_path = None

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

    if os.path.exists(file_path_temas) and os.path.exists(file_path_persona):
        with open(file_path_temas, "r") as f:
            tema_json = json.load(f)

        with open(file_path_persona, "r") as f:
            persona_json = json.load(f)

        # Armazenar os dados na sessão
        session['tema_json'] = tema_json
        session['persona_json'] = persona_json

        return {
            "temas": tema_json,
            "personas": persona_json
        }, 200

    return {"error": "Arquivo não encontrado"}, 404

@app.route("/", methods=["GET", "POST"])
def home():
    comentarios = []

    if request.method == "POST":
        ai_choice = request.form["ai"]
        tema_json = session.get('tema_json')
        persona_json = session.get('persona_json')

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

        # Definindo o caminho do arquivo no novo diretório
        file_name = f"{ai_choice.capitalize()}_{tema_json['Tema']}.txt"
        file_path = os.path.join(output_directory, file_name)

        with open(file_path, 'w') as f:
            for comentario in comentarios:
                f.write(comentario + "\n")

        return render_template("index.html", comentarios=comentarios, file_path=file_path)

    return render_template("index.html", comentarios=comentarios)

@app.route("/download")
def download():
    file_path = request.args.get('file_path')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Arquivo não encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)
