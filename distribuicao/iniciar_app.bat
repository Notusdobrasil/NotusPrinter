@echo off
title NotusPrinter - Aplicacao Web
echo ================================================
echo     Iniciando NotusPrinter Web App
echo ================================================
echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Iniciando servidor web...
echo A aplicacao estara disponivel em: http://localhost:5000
echo Pressione Ctrl+C para parar o servidor
echo.

python app.py

echo.
echo Servidor parado.
pause
