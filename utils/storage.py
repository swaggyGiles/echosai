"""SQLite persistence for EchoesAI prototype. Use fictional/demo records only."""
import sqlite3, json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "echoesai.db"
UPLOAD_DIR = ROOT / "data" / "uploads"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_storage():
    with get_connection() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT, display_name TEXT NOT NULL UNIQUE,
            age INTEGER, sex TEXT, notes TEXT DEFAULT '', created_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS eeg_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER,
            original_filename TEXT NOT NULL, stored_path TEXT, file_type TEXT,
            sampling_rate REAL, channels TEXT, duration_seconds REAL, notes TEXT DEFAULT '',
            uploaded_at TEXT NOT NULL, FOREIGN KEY(patient_id) REFERENCES patients(patient_id) ON DELETE SET NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT, record_id INTEGER,
            model_version TEXT, predicted_class TEXT, confidence REAL,
            probabilities_json TEXT DEFAULT '{}', status TEXT DEFAULT 'demo', created_at TEXT NOT NULL,
            FOREIGN KEY(record_id) REFERENCES eeg_records(record_id) ON DELETE CASCADE)""")
        c.commit()

def list_patients(search=""):
    with get_connection() as c:
        if search:
            rows = c.execute("SELECT * FROM patients WHERE display_name LIKE ? OR notes LIKE ? ORDER BY patient_id DESC", (f"%{search}%",f"%{search}%")).fetchall()
        else:
            rows = c.execute("SELECT * FROM patients ORDER BY patient_id DESC").fetchall()
        return [dict(r) for r in rows]

def add_patient(display_name, age=None, sex=None, notes=""):
    with get_connection() as c:
        cur = c.execute("INSERT INTO patients(display_name,age,sex,notes,created_at) VALUES(?,?,?,?,?)",
            (display_name, age, sex, notes, datetime.now().isoformat(timespec="seconds")))
        c.commit()
        return cur.lastrowid

def update_patient(patient_id, display_name, age=None, sex=None, notes=""):
    with get_connection() as c:
        c.execute("UPDATE patients SET display_name=?, age=?, sex=?, notes=? WHERE patient_id=?",
                  (display_name, age, sex, notes, patient_id))
        c.commit()

def delete_patient(patient_id):
    with get_connection() as c:
        c.execute("UPDATE eeg_records SET patient_id=NULL WHERE patient_id=?", (patient_id,))
        c.execute("DELETE FROM patients WHERE patient_id=?", (patient_id,))
        c.commit()

def list_eeg_records():
    with get_connection() as c:
        q = """SELECT e.*, p.display_name AS patient_name FROM eeg_records e
               LEFT JOIN patients p ON e.patient_id=p.patient_id ORDER BY e.record_id DESC"""
        return [dict(r) for r in c.execute(q).fetchall()]

def add_eeg_record(patient_id, original_filename, stored_path="", file_type="unknown",
                   sampling_rate=None, channels="", duration_seconds=None, notes=""):
    with get_connection() as c:
        cur = c.execute("""INSERT INTO eeg_records
            (patient_id,original_filename,stored_path,file_type,sampling_rate,channels,duration_seconds,notes,uploaded_at)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (patient_id, original_filename, stored_path, file_type, sampling_rate, channels,
             duration_seconds, notes, datetime.now().isoformat(timespec="seconds")))
        c.commit()
        return cur.lastrowid

def delete_eeg_record(record_id):
    with get_connection() as c:
        row = c.execute("SELECT stored_path FROM eeg_records WHERE record_id=?", (record_id,)).fetchone()
        c.execute("DELETE FROM eeg_records WHERE record_id=?", (record_id,))
        c.commit()
    if row and row["stored_path"]:
        try:
            p = Path(row["stored_path"]).resolve()
            if UPLOAD_DIR.resolve() in p.parents and p.is_file(): p.unlink()
        except OSError:
            pass

def list_predictions():
    with get_connection() as c:
        q = """SELECT pr.*, e.original_filename, e.patient_id, p.display_name AS patient_name
               FROM predictions pr LEFT JOIN eeg_records e ON pr.record_id=e.record_id
               LEFT JOIN patients p ON e.patient_id=p.patient_id ORDER BY pr.prediction_id DESC"""
        return [dict(r) for r in c.execute(q).fetchall()]

def add_prediction(record_id, model_version, predicted_class, confidence=None, probabilities=None, status="demo"):
    with get_connection() as c:
        cur = c.execute("""INSERT INTO predictions
            (record_id,model_version,predicted_class,confidence,probabilities_json,status,created_at)
            VALUES(?,?,?,?,?,?,?)""",
            (record_id, model_version, predicted_class, confidence, json.dumps(probabilities or {}),
             status, datetime.now().isoformat(timespec="seconds")))
        c.commit()
        return cur.lastrowid
