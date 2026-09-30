import os
import re
import glob

from utils import ler_texto_pdf, valor_br_para_texto, nome_mes_para_data, montar_linha_txt
from config import ARQUIVO_RECEITA


# =========================================================
# EXTRAÇÃO DE DADOS DO PDF (MODO 1)
# =========================================================

def extrair_dados_pdf(caminho_pdf):
    """
    Lê o PDF e extrai linhas no formato:
    Maio/2025 9.260,00
    Junho/2025 19.969,00
    """
    texto_completo = ler_texto_pdf(caminho_pdf)

    padrao = re.compile(
        r"(Janeiro|Fevereiro|Março|Marco|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro)/(\d{4})\s+([\d\.\,]+)",
        re.IGNORECASE
    )

    dados = []

    for match in padrao.finditer(texto_completo):
        mes = match.group(1)
        ano = match.group(2)
        valor_br = match.group(3)

        mes_ano = f"{mes}/{ano}"
        data = nome_mes_para_data(mes_ano)
        valor = valor_br_para_texto(valor_br)

        dados.append({
            "data": data,
            "valor": valor
        })

    return dados


# =========================================================
# GERAÇÃO DO TXT (MODO 1)
# =========================================================

def gerar_txt_modo1(pasta_pdf, atualizar_status=None, atualizar_progresso=None):
    """
    Gera um TXT único com os dados de todos os PDFs simples da pasta escolhida.
    """
    arquivos_pdf = glob.glob(os.path.join(pasta_pdf, "*.pdf"))

    if not arquivos_pdf:
        raise FileNotFoundError("Nenhum arquivo PDF foi encontrado na pasta selecionada.")

    caminho_txt = os.path.join(pasta_pdf, ARQUIVO_RECEITA)

    total_linhas = 0
    arquivos_processados = 0
    arquivos_sem_dados = []

    total_arquivos = len(arquivos_pdf)

    with open(caminho_txt, "w", encoding="utf-8") as arquivo_txt:

        for indice, caminho_pdf in enumerate(arquivos_pdf, start=1):
            nome_pdf = os.path.splitext(os.path.basename(caminho_pdf))[0]

            if atualizar_status:
                atualizar_status(f"Processando {indice} de {total_arquivos}: {nome_pdf}.pdf")

            try:
                dados = extrair_dados_pdf(caminho_pdf)

                if not dados:
                    arquivos_sem_dados.append(nome_pdf)
                else:
                    for item in dados:
                        linha = montar_linha_txt(nome_pdf, item["data"], item["valor"])
                        arquivo_txt.write(linha + "\n")
                        total_linhas += 1

                    arquivos_processados += 1

            except Exception:
                arquivos_sem_dados.append(nome_pdf)

            if atualizar_progresso:
                progresso = int((indice / total_arquivos) * 100)
                atualizar_progresso(progresso)

    if total_linhas == 0:
        raise Exception("Nenhum dado foi extraído de nenhum PDF.")

    return {
        "modo": 1,
        "caminho_txt": caminho_txt,
        "total_pdfs": total_arquivos,
        "arquivos_processados": arquivos_processados,
        "total_linhas": total_linhas,
        "arquivos_sem_dados": arquivos_sem_dados
    }