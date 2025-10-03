from datetime import datetime
import time
import os
import sqlite3
import traceback
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bs4 import BeautifulSoup
from plyer import notification # <-- Importar a biblioteca de notificação

# --- CONFIGURAções ---
def obter_diretorio_monitorado():
    """Obtém o diretório de temp do usuário atual automaticamente"""
    usuario_atual = getpass.getuser()
    diretorio_temp = f"C:/Users/{usuario_atual}/AppData/Local/Temp/"
    
    # Verifica se o diretório existe
    if not os.path.exists(diretorio_temp):
        print(f"AVISO: Diretório {diretorio_temp} não encontrado. Tentando diretório alternativo...")
        # Fallback para o diretório temp padrão do sistema
        diretorio_temp = os.path.join(os.environ.get('TEMP', ''), '')
        if not os.path.exists(diretorio_temp):
            print(f"ERRO: Não foi possível encontrar um diretório temp válido.")
            return None
    
    print(f"Usuário detectado: {usuario_atual}")
    print(f"Diretório monitorado: {diretorio_temp}")
    return diretorio_temp

DIRETORIO_MONITORADO = obter_diretorio_monitorado()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "etiquetas.db")
UPDATE_SIGNAL_FILE = os.path.join(BASE_DIR, "update_signal.txt")

