@echo off
echo ================================================
echo     Instalador do NotusPrinter
echo ================================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao foi encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior a partir de:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo Python encontrado. Verificando versao...
python --version

:: Criar ambiente virtual
echo.
echo Criando ambiente virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

:: Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate

:: Instalar dependências
echo.
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

:: Criar banco de dados
echo.
echo Criando banco de dados novo...
if exist "etiquetas.db" (
    echo Removendo banco de dados antigo...
    del "etiquetas.db"
)
if exist "etiquetas_exemplo.db" (
    echo Removendo banco de exemplo...
    del "etiquetas_exemplo.db"
)
python cria_banco.py
if %errorlevel% neq 0 (
    echo ERRO: Falha ao criar banco de dados!
    echo Verifique se tem permissoes de escrita na pasta.
    pause
    exit /b 1
)
echo Banco de dados criado com sucesso!

echo.
echo ================================================
echo     Instalacao concluida com sucesso!
echo ================================================
echo.
echo Para executar o programa:
echo   1. Use o arquivo "iniciar_app.bat"
echo   2. Ou execute manualmente: python app.py
echo.
echo Para monitorar arquivos automaticamente:
echo   1. Use o arquivo "iniciar_monitor.bat"
echo   2. Ou execute manualmente: python monitor.py
echo.
echo IMPORTANTE: Execute ambos os programas para usar todas as funcionalidades!
echo.
pause
