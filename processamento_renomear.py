import os
import shutil
import re

try:
    import openpyxl
except ImportError:
    openpyxl = None

try:
    import xlrd
except ImportError:
    xlrd = None


def limpar_nome_arquivo(nome):
    """
    Limpa o nome do arquivo.

    Exemplo:
    1.0 -> 1
    2.0 -> 2
    Empresa/Teste -> Empresa-Teste
    """
    nome = str(nome).strip()

    if nome.endswith(".0"):
        nome = nome[:-2]

    nome = re.sub(r'[\\/:*?"<>|]', "-", nome)
    nome = re.sub(r"\s+", " ", nome)

    return nome


def limpar_cnpj(cnpj):
    """
    Remove tudo que não for número do CNPJ/CPF.
    Também corrige caso venha como 32719920000167.0.
    """
    cnpj = str(cnpj).strip()

    if cnpj.endswith(".0"):
        cnpj = cnpj[:-2]

    cnpj = re.sub(r"\D", "", cnpj)

    return cnpj


def caminho_unico(pasta, nome_base, extensao=".pdf"):
    """
    Evita sobrescrever arquivo se já existir.

    Exemplo:
    1.pdf
    1_1.pdf
    1_2.pdf
    """
    caminho = os.path.join(pasta, f"{nome_base}{extensao}")
    contador = 1

    while os.path.exists(caminho):
        caminho = os.path.join(pasta, f"{nome_base}_{contador}{extensao}")
        contador += 1

    return caminho


def ler_planilha_xls(caminho_excel):
    if xlrd is None:
        raise ImportError(
            "A biblioteca xlrd não está instalada.\n\n"
            "Instale com:\n"
            "py -m pip install xlrd\n\n"
            "Ou salve a planilha como .xlsx."
        )

    dados = []

    planilha = xlrd.open_workbook(caminho_excel)
    aba = planilha.sheet_by_index(0)

    # Sua planilha:
    # Linha 4 = cabeçalho
    # Linha 5 em diante = dados
    # Coluna A / índice 0 = Código / Nome do arquivo final
    # Coluna C / índice 2 = CNPJ/CPF
    for indice_linha in range(4, aba.nrows):
        nome = aba.cell_value(indice_linha, 0)   # Coluna A
        cnpj = aba.cell_value(indice_linha, 2)   # Coluna C

        if nome in ("", None) or cnpj in ("", None):
            continue

        novo_nome = limpar_nome_arquivo(nome)
        cnpj_limpo = limpar_cnpj(cnpj)

        if novo_nome and cnpj_limpo:
            dados.append((novo_nome, cnpj_limpo))

    return dados


def ler_planilha_xlsx(caminho_excel):
    if openpyxl is None:
        raise ImportError(
            "A biblioteca openpyxl não está instalada.\n\n"
            "Instale com:\n"
            "py -m pip install openpyxl"
        )

    dados = []

    planilha = openpyxl.load_workbook(caminho_excel, data_only=True)
    aba = planilha.active

    try:
        # Linha 5 em diante
        for linha in aba.iter_rows(min_row=5, values_only=True):
            if not linha:
                continue

            nome = linha[0] if len(linha) > 0 else None   # Coluna A
            cnpj = linha[2] if len(linha) > 2 else None   # Coluna C

            if nome is None or cnpj is None:
                continue

            novo_nome = limpar_nome_arquivo(nome)
            cnpj_limpo = limpar_cnpj(cnpj)

            if novo_nome and cnpj_limpo:
                dados.append((novo_nome, cnpj_limpo))

    finally:
        planilha.close()

    return dados


def ler_planilha_banco(caminho_excel):
    extensao = os.path.splitext(caminho_excel)[1].lower()

    if extensao == ".xls":
        return ler_planilha_xls(caminho_excel)

    if extensao == ".xlsx":
        return ler_planilha_xlsx(caminho_excel)

    raise ValueError("Formato de Excel não suportado. Use .xls ou .xlsx.")


def renomear_arquivos(caminho_excel, pasta_pdfs, atualizar_status=None, atualizar_progresso=None):
    if atualizar_status:
        atualizar_status("Lendo planilha...")

    dados_banco = ler_planilha_banco(caminho_excel)

    if not dados_banco:
        raise Exception(
            "Nenhum registro foi encontrado na planilha.\n\n"
            "Verifique se:\n"
            "- O código está na coluna A\n"
            "- O CNPJ/CPF está na coluna C\n"
            "- Os dados começam na linha 5"
        )

    pasta_destino = os.path.join(pasta_pdfs, "Arquivos_Renomeados")
    os.makedirs(pasta_destino, exist_ok=True)

    pdfs = [
        arquivo for arquivo in os.listdir(pasta_pdfs)
        if arquivo.lower().endswith(".pdf")
    ]

    total = len(dados_banco)
    copiados = 0
    nao_encontrados = 0
    lista_nao_encontrados = []

    for indice, (novo_nome, cnpj) in enumerate(dados_banco, start=1):
        base_cnpj = cnpj[:8]
        encontrado = None

        for pdf in pdfs:
            pdf_normalizado = re.sub(r"\D", "", pdf)

            if base_cnpj and base_cnpj in pdf_normalizado:
                encontrado = pdf
                break

        if encontrado:
            origem = os.path.join(pasta_pdfs, encontrado)
            destino = caminho_unico(pasta_destino, novo_nome)

            shutil.copy2(origem, destino)
            copiados += 1

            if atualizar_status:
                atualizar_status(
                    f"Copiado: {encontrado} -> {os.path.basename(destino)}"
                )

        else:
            nao_encontrados += 1
            lista_nao_encontrados.append((novo_nome, cnpj))

            if atualizar_status:
                atualizar_status(f"Não encontrado: {cnpj} -> {novo_nome}.pdf")

        if atualizar_progresso and total > 0:
            atualizar_progresso(int((indice / total) * 100))

    return {
        "total_linhas": total,
        "copiados": copiados,
        "nao_encontrados": nao_encontrados,
        "lista_nao_encontrados": lista_nao_encontrados,
        "pasta_destino": pasta_destino,
    }