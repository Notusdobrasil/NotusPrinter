# Sistema de Impressão de Etiquetas

Sistema web para gerenciamento e impressão de etiquetas de envio.

## Funcionalidades

- Monitoramento automático de arquivos HTML de etiquetas
- Interface web para visualização e impressão
- Controle de reimpressões com código de autorização
- Histórico de pedidos e volumes
- Detecção de duplicatas

## Tecnologias

- **Backend**: Python Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Monitoramento**: Watchdog

## Instalação Local

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o monitor:
   ```bash
   python monitor.py
   ```
5. Execute a aplicação web:
   ```bash
   python app.py
   ```

## Deploy no Railway

1. Faça push do código para o GitHub
2. Conecte o repositório no Railway
3. O deploy será automático

## Estrutura do Projeto

- `app.py` - Aplicação Flask principal
- `monitor.py` - Monitor de arquivos
- `wsgi.py` - Configuração para produção
- `etiquetas.db` - Banco de dados SQLite
- `templates/` - Templates HTML
- `static/` - Arquivos estáticos

## Configuração

- O monitor observa arquivos HTML no diretório temp do usuário
- Código de reimpressão: `VIP123`
- Porta padrão: 5000 (configurável via variável PORT)
