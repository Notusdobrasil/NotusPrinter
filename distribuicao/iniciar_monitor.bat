@echo off
title NotusPrinter - Monitor de Arquivos
echo ================================================
echo     Iniciando Monitor de Arquivos
echo ================================================
echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Iniciando monitor de arquivos...
echo Monitorando: C:\Users\%USERNAME%\AppData\Local\Temp\
echo Pressione Ctrl+C para parar o monitor
echo.

python monitor.py

echo.
echo Monitor parado.
pause