def processar_arquivo_etiqueta(caminho_do_arquivo):
    print(f"Novo ficheiro detetado: {caminho_do_arquivo}")
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        etiquetas_html = soup.find_all('div', class_='etiqueta')
        
        if not etiquetas_html:
            print("Nenhuma etiqueta encontrada no ficheiro.")
            return

        # 1. Extrai o número do pedido para verificação
        primeira_etiqueta_soup = etiquetas_html[0]
        numero_pedido_verificacao = "N/A"
        pedido_tag_verificacao = primeira_etiqueta_soup.find(string=lambda t: "PEDIDO:" in t)
        if pedido_tag_verificacao:
            numero_pedido_verificacao = pedido_tag_verificacao.strip().split(':')[1].strip()

        # 2. Conecta ao banco e verifica o status dos pedidos existentes
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        
        status_final = 'novo'
        if numero_pedido_verificacao != "N/A":
            # --- LÓGICA DE VERIFICAÇÃO ATUALIZADA ---
            # Verifica se já existe um ficheiro para este pedido com status 'duplicado' (amarelo)
            cur.execute("""
                SELECT ap.id FROM arquivos_processados ap
                JOIN etiquetas e ON ap.id = e.arquivo_id
                WHERE e.numero_pedido = ? AND ap.status = 'duplicado'
                LIMIT 1
            """, (numero_pedido_verificacao,))
            duplicado_ja_existe = cur.fetchone()

            if duplicado_ja_existe:
                print(f"ALERTA: Já existe uma reimpressão pendente para o pedido '{numero_pedido_verificacao}'. O ficheiro {os.path.basename(caminho_do_arquivo)} será ignorado.")
                # Dispara a notificação no sistema operativo
                notification.notify(
                    title='Impressão Duplicada Ignorada',
                    message=f'Já existe uma reimpressão pendente para o pedido {numero_pedido_verificacao}. O novo ficheiro foi ignorado.',
                    app_name='Monitor de Impressão',
                    timeout=10 # A notificação desaparecerá após 10 segundos
                )
                conn.close()
                return # Interrompe o processamento deste ficheiro

            # Se não houver duplicado pendente, verifica se o pedido já foi processado alguma vez
            cur.execute("SELECT id FROM etiquetas WHERE numero_pedido = ? LIMIT 1", (numero_pedido_verificacao,))
            pedido_existente = cur.fetchone()
            if pedido_existente:
                status_final = 'duplicado'
                print(f"AVISO: O pedido '{numero_pedido_verificacao}' já existe no banco. Marcando como duplicado.")
        
        # O resto da lógica para inserir o novo ficheiro continua a mesma...
        nome_arquivo = os.path.basename(caminho_do_arquivo)
        total_etiquetas = len(etiquetas_html)
        
        sql_arquivo = "INSERT INTO arquivos_processados (nome_arquivo, caminho_arquivo, total_etiquetas, status) VALUES (?, ?, ?, ?)"
        cur.execute(sql_arquivo, (nome_arquivo, caminho_do_arquivo, total_etiquetas, status_final))
        arquivo_id = cur.lastrowid

        for etiqueta_html in etiquetas_html:
            html_da_etiqueta = str(etiqueta_html)
            # ... (a sua lógica de extração robusta continua aqui) ...
            ref_numero, numero_pedido, data_pedido, nome_destinatario = "N/A", "N/A", "N/A", "N/A"
            endereco_completo, cidade_destinatario, uf_destinatario = "N/A", "N/A", "N/A"
            numero_nf = "N/A"
            volume_atual, volume_total = 0, 0
            
            try:
                ref_numero = etiqueta_html.find('b').get_text(strip=True)
                pedido_tag = etiqueta_html.find(string=lambda t: "PEDIDO:" in t)
                if pedido_tag:
                    numero_pedido = pedido_tag.strip().split(':')[1].strip()
                    data_pedido_tag = pedido_tag.find_next_sibling('small')
                    if data_pedido_tag: data_pedido = data_pedido_tag.get_text(strip=True)
                b_tags = etiqueta_html.find_all('b')
                if len(b_tags) > 1:
                    destinatario_tag = b_tags[1]
                    nome_destinatario = destinatario_tag.get_text(strip=True)
                    endereco_tags = destinatario_tag.find_next_siblings('small')
                    if endereco_tags:
                        endereco_completo = " ".join([tag.get_text(strip=True) for tag in endereco_tags[:-1]])
                        cidade_uf = endereco_tags[-1].get_text(strip=True).split(' - ')
                        cidade_destinatario = cidade_uf[0]
                        uf_destinatario = cidade_uf[1] if len(cidade_uf) > 1 else ''
                nf_tag = etiqueta_html.find('b', string=lambda t: "NF:" in t)
                if nf_tag:
                    nf_text = nf_tag.get_text(strip=True)
                    if ":" in nf_text and len(nf_text.split(':')[1].strip()) > 0: numero_nf = nf_text.split(':')[1].strip()
                    elif nf_tag.next_sibling and isinstance(nf_tag.next_sibling, str) and len(nf_tag.next_sibling.strip()) > 0: numero_nf = nf_tag.next_sibling.strip()
                volume_tag = etiqueta_html.find(string=lambda t: "Vol.:" in t)
                if volume_tag:
                    volumes = volume_tag.strip().split(':')[1].strip().split('/')
                    volume_atual, volume_total = int(volumes[0]), int(volumes[1])
            except Exception as extract_error:
                print(f"--> Aviso: Erro menor ao extrair um campo da etiqueta. Alguns dados podem faltar. Erro: {extract_error}")
            
            sql_etiqueta = """
                INSERT INTO etiquetas (arquivo_id, ref_numero, numero_pedido, data_pedido, nome_destinatario, endereco_destinatario, cidade_destinatario, uf_destinatario, numero_nf, volume_atual, volume_total, html_content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cur.execute(sql_etiqueta, (arquivo_id, ref_numero, numero_pedido, data_pedido, nome_destinatario, endereco_completo, cidade_destinatario, uf_destinatario, numero_nf, volume_atual, volume_total, html_da_etiqueta))

        conn.commit()
        conn.close()
        print(f"{len(etiquetas_html)} etiquetas do ficheiro {nome_arquivo} salvas com detalhes.")

        with open(UPDATE_SIGNAL_FILE, "w") as f:
            f.write(str(datetime.now().timestamp()))

    except Exception as e:
        print(f"\n!!!!!! ERRO CRÍTICO AO PROCESSAR O FICHEIRO {caminho_do_arquivo} !!!!!!")
        traceback.print_exc()

class MeuHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            nome_arquivo = os.path.basename(event.src_path)
            if nome_arquivo.startswith('tmp') and nome_arquivo.endswith('.html'):
                time.sleep(1) 
                processar_arquivo_etiqueta(event.src_path)

if __name__ == "__main__":
    if DIRETORIO_MONITORADO is None:
        print("ERRO: Não foi possível determinar o diretório para monitoramento.")
        print("Verifique se o usuário tem permissões adequadas e se o diretório temp existe.")
        exit(1)
    
    event_handler = MeuHandler()
    observer = Observer()
    observer.schedule(event_handler, DIRETORIO_MONITORADO, recursive=False)
    print(f"Monitorando o diretório: {DIRETORIO_MONITORADO}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

