# 📥 Como Baixar e Instalar o NotusPrinter

## 🎯 Métodos de Download

### 1. **Download via Arquivo ZIP** (Mais Fácil)

#### Para Distribuir para Outros Usuários:
1. Execute `distribuir.bat` no projeto atual
2. Isso criará um arquivo ZIP: `NotusPrinter_[DATA].zip`
3. Envie este arquivo ZIP para outras pessoas

#### Para Instalar em Outra Máquina:
1. **Baixe o arquivo ZIP** do NotusPrinter
2. **Extraia** o arquivo ZIP em uma pasta (ex: Desktop\NotusPrinter)
3. **Execute** `INICIAR.bat`
4. **Pronto!** Sistema funcionando automaticamente

### 2. **Git Clone** (Para Desenvolvedores)

```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd NotusPrinter

# Instalar dependências
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Criar banco de dados
python cria_banco.py

# Executar
python app.py
```

### 3. **Download Manual** (GitHub/GitLab)

1. Acesse o repositório no GitHub/GitLab
2. Clique em **"Code"** → **"Download ZIP"**
3. Extraia o arquivo ZIP
4. Execute `INICIAR.bat`

## 🚀 Instalação Super Rápida

### Para Usuários Finais (Recomendado):
```
1. Baixar arquivo ZIP
2. Extrair arquivo ZIP
3. Executar INICIAR.bat
4. Pronto! Sistema funcionando!
```

### Requisitos Mínimos:
- **Windows 10/11**
- **Python 3.8+** (será instalado automaticamente se necessário)

## 📋 Passos Detalhados de Instalação

### Passo 1: Download
- Baixe o arquivo `NotusPrinter_[DATA].zip`
- Salve em uma pasta de fácil acesso

### Passo 2: Extração
- Clique com botão direito no ZIP
- Selecione "Extrair aqui" ou "Extract here"
- Isso criará uma pasta com todos os arquivos

### Passo 3: Instalação Automática
- Entre na pasta extraída
- Execute `INICIAR.bat`
- O sistema fará tudo automaticamente:
  - ✅ Verificar Python
  - ✅ Instalar dependências
  - ✅ Criar banco de dados
  - ✅ Iniciar sistema completo

### Passo 4: Uso
- O navegador abrirá automaticamente em `http://localhost:5000`
- O monitor de arquivos estará ativo
- Sistema pronto para uso!

## 🔧 Instalação Manual (Alternativa)

Se preferir instalar manualmente:

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar banco de dados
python cria_banco.py

# 5. Executar sistema
python app.py
```

## 📁 Estrutura Após Download

```
NotusPrinter/
├── INICIAR.bat              ← EXECUTE ESTE ARQUIVO
├── iniciar_completo.bat     ← Alternativa detalhada
├── install.bat             ← Instalador manual
├── app.py                  ← Aplicação web
├── monitor.py              ← Monitor de arquivos
├── requirements.txt        ← Dependências
├── README.md               ← Manual completo
├── GUIA_DISTRIBUICAO.md    ← Guia de distribuição
├── static/                 ← Arquivos estáticos
└── templates/              ← Templates HTML
```

## ⚡ Instalação em 30 Segundos

**Para usuários que querem rapidez máxima:**

1. **Download** → Baixar ZIP
2. **Extrair** → Extrair arquivo
3. **Executar** → Clicar em `INICIAR.bat`
4. **Usar** → Sistema funcionando!

## 🆘 Resolução de Problemas

### Erro "Python não encontrado"
- Instale Python do [python.org](https://www.python.org/downloads/)
- Marque "Add Python to PATH" durante instalação

### Erro de permissões
- Execute `INICIAR.bat` como Administrador
- Verifique se antivírus não está bloqueando

### Porta 5000 ocupada
- Feche outros programas usando porta 5000
- Ou altere porta em `app.py`

## 📞 Suporte

Se tiver problemas:
1. Verifique se Python está instalado
2. Execute como Administrador
3. Verifique logs no terminal
4. Entre em contato para suporte técnico

---

**NotusPrinter** - Sistema de Gestão de Impressão de Etiquetas
**Instalação em menos de 1 minuto!** ⚡
