@echo off
title NotusPrinter - Inicio Rapido
color 0B
echo.
echo ================================================
echo           NOTUS PRINTER - INICIO RAPIDO
echo ================================================
echo.
echo Iniciando sistema automaticamente...
echo.

:: Verificar se ja foi instalado
if not exist "venv" (
    echo [INSTALANDO] Primeira execucao detectada...
    echo Executando instalacao automatica...
    call install.bat
    echo.
) else (
    :: Verificar se banco existe, se nao criar um novo
    if not exist "etiquetas.db" (
        echo [CRIANDO] Banco de dados novo...
        call venv\Scripts\activate
        python cria_banco.py
        echo Banco de dados criado!
    )
)

:: Iniciar sistema completo
echo [INICIANDO] Sistema NotusPrinter...
call iniciar_completo.bat
