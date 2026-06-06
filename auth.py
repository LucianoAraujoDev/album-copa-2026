# auth.py — Autenticação com persistência via SQLite (compatível com deploy)

import hashlib
import secrets
import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get("ALBUM_DB_PATH", "album_copa.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas se não existirem."""
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username    TEXT PRIMARY KEY,
            nome        TEXT NOT NULL,
            salt        TEXT NOT NULL,
            senha_hash  TEXT NOT NULL,
            criado_em   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS album (
            username    TEXT NOT NULL,
            figurinha   TEXT NOT NULL,
            tenho       INTEGER NOT NULL DEFAULT 0,
            repetidas   INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (username, figurinha),
            FOREIGN KEY (username) REFERENCES usuarios(username)
        );
    """)
    conn.commit()
    conn.close()


def _hash_senha(senha: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", senha.encode(), salt.encode(), 200_000
    ).hex()


# ── Usuários ────────────────────────────────────────────────────

def cadastrar_usuario(nome: str, username: str, senha: str) -> tuple[bool, str]:
    username = username.strip().lower()
    nome = nome.strip()

    if not username or not senha or not nome:
        return False, "Preencha todos os campos."
    if len(username) < 3:
        return False, "Usuário deve ter ao menos 3 caracteres."
    if len(senha) < 4:
        return False, "Senha deve ter ao menos 4 caracteres."
    if not username.replace("_", "").replace(".", "").isalnum():
        return False, "Usuário só pode conter letras, números, _ e ."

    init_db()
    conn = _get_conn()
    try:
        existe = conn.execute(
            "SELECT 1 FROM usuarios WHERE username = ?", (username,)
        ).fetchone()
        if existe:
            return False, "Este usuário já existe. Escolha outro."

        salt = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO usuarios VALUES (?, ?, ?, ?, ?)",
            (username, nome, salt, _hash_senha(senha, salt), datetime.now().isoformat())
        )
        conn.commit()
        return True, f"Conta criada! Bem-vindo(a), {nome}!"
    finally:
        conn.close()


def autenticar_usuario(username: str, senha: str) -> tuple[bool, str, dict]:
    username = username.strip().lower()
    init_db()
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE username = ?", (username,)
        ).fetchone()
        if not row:
            return False, "Usuário não encontrado.", {}
        if _hash_senha(senha, row["salt"]) != row["senha_hash"]:
            return False, "Senha incorreta.", {}
        return True, f"Bem-vindo(a) de volta, {row['nome']}!", dict(row)
    finally:
        conn.close()


# ── Álbum ────────────────────────────────────────────────────────

def carregar_dados_usuario(username: str) -> dict:
    """Retorna dict {figurinha: {tenho, repetidas}} do usuário."""
    init_db()
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT figurinha, tenho, repetidas FROM album WHERE username = ?",
            (username,)
        ).fetchall()
        return {
            row["figurinha"]: {"tenho": bool(row["tenho"]), "repetidas": row["repetidas"]}
            for row in rows
        }
    finally:
        conn.close()


def salvar_dados_usuario(username: str, dados: dict) -> None:
    """Salva/atualiza todas as figurinhas do usuário (upsert em lote)."""
    init_db()
    conn = _get_conn()
    try:
        conn.executemany(
            """INSERT INTO album (username, figurinha, tenho, repetidas)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(username, figurinha)
               DO UPDATE SET tenho = excluded.tenho, repetidas = excluded.repetidas""",
            [
                (username, fig, int(info.get("tenho", False)), info.get("repetidas", 0))
                for fig, info in dados.items()
            ]
        )
        conn.commit()
    finally:
        conn.close()


def listar_usuarios() -> list[dict]:
    init_db()
    conn = _get_conn()
    try:
        rows = conn.execute("SELECT username, nome, criado_em FROM usuarios").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
