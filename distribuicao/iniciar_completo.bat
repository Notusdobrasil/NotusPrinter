@echo off
title NotusPrinter - Sistema Completo
color 0A
echo.
echo ================================================
echo     NOTUS PRINTER - SISTEMA COMPLETO
echo ================================================
echo.
echo Este script iniciara automaticamente:
echo [1] Monitor de arquivos (monitor.py)
echo [2] Aplicacao web (app.py)
echo [3] Navegador web
echo.

:: Verificar se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python primeiro.
    pause
    exit /b 1
)

:: Verificar se ambiente virtual existe
if not exist "venv" (
    echo [AVISO] Ambiente virtual nao encontrado!
    echo Executando instalacao automatica...
    call install.bat
    if %errorlevel% neq 0 (
        echo [ERRO] Falha na instalacao!
        pause
        exit /b 1
    )
)

:: Verificar se os programas necessarios existem
if not exist "app.py" (
    echo [ERRO] Arquivo app.py nao encontrado!
    pause
    exit /b 1
)

if not exist "monitor.py" (
    echo [ERRO] Arquivo monitor.py nao encontrado!
    pause
    exit /b 1
)

:: Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate

echo [INFO] Iniciando Monitor de Arquivos...
start "NotusPrinter Monitor" cmd /c "title NotusPrinter Monitor && venv\Scripts\activate && echo Monitor de Arquivos Iniciado && echo Monitorando: C:\Users\%USERNAME%\AppData\Local\Temp\ && echo. && python monitor.py && pause"

echo [INFO] Aguardando inicializacao do monitor...
timeout /t 2 /nobreak >nul

echo [INFO] Iniciando Aplicacao Web...
echo.
echo ================================================
echo     SISTEMA INICIADO COM SUCESSO!
echo ================================================
echo.
echo Monitor: [ATIVO] Monitorando arquivos automaticamente
echo Web App: [ATIVO] http://localhost:5000
echo.
echo Abrindo navegador automaticamente...
echo ================================================
echo.

:: Abrir navegador automaticamente
start "" http://localhost:5000

:: Iniciar aplicacao web
echo Pressione Ctrl+C para parar o sistema completo
echo.
python app.py

echo.
echo ================================================
echo     SISTEMA PARADO
echo ================================================
echo.
echo Para reiniciar, execute este arquivo novamente.
pause
