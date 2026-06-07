# auth.py — Autenticação com persistência via Supabase (PostgreSQL)

import hashlib
import os
import secrets
from datetime import datetime
import psycopg2
from psycopg2.extras import DictCursor
import streamlit as st

# Puxa a URL das Secrets do Streamlit (em desenvolvimento local, pode usar uma variável de ambiente)
DB_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")


def _get_conn():
    # Conecta ao PostgreSQL do Supabase
    conn = psycopg2.connect(DB_URL)
    return conn


def init_db():
    """Cria as tabelas se não existirem no Supabase. Chame apenas uma vez na inicialização do app."""
    conn = _get_conn()
    with conn.cursor() as cursor:
        cursor.execute(
            """
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
                FOREIGN KEY (username) REFERENCES usuarios(username) ON DELETE CASCADE
            );
        """
        )
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

    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT 1 FROM usuarios WHERE username = %s", (username,)
            )
            if cursor.fetchone():
                return False, "Este usuário já existe. Escolha outro."

            salt = secrets.token_hex(16)
            cursor.execute(
                "INSERT INTO usuarios VALUES (%s, %s, %s, %s, %s)",
                (
                    username,
                    nome,
                    salt,
                    _hash_senha(senha, salt),
                    datetime.now().isoformat(),
                ),
            )
        conn.commit()
        return True, f"Conta criada! Bem-vindo(a), {nome}!"
    finally:
        conn.close()


def autenticar_usuario(username: str, senha: str) -> tuple[bool, str, dict]:
    username = username.strip().lower()
    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE username = %s", (username,)
            )
            row = cursor.fetchone()
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
    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT figurinha, tenho, repetidas FROM album WHERE username = %s",
                (username,),
            )
            rows = cursor.fetchall()
            return {
                row["figurinha"]: {
                    "tenho": bool(row["tenho"]),
                    "repetidas": row["repetidas"],
                }
                for row in rows
            }
    finally:
        conn.close()


def salvar_dados_usuario(username: str, dados: dict) -> None:
    """Salva/atualiza todas as figurinhas do usuário (upsert em lote) no Postgres."""
    conn = _get_conn()
    try:
        with conn.cursor() as cursor:
            # O executemany do psycopg2 usa uma sintaxe ligeiramente diferente para os placeholders (%s)
            cursor.executemany(
                """INSERT INTO album (username, figurinha, tenho, repetidas)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT(username, figurinha)
                   DO UPDATE SET tenho = EXCLUDED.tenho, repetidas = EXCLUDED.repetidas""",
                [
                    (
                        username,
                        fig,
                        int(info.get("tenho", False)),
                        info.get("repetidas", 0),
                    )
                    for fig, info in dados.items()
                ],
            )
        conn.commit()
    finally:
        conn.close()


def listar_usuarios() -> list[dict]:
    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT username, nome, criado_em FROM usuarios")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
    finally:
        conn.close()
