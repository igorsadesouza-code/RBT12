import os
import uuid
import zipfile
import shutil

from flask import Flask, render_template, request, send_file, flash, redirect, url_for

from processamento_modo1 import gerar_txt_modo1
from processamento_modo2 import gerar_txt_modo2
from processamento_renomear import renomear_arquivos


app = Flask(__name__)

# Chave usada pelo Flask para mensagens flash.
# Depois podemos trocar por variável de ambiente.
app.secret_key = "troque-essa-chave-secreta"

# Limite de upload: 200 MB
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# PÁGINA PRINCIPAL
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# GERAR TXT
# =========================================================

@app.route("/gerar-txt", methods=["POST"])
def gerar_txt():
    modo = request.form.get("modo", "2")
    arquivos = request.files.getlist("pdfs")

    if not arquivos or arquivos[0].filename == "":
        flash("Selecione pelo menos um arquivo PDF.")
        return redirect(url_for("index"))

    id_execucao = str(uuid.uuid4())
    pasta_trabalho = os.path.join(UPLOAD_FOLDER, id_execucao)

    os.makedirs(pasta_trabalho, exist_ok=True)

    caminho_zip = os.path.join(UPLOAD_FOLDER, f"{id_execucao}.zip")

    try:
        # Salva PDFs enviados na pasta temporária
        total_salvos = 0

        for arquivo in arquivos:
            if arquivo and arquivo.filename.lower().endswith(".pdf"):
                caminho_pdf = os.path.join(pasta_trabalho, arquivo.filename)
                arquivo.save(caminho_pdf)
                total_salvos += 1

        if total_salvos == 0:
            flash("Nenhum arquivo PDF válido foi enviado.")
            return redirect(url_for("index"))

        # Processa conforme o modo selecionado
        if modo == "1":
            resultado = gerar_txt_modo1(pasta_trabalho)
            caminho_txt = resultado["caminho_txt"]

            with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                if caminho_txt and os.path.exists(caminho_txt):
                    zipf.write(caminho_txt, os.path.basename(caminho_txt))

        else:
            resultado = gerar_txt_modo2(pasta_trabalho)

            with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                caminho_receita = resultado.get("caminho_receita")
                caminho_folha = resultado.get("caminho_folha")

                if caminho_receita and os.path.exists(caminho_receita):
                    zipf.write(caminho_receita, os.path.basename(caminho_receita))

                if caminho_folha and os.path.exists(caminho_folha):
                    zipf.write(caminho_folha, os.path.basename(caminho_folha))

        return send_file(
            caminho_zip,
            as_attachment=True,
            download_name="arquivos_gerados.zip"
        )

    except Exception as e:
        flash(f"Erro ao processar os PDFs: {str(e)}")
        return redirect(url_for("index"))

    finally:
        if os.path.exists(pasta_trabalho):
            shutil.rmtree(pasta_trabalho, ignore_errors=True)


# =========================================================
# RENOMEAR ARQUIVOS
# =========================================================

@app.route("/renomear", methods=["POST"])
def renomear():
    excel = request.files.get("excel")
    pdfs = request.files.getlist("pdfs_renomear")

    if not excel or excel.filename == "":
        flash("Selecione a planilha Excel.")
        return redirect(url_for("index"))

    if not pdfs or pdfs[0].filename == "":
        flash("Selecione pelo menos um PDF para renomear.")
        return redirect(url_for("index"))

    extensao_excel = os.path.splitext(excel.filename)[1].lower()

    if extensao_excel not in [".xls", ".xlsx"]:
        flash("Formato de planilha inválido. Use .xls ou .xlsx.")
        return redirect(url_for("index"))

    id_execucao = str(uuid.uuid4())

    pasta_trabalho = os.path.join(UPLOAD_FOLDER, id_execucao)
    pasta_pdfs = os.path.join(pasta_trabalho, "pdfs")

    os.makedirs(pasta_pdfs, exist_ok=True)

    caminho_zip = os.path.join(UPLOAD_FOLDER, f"{id_execucao}_renomeados.zip")

    try:
        # Salva Excel
        caminho_excel = os.path.join(pasta_trabalho, excel.filename)
        excel.save(caminho_excel)

        # Salva PDFs
        total_pdfs_salvos = 0

        for arquivo in pdfs:
            if arquivo and arquivo.filename.lower().endswith(".pdf"):
                caminho_pdf = os.path.join(pasta_pdfs, arquivo.filename)
                arquivo.save(caminho_pdf)
                total_pdfs_salvos += 1

        if total_pdfs_salvos == 0:
            flash("Nenhum arquivo PDF válido foi enviado para renomeação.")
            return redirect(url_for("index"))

        # Executa sua função existente
        resultado = renomear_arquivos(caminho_excel, pasta_pdfs)

        pasta_destino = resultado["pasta_destino"]

        if not os.path.exists(pasta_destino):
            flash("A pasta de arquivos renomeados não foi criada.")
            return redirect(url_for("index"))

        # Compacta os PDFs renomeados
        with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for nome_arquivo in os.listdir(pasta_destino):
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

                if os.path.isfile(caminho_arquivo):
                    zipf.write(caminho_arquivo, nome_arquivo)

        return send_file(
            caminho_zip,
            as_attachment=True,
            download_name="arquivos_renomeados.zip"
        )

    except Exception as e:
        flash(f"Erro ao renomear arquivos: {str(e)}")
        return redirect(url_for("index"))

    finally:
        if os.path.exists(pasta_trabalho):
            shutil.rmtree(pasta_trabalho, ignore_errors=True)


# =========================================================
# EXECUÇÃO LOCAL
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)