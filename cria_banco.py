# cria_banco.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "etiquetas.db")

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Tabela de ficheiros permanece a mesma
cur.execute("""
    CREATE TABLE IF NOT EXISTS arquivos_processados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_arquivo TEXT NOT NULL,
        caminho_arquivo TEXT NOT NULL,
        data_processamento DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_etiquetas INTEGER,
        status TEXT NOT NULL DEFAULT 'novo' 
    )
""")

# Tabela de etiquetas com a nova coluna 'html_content'
cur.execute("""
    CREATE TABLE IF NOT EXISTS etiquetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arquivo_id INTEGER,
        ref_numero TEXT,
        numero_pedido TEXT,
        data_pedido TEXT,
        nome_destinatario TEXT,
        endereco_destinatario TEXT,
        cidade_destinatario TEXT,
        uf_destinatario TEXT,
        numero_nf TEXT,
        volume_atual INTEGER,
        volume_total INTEGER,
        html_content TEXT, -- <-- NOVA COLUNA
        FOREIGN KEY (arquivo_id) REFERENCES arquivos_processados (id)
    )
""")

print(f"Banco de dados '{DB_FILE}' criado com a nova estrutura (com html_content).")
conn.commit()
conn.close()
