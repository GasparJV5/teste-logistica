from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mdr_v2.db"
FRONTEND_DIR = BASE_DIR.parent / "frontend"
BACKUP_PATH = BASE_DIR / "backup_mdr_v2.json"
MAIN_HTML = "index.html"

app = Flask(__name__)
CORS(app)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            data TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backup_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            file_path TEXT NOT NULL,
            size_bytes INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def now_iso():
    return datetime.now().isoformat(timespec="seconds")

def save_current_state(data: dict):
    payload = json.dumps(data, ensure_ascii=False)

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO app_state (id, data, updated_at)
        VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            data = excluded.data,
            updated_at = excluded.updated_at
    """, (payload, now_iso()))
    conn.commit()
    conn.close()

def load_current_state():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT data, updated_at FROM app_state WHERE id = 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row["data"])

def write_backup_file(data: dict):
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    size_bytes = BACKUP_PATH.stat().st_size if BACKUP_PATH.exists() else 0

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backup_log (created_at, file_path, size_bytes)
        VALUES (?, ?, ?)
    """, (now_iso(), str(BACKUP_PATH), size_bytes))
    conn.commit()
    conn.close()

    return size_bytes

def load_backup_file():
    if not BACKUP_PATH.exists():
        return None

    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, MAIN_HTML)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "db": str(DB_PATH),
        "backup": str(BACKUP_PATH),
        "main_html": MAIN_HTML
    })

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "erro",
            "message": "JSON inválido. Envie um objeto com a base do sistema."
        }), 400

    save_current_state(data)

    return jsonify({
        "status": "ok",
        "message": "Estado salvo no banco com sucesso.",
        "updated_at": now_iso()
    })

@app.route("/load", methods=["GET"])
def load():
    data = load_current_state()

    if data is not None:
        return jsonify({
            "status": "ok",
            "source": "database",
            "data": data
        })

    backup_data = load_backup_file()
    if backup_data is not None:
        return jsonify({
            "status": "ok",
            "source": "backup_file",
            "data": backup_data
        })

    return jsonify({
        "status": "empty",
        "message": "Nenhum estado salvo encontrado no banco ou no backup."
    }), 404

@app.route("/backup", methods=["POST"])
def backup():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        data = load_current_state()

    if not isinstance(data, dict):
        return jsonify({
            "status": "erro",
            "message": "Nenhum dado disponível para gerar backup."
        }), 400

    save_current_state(data)
    size_bytes = write_backup_file(data)

    return jsonify({
        "status": "ok",
        "message": "Backup gerado com sucesso.",
        "backup_file": str(BACKUP_PATH),
        "size_bytes": size_bytes,
        "updated_at": now_iso()
    })

@app.route("/backup-info", methods=["GET"])
def backup_info():
    exists = BACKUP_PATH.exists()
    size_bytes = BACKUP_PATH.stat().st_size if exists else 0

    return jsonify({
        "status": "ok",
        "exists": exists,
        "backup_file": str(BACKUP_PATH),
        "size_bytes": size_bytes
    })
@app.route("/version")
def version():
    return jsonify({
        "version": "V2",
        "db": str(DB_PATH),
        "port": 5001
    })

@app.route("/download-backup", methods=["GET"])
def download_backup():
    if not BACKUP_PATH.exists():
        return jsonify({
            "status": "erro",
            "message": "Arquivo de backup não encontrado."
        }), 404

    return send_from_directory(BASE_DIR, BACKUP_PATH.name, as_attachment=True)

if __name__ == "__main__":
    init_db()
    print("================================")
    print("MDR Ecosystem Backend V2 iniciado")
    print(f"DB: {DB_PATH}")
    print(f"Backup: {BACKUP_PATH}")
    print(f"Main HTML: {MAIN_HTML}")
    print("================================")
    app.run(host="0.0.0.0", port=5001, debug=True)