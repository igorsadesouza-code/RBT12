# =========================================================
# CONFIGURAÇÕES GERAIS DO SISTEMA
# =========================================================

# --- Nomes dos arquivos de saída ---
ARQUIVO_RECEITA = "EFSIMPLES_NACIONAL_RECEITA_BRUTA_ANTERIOR.txt"
ARQUIVO_FOLHA = "EFSIMPLES_NACIONAL_FOLHA_ANTERIOR.txt"


# --- Dicionário de meses (usado na conversão de datas) ---
MESES = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "marco": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12",
}


# --- Cores do sistema (identidade visual) ---
COR_PRIMARIA = "#123121"      # fundo principal
COR_SECUNDARIA = "#d64000"    # botões e destaques
COR_HOVER = "#b83800"         # cor do botão ao passar o mouse
COR_TEXTO = "#ffffff"         # cor do texto
COR_DESABILITADO = "#777777"  # cor de botão desabilitado


# --- Configurações da janela ---
TITULO_JANELA = "Receita Bruta Acumulada"
LARGURA_JANELA = 540
ALTURA_JANELA = 520


# --- Fontes padrão ---
FONTE_TITULO = ("Arial", 16, "bold")
FONTE_TEXTO = ("Arial", 10)
FONTE_PEQUENA = ("Arial", 9)
FONTE_BOTAO = ("Arial", 10, "bold")


# --- Textos de seção usados no Modo 2 (PDF completo) ---
SECAO_RECEITA_INICIO = "2.2) Receitas Brutas Anteriores"
SECAO_RECEITA_FIM = "2.3) Folha de Salários Anteriores"
SECAO_MERCADO_INTERNO_INICIO = "2.2.1) Mercado Interno"
SECAO_MERCADO_INTERNO_FIM = "2.2.2) Mercado Externo"

SECAO_FOLHA_INICIO = "2.3) Folha de Salários Anteriores"
SECAO_FOLHA_FIM = "2.4) Fator r"