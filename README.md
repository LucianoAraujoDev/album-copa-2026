# ⚽ Álbum Copa do Mundo 2026

App em **Python + Streamlit** com login por usuário para controlar figurinhas da Copa.

---

## 🚀 Opção 1 — Streamlit Community Cloud (gratuito, mais fácil)

### Pré-requisitos
- Conta no [GitHub](https://github.com)
- Conta no [Streamlit Cloud](https://streamlit.io/cloud)

### Passo a passo

1. **Crie um repositório no GitHub** (pode ser privado)
   - Vá em github.com → **New repository** → nome: `album-copa-2026`

2. **Faça upload dos arquivos** para o repositório
   (ou use Git: `git init`, `git add .`, `git commit -m "inicio"`, `git push`)

3. **Acesse** [share.streamlit.io](https://share.streamlit.io)

4. Clique em **"New app"** → conecte seu GitHub → selecione o repositório

5. Configure:
   - **Branch:** `main`
   - **Main file path:** `app.py`

6. Clique em **Deploy!** — em ~2 minutos o app está no ar.

> ⚠️ O Streamlit Cloud tem sistema de arquivos efêmero. O banco SQLite pode ser apagado em reinicializações. Para uso permanente, use Railway ou Render com volume.

---

## 🚀 Opção 2 — Railway (recomendado, volume persistente)

1. Crie conta em [railway.app](https://railway.app)
2. **New Project → Deploy from GitHub repo** → selecione o repositório
3. Railway detecta o `Dockerfile` automaticamente
4. Adicione um **Volume**: painel do serviço → **Volumes → Add Volume** → Mount path: `/app/data`
5. Em **Variables**: `ALBUM_DB_PATH=/app/data/album_copa.db`
6. **Settings → Networking → Generate Domain**

---

## 🚀 Opção 3 — Render

1. Crie conta em [render.com](https://render.com)
2. **New → Web Service** → conecte o repositório
3. Runtime: **Docker**
4. **Add Disk** → Mount Path: `/app/data`
5. Environment: `ALBUM_DB_PATH=/app/data/album_copa.db`
6. **Create Web Service**

---

## 💻 Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Acesse: `http://localhost:8501`

---

## 📁 Estrutura

```
album_copa/
├── app.py                  # App principal
├── auth.py                 # Autenticação + SQLite
├── data.py                 # Seções e figurinhas
├── utils.py                # Estatísticas
├── requirements.txt
├── Dockerfile
├── .gitignore
└── .streamlit/
    └── config.toml
```
