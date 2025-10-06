import os
import sys
import webbrowser
import threading
import time
from flask import Flask, render_template, redirect, url_for, abort, jsonify, request
import sqlite3
from datetime import datetime, timezone, timedelta

# Importar o monitor
from monitor import DIRETORIO_MONITORADO, MeuHandler
from watchdog.observers import Observer

# --- CONFIGURAÇÕES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "etiquetas.db")
UPDATE_SIGNAL_FILE = os.path.join(BASE_DIR, "update_signal.txt")
CODIGO_REIMPRESSAO = "VIP123"

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_last_update_time():
    if os.path.exists(UPDATE_SIGNAL_FILE):
        with open(UPDATE_SIGNAL_FILE, "r") as f:
            try: return float(f.read())
            except (ValueError, TypeError): return 0.0
    return 0.0

def converter_utc_para_local(data_utc_str):
    """Converte data UTC do SQLite para horário local (Brasília UTC-3)"""
    try:
        # Parse da data UTC do SQLite
        data_utc = datetime.strptime(data_utc_str, '%Y-%m-%d %H:%M:%S')
        # Adiciona timezone UTC
        data_utc = data_utc.replace(tzinfo=timezone.utc)
        # Converte para horário de Brasília (UTC-3)
        brasilia_tz = timezone(timedelta(hours=-3))
        data_local = data_utc.astimezone(brasilia_tz)
        # Retorna formatado
        return data_local.strftime('%d/%m/%Y %H:%M:%S')
    except Exception:
        # Se houver erro, retorna a data original
        return data_utc_str

def start_file_monitor():
    """Inicia o monitor de arquivos em uma thread separada"""
    if DIRETORIO_MONITORADO is None:
        print("ERRO: Não foi possível determinar o diretório para monitoramento.")
        return None
    
    try:
        event_handler = MeuHandler()
        observer = Observer()
        observer.schedule(event_handler, DIRETORIO_MONITORADO, recursive=False)
        print(f"Monitorando o diretório: {DIRETORIO_MONITORADO}")
        observer.start()
        return observer
    except Exception as e:
        print(f"ERRO ao iniciar monitor: {e}")
        return None

