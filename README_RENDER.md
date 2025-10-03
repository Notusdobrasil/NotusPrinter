# Deploy no Render.com

Este guia explica como fazer o deploy desta aplicação Flask no Render.com.

## Pré-requisitos

- Conta no Render.com
- Projeto configurado no GitHub

## Configuração no Render

### 1. Configurar um novo Web Service

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em "New +"
3. Selecione "Web Service"
4. Conecte seu repositório GitHub
5. Selecione este repositório

### 2. Configurações do Serviço

**Configurações básicas:**
- **Name**: impressao-etiquetas (ou o nome de sua escolha)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Port**: Deixe padrão (Render usa variável PORT automaticamente)

**Configurações de ambiente:**
- **FLASK_ENV**: production
- **CODIGO_REIMPRESSAO**: VIP123 (ou outro código de sua escolha)
- **SECRET_API_KEY**: Sua chave secreta personalizada

### 3. Recursos necessários

- **Plano**: Starter (gratuito) é suficiente para começarmos
- **Auto Deploy**: Ative se quiser que o deploy seja automático a cada commit

### 4. Banco de dados

A aplicação usa SQLite que será criado automaticamente pelo Render. O arquivo `etiquetas.db` será gerado na primeira execução.

## Arquivos importantes

- `app.py`: Aplicação principal Flask
- `requirements.txt`: Dependências Python otimizadas para produção
- `Procfile`: Configuração do processo web
- `render.yaml`: Configuração alternativa do Render (opcional)

## Monitoramento

**Nota**: O arquivo `monitor.py` é específico para Windows e monitoramento local. No ambiente de produção no Render, você precisará implementar uma solução diferente para upload de arquivos HTML.

## Variáveis de Ambiente no Render

Configure estas variáveis no dashboard do Render:

- `FLASK_ENV=production`
- `CODIGO_REIMPRESSAO=VIP123` (personalize conforme necessário)
- `SECRET_API_KEY=sua_chave_secreta` (personalize conforme necessário)

## URL de acesso

Após o deploy, sua aplicação estará disponível em:
`https://impressao-etiquetas.onrender.com` (substitua pelo nome do seu serviço)

## Funcionalidades disponíveis

- ✅ Visualização de etiquetas processadas
- ✅ Impressão individual ou em lote
- ✅ Sistema de autorização para reimpressão
- ✅ Histórico de pedidos
- ⚠️ Monitoramento de arquivos precisa de adaptação para ambiente cloud

## Troubleshooting

1. **Erro de importação**: Verifique se todas as dependências estão no requirements.txt
2. **Erro 500**: Verifique os logs do Render para identificar problemas
3. **Banco não inicializado**: Execute `cria_banco.py` uma vez ou verifique se as tabelas existem

## Próximos passos

Para ambiente de produção, considere:
1. Implementar upload de arquivos via interface web
2. Usar banco PostgreSQL para melhor performance
3. Implementar autenticação de usuários
4. Adicionar logs estruturados
