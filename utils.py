import pdfplumber
from config import MESES


# =========================================================
# LEITURA DE PDF
# =========================================================

def ler_texto_pdf(caminho_pdf):
    """
    Extrai todo o texto de um PDF, página por página.
    Usado tanto pelo Modo 1 quanto pelo Modo 2.
    """
    texto_completo = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"

    return texto_completo


# =========================================================
# CONVERSÃO DE VALORES
# =========================================================

def valor_br_para_texto(valor_br):
    """
    Converte valor no formato brasileiro para formato americano.
    Exemplo:
    9.260,00 -> 9260.00
    20.731,50 -> 20731.50
    0,00 -> 0.00
    """
    valor = valor_br.strip().replace(".", "").replace(",", ".")
    return f"{float(valor):.2f}"


# =========================================================
# CONVERSÃO DE DATAS
# =========================================================

def nome_mes_para_data(mes_ano):
    """
    Converte Maio/2025 para 01/05/2025
    Usado no Modo 1 (mês por extenso).
    """
    mes, ano = mes_ano.split("/")
    mes = mes.strip().lower()

    numero_mes = MESES.get(mes)

    if not numero_mes:
        raise ValueError(f"Mês não reconhecido: {mes}")

    return f"01/{numero_mes}/{ano}"


def numero_mes_para_data(mes_ano):
    """
    Converte 01/2025 para 01/01/2025
    Usado no Modo 2 (mês já numérico).
    """
    mes, ano = mes_ano.split("/")
    return f"01/{mes}/{ano}"


# =========================================================
# MONTAGEM DE LINHA PADRÃO DO TXT
# =========================================================

def montar_linha_txt(nome_arquivo, data, valor):
    """
    Monta a linha padrão usada em ambos os modos:
    nome_arquivo <TAB> data <TAB> valor <TAB> valor <TAB> 0.00
    """
    return f"{nome_arquivo}\t{data}\t{valor}\t{valor}\t0.00"