document.addEventListener("DOMContentLoaded", function () {
    const inputPdfs = document.getElementById("pdfs");
    const infoPdfs = document.getElementById("infoPdfs");

    const inputPdfsRenomear = document.getElementById("pdfsRenomear");
    const infoPdfsRenomear = document.getElementById("infoPdfsRenomear");

    const formGerarTxt = document.getElementById("formGerarTxt");
    const formRenomear = document.getElementById("formRenomear");

    const statusTexto = document.getElementById("statusTexto");
    const barraProgresso = document.getElementById("barraProgresso");

    function atualizarInfoArquivos(input, elementoInfo) {
        const quantidade = input.files.length;

        if (quantidade === 0) {
            elementoInfo.textContent = "Nenhum arquivo selecionado.";
        } else if (quantidade === 1) {
            elementoInfo.textContent = "1 arquivo selecionado.";
        } else {
            elementoInfo.textContent = quantidade + " arquivos selecionados.";
        }
    }

    function resetarTelaDepoisDoDownload(formulario, textoBotaoOriginal, mensagemFinal) {
        setTimeout(function () {
            statusTexto.textContent = mensagemFinal;
            barraProgresso.style.width = "100%";

            const botao = formulario.querySelector("button[type='submit']");
            botao.disabled = false;
            botao.textContent = textoBotaoOriginal;
        }, 3000);
    }

    if (inputPdfs) {
        inputPdfs.addEventListener("change", function () {
            atualizarInfoArquivos(inputPdfs, infoPdfs);
            statusTexto.textContent = "Arquivos selecionados. Clique em Gerar TXT.";
            barraProgresso.style.width = "0%";
        });
    }

    if (inputPdfsRenomear) {
        inputPdfsRenomear.addEventListener("change", function () {
            atualizarInfoArquivos(inputPdfsRenomear, infoPdfsRenomear);
            statusTexto.textContent = "PDFs para renomeação selecionados.";
            barraProgresso.style.width = "0%";
        });
    }

    if (formGerarTxt) {
        formGerarTxt.addEventListener("submit", function () {
            statusTexto.textContent = "Enviando arquivos e processando PDFs...";
            barraProgresso.style.width = "60%";

            const botao = formGerarTxt.querySelector("button[type='submit']");
            botao.disabled = true;
            botao.textContent = "Processando...";

            resetarTelaDepoisDoDownload(
                formGerarTxt,
                "Gerar Arquivo de Importação DOMÍNIO",
                "Processamento finalizado. Se tudo ocorreu bem, o download do ZIP foi iniciado."
            );
        });
    }

    if (formRenomear) {
        formRenomear.addEventListener("submit", function () {
            statusTexto.textContent = "Enviando arquivos e renomeando PDFs...";
            barraProgresso.style.width = "60%";

            const botao = formRenomear.querySelector("button[type='submit']");
            botao.disabled = true;
            botao.textContent = "Renomeando...";

            resetarTelaDepoisDoDownload(
                formRenomear,
                "Renomear Arquivos",
                "Renomeação finalizada. Se tudo ocorreu bem, o download do ZIP foi iniciado."
            );
        });
    }

    window.addEventListener("pageshow", function () {
        if (formGerarTxt) {
            const botaoGerar = formGerarTxt.querySelector("button[type='submit']");
            botaoGerar.disabled = false;
            botaoGerar.textContent = "Gerar Arquivo de Importação DOMÍNIO";
        }

        if (formRenomear) {
            const botaoRenomear = formRenomear.querySelector("button[type='submit']");
            botaoRenomear.disabled = false;
            botaoRenomear.textContent = "Renomear Arquivos";
        }
    });
});