def open_browser():
    """Abre o navegador após um pequeno delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

@app.route('/')
def index():
    conn = get_db_connection()
    arquivos_raw = conn.execute("""
        SELECT ap.id, ap.nome_arquivo, ap.data_processamento, ap.status, ap.total_etiquetas,
               (SELECT e.numero_pedido FROM etiquetas e WHERE e.arquivo_id = ap.id LIMIT 1) as pedido,
               (SELECT e.nome_destinatario FROM etiquetas e WHERE e.arquivo_id = ap.id LIMIT 1) as destinatario
        FROM arquivos_processados ap ORDER BY ap.id DESC
    """).fetchall()
    conn.close()
    
    # Converte as datas para horário local
    arquivos = []
    for arquivo in arquivos_raw:
        arquivo_dict = dict(arquivo)
        arquivo_dict['data_processamento'] = converter_utc_para_local(arquivo_dict['data_processamento'])
        arquivos.append(arquivo_dict)
    
    last_update = get_last_update_time()
    return render_template('index.html', arquivos=arquivos, last_update=last_update)

@app.route('/check-update/<float:last_known_time>')
def check_update(last_known_time):
    current_update_time = get_last_update_time()
    if current_update_time > last_known_time:
        return jsonify({'update_available': True})
    return jsonify({'update_available': False})

@app.route('/historico-pedido')
def historico_pedido():
    pedido_num = request.args.get('pedido_num')
    arquivo_id_atual = request.args.get('arquivo_id_atual', type=int)
    
    print(f"DEBUG: historico_pedido chamado com pedido_num='{pedido_num}', arquivo_id_atual={arquivo_id_atual}")
    print(f"DEBUG: Query args: {request.args}")
    print(f"DEBUG: URL completa: {request.url}")
    
    if not pedido_num or arquivo_id_atual is None:
        return jsonify({'error': 'Parâmetros inválidos'}), 400
    
    conn = get_db_connection()
    impressoes_anteriores = conn.execute("""
        SELECT e.id, e.volume_atual, e.volume_total, e.ref_numero, ap.nome_arquivo, ap.status
        FROM etiquetas e JOIN arquivos_processados ap ON e.arquivo_id = ap.id
        WHERE e.numero_pedido = ? AND e.arquivo_id != ?
        ORDER BY ap.id, e.volume_atual
    """, (pedido_num, arquivo_id_atual)).fetchall()
    conn.close()
    print(f"DEBUG: Encontradas {len(impressoes_anteriores)} impressões anteriores")
    return jsonify([dict(row) for row in impressoes_anteriores])

# --- ROTA DE AUTORIZAÇÃO ATUALIZADA ---
@app.route('/autorizar-reimpressao', methods=['POST'])
def autorizar_reimpressao():
    """Verifica o código e retorna uma resposta JSON."""
    codigo_fornecido = request.form.get('codigo')
    if codigo_fornecido == CODIGO_REIMPRESSAO:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Código inválido!'})

@app.route('/arquivo/<int:arquivo_id>')
def detalhes_arquivo(arquivo_id):
    conn = get_db_connection()
    arquivo_raw = conn.execute("SELECT * FROM arquivos_processados WHERE id = ?", (arquivo_id,)).fetchone()
    if arquivo_raw is None: abort(404)
    etiquetas = conn.execute("SELECT * FROM etiquetas WHERE arquivo_id = ? ORDER BY volume_atual", (arquivo_id,)).fetchall()
    conn.close()
    
    # Converte a data para horário local
    arquivo = dict(arquivo_raw)
    arquivo['data_processamento'] = converter_utc_para_local(arquivo['data_processamento'])
    
    return render_template('detalhes.html', arquivo=arquivo, etiquetas=etiquetas)

@app.route('/marcar_impresso/<int:arquivo_id>')
def marcar_como_impresso(arquivo_id):
    conn = get_db_connection()
    conn.execute("UPDATE arquivos_processados SET status = 'impresso' WHERE id = ?", (arquivo_id,))
    conn.commit()
    conn.close()
    with open(UPDATE_SIGNAL_FILE, "w") as f:
        f.write(str(datetime.now().timestamp()))
    return redirect(url_for('imprimir_arquivo', arquivo_id=arquivo_id))

@app.route('/imprimir/<int:arquivo_id>')
def imprimir_arquivo(arquivo_id):
    conn = get_db_connection()
    etiquetas = conn.execute("SELECT html_content FROM etiquetas WHERE arquivo_id = ? ORDER BY volume_atual", (arquivo_id,)).fetchall()
    conn.close()
    if not etiquetas: abort(404)
    conteudo_html_completo = "".join([etiqueta['html_content'] for etiqueta in etiquetas])
    return render_template('imprimir.html', conteudo_html=conteudo_html_completo)

@app.route('/imprimir-parcial/<int:arquivo_id>')
def imprimir_parcial(arquivo_id):
    conn = get_db_connection()
    etiquetas_atuais = conn.execute("SELECT numero_pedido, volume_atual FROM etiquetas WHERE arquivo_id = ?", (arquivo_id,)).fetchall()
    if not etiquetas_atuais: abort(404)
    
    pedido_num = etiquetas_atuais[0]['numero_pedido']
    volumes_atuais = {etiqueta['volume_atual'] for etiqueta in etiquetas_atuais}

    volumes_anteriores_rows = conn.execute("""
        SELECT e.volume_atual FROM etiquetas e
        JOIN arquivos_processados ap ON e.arquivo_id = ap.id
        WHERE e.numero_pedido = ? AND e.arquivo_id != ?
    """, (pedido_num, arquivo_id)).fetchall()
    volumes_anteriores = {row['volume_atual'] for row in volumes_anteriores_rows}

    volumes_nao_repetidos = sorted(list(volumes_atuais - volumes_anteriores))
    
    if not volumes_nao_repetidos:
        return "Não foram encontradas etiquetas não repetidas para este ficheiro.", 200

    placeholders = ','.join('?' for _ in volumes_nao_repetidos)
    query_parcial = f"SELECT html_content FROM etiquetas WHERE arquivo_id = ? AND volume_atual IN ({placeholders}) ORDER BY volume_atual"
    
    etiquetas_para_imprimir = conn.execute(query_parcial, [arquivo_id] + volumes_nao_repetidos).fetchall()
    
    conn.execute("UPDATE arquivos_processados SET status = 'impresso' WHERE id = ?", (arquivo_id,))
    conn.commit()
    conn.close()
    
    with open(UPDATE_SIGNAL_FILE, "w") as f:
        f.write(str(datetime.now().timestamp()))
        
    conteudo_html_parcial = "".join([etiqueta['html_content'] for etiqueta in etiquetas_para_imprimir])
    return render_template('imprimir.html', conteudo_html=conteudo_html_parcial)

if __name__ == '__main__':
    print("=" * 50)
    print("    NOTUS PRINTER - Sistema de Impressão")
    print("=" * 50)
    print("Iniciando servidor...")
    print("A aplicação será aberta automaticamente no navegador.")
    print("Para parar o servidor, pressione Ctrl+C")
    print("=" * 50)
    
    # Inicia o monitor de arquivos
    monitor_observer = start_file_monitor()
    
    # Inicia thread para abrir navegador
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Inicia o servidor Flask
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nParando servidor...")
        if monitor_observer:
            monitor_observer.stop()
            monitor_observer.join()
        print("Servidor parado.")
