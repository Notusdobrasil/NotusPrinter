# NotusPrinter - Sistema de Impressão

## 📋 Descrição
Sistema web para gerenciamento e impressão de etiquetas, desenvolvido em Flask.

## 🚀 Como Executar

### Opção 1: Executável (Recomendado para distribuição)
1. Execute o arquivo `NotusPrinter.exe`
2. O sistema abrirá automaticamente no navegador em `http://127.0.0.1:5000`
3. Para parar o sistema, feche a janela do terminal ou pressione `Ctrl+C`

### Opção 2: Código Fonte (Para desenvolvedores)
1. Instale Python 3.13+
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute: `python main.py`

## 📁 Arquivos Necessários
Para distribuir o sistema, você precisa incluir:
- `NotusPrinter.exe` (executável principal)
- `etiquetas.db` (banco de dados)
- `update_signal.txt` (arquivo de controle)

## 🔧 Funcionalidades
- ✅ Visualização de arquivos processados
- ✅ Impressão completa de etiquetas
- ✅ Impressão parcial (apenas volumes não repetidos)
- ✅ Histórico de pedidos
- ✅ Sistema de autorização para reimpressão
- ✅ Interface web responsiva

## 🌐 Acesso
- URL: http://127.0.0.1:5000
- Porta: 5000 (padrão)
- Host: 127.0.0.1 (apenas local)

## 📝 Notas Importantes
- O sistema funciona apenas na máquina local
- Não requer instalação de Python nas máquinas de destino
- O banco de dados SQLite é incluído no executável
- Compatível com Windows 10/11

## 🛠️ Desenvolvimento
Para modificar o sistema:
1. Edite os arquivos Python conforme necessário
2. Regenerar o executável: `pyinstaller notus_printer.spec`
3. O novo executável estará em `dist/NotusPrinter.exe`

## 📞 Suporte
Para dúvidas ou problemas, entre em contato com a equipe de desenvolvimento.
