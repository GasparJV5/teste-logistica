from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mdr_v2.db"
FRONTEND_DIR = BASE_DIR.parent / "frontend"
BACKUP_PATH = BASE_DIR / "backup_mdr_v2.json"
MAIN_HTML = "index.html"

app = Flask(__name__, static_folder=None)
CORS(app)


# =========================================
# Helpers
# =========================================

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


def empty_state():
    return {
        "blocks": [],
        "analyses": [],
        "imports": [],
        "activeBlockId": None,
        "counters": {
            "processSeq": 0,
            "analysisSeq": 0
        }
    }


def save_current_state(data: dict, updated_at: str | None = None):
    if updated_at is None:
        updated_at = now_iso()

    payload = json.dumps(data, ensure_ascii=False)

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO app_state (id, data, updated_at)
        VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            data = excluded.data,
            updated_at = excluded.updated_at
    """, (payload, updated_at))
    conn.commit()
    conn.close()

    return updated_at


def load_current_state():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT data, updated_at FROM app_state WHERE id = 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row["data"])


def write_backup_file(data: dict, created_at: str | None = None):
    if created_at is None:
        created_at = now_iso()

    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    size_bytes = BACKUP_PATH.stat().st_size if BACKUP_PATH.exists() else 0

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backup_log (created_at, file_path, size_bytes)
        VALUES (?, ?, ?)
    """, (created_at, str(BACKUP_PATH), size_bytes))
    conn.commit()
    conn.close()

    return size_bytes


def load_backup_file():
    if not BACKUP_PATH.exists():
        return None

    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_current_payload_for_hash():
    data = load_current_state()
    if data is not None:
        return data

    backup_data = load_backup_file()
    if backup_data is not None:
        return backup_data

    return empty_state()


def make_hash(data: dict):
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# =========================================
# Frontend routes
# =========================================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, MAIN_HTML)


@app.route("/<path:path>")
def frontend_files(path):
    target = FRONTEND_DIR / path

    if target.exists() and target.is_file():
        return send_from_directory(FRONTEND_DIR, path)

    return send_from_directory(FRONTEND_DIR, MAIN_HTML)


# =========================================
# API routes
# =========================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "db": str(DB_PATH),
        "backup": str(BACKUP_PATH),
        "frontend_dir": str(FRONTEND_DIR),
        "main_html": MAIN_HTML,
        "port": 5001
    })


@app.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": "V2",
        "db": str(DB_PATH),
        "port": 5001
    })


@app.route("/hash", methods=["GET"])
def hash_state():
    data = get_current_payload_for_hash()
    return jsonify({
        "status": "ok",
        "hash": make_hash(data)
    })


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "erro",
            "message": "JSON inválido. Envie um objeto com a base do sistema."
        }), 400

    updated_at = save_current_state(data)

    return jsonify({
        "status": "ok",
        "message": "Estado salvo no banco com sucesso.",
        "updated_at": updated_at
    })


@app.route("/load", methods=["GET"])
def load():
    data = load_current_state()

    if data is not None:
        return jsonify({
            "status": "ok",
            "source": "database",
            "data": data
        }), 200

    backup_data = load_backup_file()
    if backup_data is not None:
        return jsonify({
            "status": "ok",
            "source": "backup_file",
            "data": backup_data
        }), 200

    return jsonify({
        "status": "empty",
        "source": "none",
        "message": "Nenhum estado salvo encontrado no banco ou no backup.",
        "data": empty_state()
    }), 200


@app.route("/backup", methods=["POST"])
def backup():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        data = load_current_state()

    if not isinstance(data, dict):
        backup_data = load_backup_file()
        if isinstance(backup_data, dict):
            data = backup_data

    if not isinstance(data, dict):
        return jsonify({
            "status": "erro",
            "message": "Nenhum dado disponível para gerar backup."
        }), 400

    updated_at = now_iso()
    save_current_state(data, updated_at=updated_at)
    size_bytes = write_backup_file(data, created_at=updated_at)

    return jsonify({
        "status": "ok",
        "message": "Backup gerado com sucesso.",
        "backup_file": str(BACKUP_PATH),
        "size_bytes": size_bytes,
        "updated_at": updated_at
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


@app.route("/download-backup", methods=["GET"])
def download_backup():
    if not BACKUP_PATH.exists():
        return jsonify({
            "status": "erro",
            "message": "Arquivo de backup não encontrado."
        }), 404

    return send_from_directory(BASE_DIR, BACKUP_PATH.name, as_attachment=True)


# =========================================
# Main
# =========================================

if __name__ == "__main__":
    init_db()
    print("================================")
    print("MDR Ecosystem Backend V2 iniciado")
    print(f"DB: {DB_PATH}")
    print(f"Backup: {BACKUP_PATH}")
    print(f"Frontend: {FRONTEND_DIR}")
    print(f"Main HTML: {MAIN_HTML}")
    print("API teste rodando em: http://0.0.0.0:5501")
    print("================================")
    app.run(host="0.0.0.0", port=5501, debug=True)