import os
import re
import glob

from utils import ler_texto_pdf, valor_br_para_texto, numero_mes_para_data, montar_linha_txt
from config import (
    ARQUIVO_RECEITA,
    ARQUIVO_FOLHA,
    SECAO_RECEITA_INICIO,
    SECAO_RECEITA_FIM,
    SECAO_MERCADO_INTERNO_INICIO,
    SECAO_MERCADO_INTERNO_FIM,
    SECAO_FOLHA_INICIO,
    SECAO_FOLHA_FIM,
)


# =========================================================
# FUNÇÕES DE APOIO (ESPECÍFICAS DO MODO 2)
# =========================================================

def extrair_secao(texto, inicio, fim=None):
    """
    Extrai um trecho do texto entre dois marcadores.
    Se 'fim' não for encontrado, retorna até o final do texto.
    """
    pos_inicio = texto.find(inicio)

    if pos_inicio == -1:
        return ""

    if fim:
        pos_fim = texto.find(fim, pos_inicio)
        if pos_fim == -1:
            return texto[pos_inicio:]
        return texto[pos_inicio:pos_fim]

    return texto[pos_inicio:]


def extrair_pares_mes_valor(texto):
    """
    Extrai pares no formato:
    01/2025 20.731,50
    02/2025 20.111,20
    """
    padrao = re.compile(r"(\d{2}/\d{4})\s+([\d\.]+,\d{2})")
    return padrao.findall(texto)


# =========================================================
# EXTRAÇÃO DE RECEITA E FOLHA
# =========================================================

def gerar_linhas_receita(texto, nome_arquivo):
    linhas = []

    secao_22 = extrair_secao(texto, SECAO_RECEITA_INICIO, SECAO_RECEITA_FIM)

    if not secao_22:
        return linhas

    mercado_interno = extrair_secao(
        secao_22,
        SECAO_MERCADO_INTERNO_INICIO,
        SECAO_MERCADO_INTERNO_FIM
    )

    receitas = extrair_pares_mes_valor(mercado_interno)

    for mes_ano, valor_br in receitas:
        data = numero_mes_para_data(mes_ano)
        valor = valor_br_para_texto(valor_br)
        linha = montar_linha_txt(nome_arquivo, data, valor)
        linhas.append(linha)

    return linhas


def gerar_linhas_folha(texto, nome_arquivo):
    linhas = []

    secao_23 = extrair_secao(texto, SECAO_FOLHA_INICIO, SECAO_FOLHA_FIM)

    if not secao_23 or "Nenhuma" in secao_23:
        return linhas

    folhas = extrair_pares_mes_valor(secao_23)

    for mes_ano, valor_br in folhas:
        data = numero_mes_para_data(mes_ano)
        valor = valor_br_para_texto(valor_br)
        linha = montar_linha_txt(nome_arquivo, data, valor)
        linhas.append(linha)

    return linhas


# =========================================================
# GERAÇÃO DOS TXTs (MODO 2)
# =========================================================

def gerar_txt_modo2(pasta_pdf, atualizar_status=None, atualizar_progresso=None):
    """
    Gera os TXTs de Receita e Folha a partir de PDFs completos (Modo 2).
    """
    arquivos_pdf = glob.glob(os.path.join(pasta_pdf, "*.pdf"))

    if not arquivos_pdf:
        raise FileNotFoundError("Nenhum arquivo PDF foi encontrado na pasta selecionada.")

    linhas_receita = []
    linhas_folha = []
    arquivos_sem_dados = []
    arquivos_processados = 0

    total_arquivos = len(arquivos_pdf)

    for indice, caminho_pdf in enumerate(arquivos_pdf, start=1):
        nome_pdf = os.path.splitext(os.path.basename(caminho_pdf))[0]

        if atualizar_status:
            atualizar_status(f"Processando {indice} de {total_arquivos}: {nome_pdf}.pdf")

        try:
            texto = ler_texto_pdf(caminho_pdf)

            receitas_arquivo = gerar_linhas_receita(texto, nome_pdf)
            folhas_arquivo = gerar_linhas_folha(texto, nome_pdf)

            linhas_receita.extend(receitas_arquivo)
            linhas_folha.extend(folhas_arquivo)

            if receitas_arquivo or folhas_arquivo:
                arquivos_processados += 1
            else:
                arquivos_sem_dados.append(nome_pdf)

        except Exception:
            arquivos_sem_dados.append(nome_pdf)

        if atualizar_progresso:
            progresso = int((indice / total_arquivos) * 100)
            atualizar_progresso(progresso)

    if not linhas_receita and not linhas_folha:
        raise Exception("Nenhum dado foi extraído de nenhum PDF.")

    caminho_receita = None
    caminho_folha = None

    if linhas_receita:
        caminho_receita = os.path.join(pasta_pdf, ARQUIVO_RECEITA)
        with open(caminho_receita, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas_receita))

    if linhas_folha:
        caminho_folha = os.path.join(pasta_pdf, ARQUIVO_FOLHA)
        with open(caminho_folha, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas_folha))

    return {
        "modo": 2,
        "caminho_receita": caminho_receita,
        "caminho_folha": caminho_folha,
        "total_pdfs": total_arquivos,
        "arquivos_processados": arquivos_processados,
        "total_linhas_receita": len(linhas_receita),
        "total_linhas_folha": len(linhas_folha),
        "arquivos_sem_dados": arquivos_sem_dados
    }