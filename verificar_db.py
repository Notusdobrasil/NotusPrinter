# verificar_db.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "etiquetas.db")

if not os.path.exists(DB_FILE):
    print(f"ERRO: O arquivo de banco de dados '{DB_FILE}' não foi encontrado!")
else:
    print(f"Analisando o banco de dados: {DB_FILE}\n")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("--- Conteúdo da tabela 'arquivos_processados' ---")
    try:
        arquivos = cur.execute("SELECT * FROM arquivos_processados").fetchall()
        if not arquivos:
            print("Nenhum dado encontrado.")
        else:
            for arquivo in arquivos:
                print(dict(arquivo))
    except sqlite3.OperationalError as e:
        print(f"Erro ao ler a tabela 'arquivos_processados': {e}")


    print("\n--- Conteúdo da tabela 'etiquetas' ---")
    try:
        etiquetas = cur.execute("SELECT * FROM etiquetas").fetchall()
        if not etiquetas:
            print("Nenhum dado encontrado.")
        else:
            for etiqueta in etiquetas:
                print(dict(etiqueta))
    except sqlite3.OperationalError as e:
        print(f"Erro ao ler a tabela 'etiquetas': {e}")

    conn.close()