# NotusPrinter - Sistema de Gestão de Impressão

## 📋 Descrição
Sistema completo para monitoramento e impressão de etiquetas com interface web e monitoramento automático de arquivos.

## 🚀 Instalação Rápida

### Opção 1: Instalação Automática (Recomendada)
1. Execute o arquivo `install.bat`
2. O script instalará automaticamente todas as dependências
3. Após a instalação, execute `iniciar_completo.bat`

### Opção 2: Instalação Manual

#### Pré-requisitos
- Python 3.8 ou superior
- Windows 10/11

#### Passos:
1. **Instalar Python**: Baixe do [python.org](https://www.python.org/downloads/)
   - Marque "Add Python to PATH" durante a instalação

2. **Configurar Ambiente Virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Criar Banco de Dados**:
   ```bash
   python cria_banco.py
   ```

4. **Executar Sistema**:
   ```bash
   # Terminal 1: Monitor de arquivos
   python monitor.py
   
   # Terminal 2: Aplicação web
   python app.py
   ```

## 🎯 Como Usar

### Iniciar o Sistema Completo
Execute `iniciar_completo.bat` - iniciará ambos os componentes automaticamente.

### Componentes Disponíveis

1. **Monitor de Arquivos** (`monitor.py`):
   - Monitora automaticamente arquivos HTML no diretório Temp
   - Processa etiquetas automaticamente
   - Detecta duplicatas e enviar notificações

2. **Aplicação Web** (`app.py`):
   - Interface web em `http://localhost:5000`
   - Visualização de arquivos processados
   - Impressão de etiquetas individual ou em lote
   - Gestão de reimpressões

### Funcionalidades Principais

- ✅ **Monitoramento Automático**: Detecta novos arquivos HTML automaticamente
- ✅ **Detecção de Duplicatas**: Identifica pedidos já processados
- ✅ **Interface Web**: Interface amigável para gestão
- ✅ **Impressão Inteligente**: Impressão parcial para evitar duplicatas
- ✅ **Histórico Completo**: Visualização de histórico de pedidos
- ✅ **Notificações**: Alertas do sistema operativo

## 📁 Estrutura do Projeto

```
NotusPrinter/
├── app.py                 # Aplicação web Flask
├── monitor.py             # Monitor de arquivos
├── cria_banco.py          # Script de criação do banco
├── etiquetas.db           # Banco de dados SQLite
├── requirements.txt       # Dependências Python
├── install.bat           # Instalador automático
├── iniciar_completo.bat   # Inicializador completo
├── iniciar_app.bat        # Apenas aplicação web
├── iniciar_monitor.bat    # Apenas monitor
├── static/               # Arquivos estáticos (CSS, imagens)
└── templates/            # Templates HTML
```

## 🔧 Configuração

### Diretório Monitorado
Por padrão, o sistema monitora: `C:\Users\{usuario}\AppData\Local\Temp\`

### Arquivos Processados
O sistema processa arquivos que:
- Começam com "tmp"
- Termina com ".html"
- Contém etiquetas válidas

### Código de Reimpressão
Código padrão: `VIP123` (alterável em `app.py`)

## 🛠️ Manutenção

### Atualizar Dependências
```bash
venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

### Backup do Banco de Dados
O banco de dados está em `etiquetas.db`. Faça backup regular deste arquivo.

### Logs
Logs são exibidos no terminal onde o monitor está rodando.

## 🚨 Resolução de Problemas

### Erro "Python não encontrado"
- Instale Python do site oficial
- Certifique-se de marcar "Add Python to PATH"

### Erro de permissões
- Execute os arquivos .bat como Administrador
- Verifique se o antivírus não está bloqueando

### Porta 5000 ocupada
- Feche outros programas que usam a porta 5000
- Ou altere a porta em `app.py` (última linha)

### Monitor não funciona
- Verifique se o diretório Temp existe
- Execute como Administrador se necessário

## 📞 Suporte
Para questões técnicas ou bugs, entre em contato com o desenvolvedor.

---
**NotusPrinter v1.0** - Sistema de Gestão de Impressão de Etiquetas
