Assim, quando você quiser adicionar um Modo 3 no futuro,
basta criar processamento_modo3.py, importar em interface.py, 
adicionar um terceiro Radiobutton e um elif no processar().
Nada dos outros arquivos precisa ser tocado. 🎯

Quer que eu revise tudo junto agora pra garantir que os imports estão 100% consistentes entre os arquivos,
ou já quer partir para a próxima funcionalidade?



pyinstaller --onefile --noconsole --name ConversorPDF app.py