@echo off
title NotusPrinter - Criar Pacote de Distribuicao
echo ================================================
echo     Criando Pacote de Distribuicao
echo ================================================
echo.

set DATA_HOJE=%date:~0,2%%date:~3,2%%date:~6,4%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATA_HOJE=%DATA_HOJE: =0%
set NOME_ARQUIVO=NotusPrinter_%DATA_HOJE%

echo Criando pasta de distribuicao...
if exist "distribuicao" rmdir /s /q "distribuicao"
mkdir "distribuicao"

echo Copiando arquivos essenciais...
copy "*.py" "distribuicao\"
copy "*.bat" "distribuicao\"
copy "*.txt" "distribuicao\"
copy "*.md" "distribuicao\"

echo Criando banco de dados de exemplo...
copy "etiquetas.db" "distribuicao\etiquetas_exemplo.db" 2>nul

echo Copiando pastas...
xcopy "static" "distribuicao\static\" /e /i /q
xcopy "templates" "distribuicao\templates\" /e /i /q

echo Criando arquivo ZIP...
powershell Compress-Archive -Path "distribuicao\*" -DestinationPath "%NOME_ARQUIVO%.zip" -Force

echo.
echo ================================================
echo     Distribuicao Criada com Sucesso!
echo ================================================
echo Arquivo: %NOME_ARQUIVO%.zip
echo Local: %CD%\%NOME_ARQUIVO%.zip
echo.
echo Para distribuir:
echo 1. Envie o arquivo ZIP para outras maquinas
echo 2. Extraia o conteudo
echo 3. Execute "install.bat"
echo.
pause
