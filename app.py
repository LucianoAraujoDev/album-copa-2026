import streamlit as st
import json
import os
from data import SECOES_COPA
from utils import calcular_estatisticas
from auth import (
    cadastrar_usuario, autenticar_usuario,
    carregar_dados_usuario, salvar_dados_usuario
)

# --- Configuração da página ---
st.set_page_config(
    page_title="Álbum Copa do Mundo",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS Global ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Open Sans', sans-serif; }
h1, h2, h3 { font-family: 'Oswald', sans-serif; letter-spacing: 1px; }

.hero-header {
    background: linear-gradient(135deg, #1a472a 0%, #2d6a4f 40%, #c8a900 100%);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem;
    color: white; display: flex; align-items: center; gap: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero-title {
    font-family: 'Oswald', sans-serif; font-size: 2.4rem; font-weight: 700;
    margin: 0; letter-spacing: 2px; text-transform: uppercase;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.hero-sub { font-size: 1rem; opacity: 0.85; margin: 0; }

/* Login */
.login-wrap {
    max-width: 440px; margin: 2rem auto; background: white;
    border-radius: 20px; padding: 2.5rem 2.5rem 2rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.13);
    border-top: 6px solid #1a472a;
}
.login-logo { text-align: center; font-size: 4rem; margin-bottom: 0.5rem; }
.login-title {
    font-family: 'Oswald', sans-serif; font-size: 1.8rem; font-weight: 700;
    text-align: center; color: #1a472a; text-transform: uppercase;
    letter-spacing: 2px; margin-bottom: 0.2rem;
}
.login-sub { text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 1.5rem; }

/* Stats */
.stat-card {
    background: white; border-radius: 12px; padding: 1.2rem 1.5rem;
    text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #1a472a; margin-bottom: 1rem;
}
.stat-card.gold { border-left-color: #c8a900; }
.stat-card.blue { border-left-color: #1a6fc4; }
.stat-card.red  { border-left-color: #c0392b; }
.stat-number { font-family: 'Oswald', sans-serif; font-size: 2.2rem; font-weight: 700; color: #1a472a; line-height: 1; }
.stat-number.gold { color: #c8a900; }
.stat-number.blue { color: #1a6fc4; }
.stat-number.red  { color: #c0392b; }
.stat-label { font-size: 0.78rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.3rem; }

.progress-bar-container {
    background: #e9ecef; border-radius: 50px; height: 18px;
    overflow: hidden; margin: 0.5rem 0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}
.progress-bar-fill {
    height: 100%; border-radius: 50px;
    background: linear-gradient(90deg, #1a472a, #2d6a4f, #c8a900);
    display: flex; align-items: center; justify-content: flex-end;
    padding-right: 8px; font-size: 0.7rem; color: white; font-weight: 600;
}
.secao-header {
    background: linear-gradient(90deg, #1a472a, #2d6a4f);
    color: white; padding: 0.7rem 1.2rem; border-radius: 10px;
    margin: 1rem 0 0.5rem 0; font-family: 'Oswald', sans-serif;
    font-size: 1.1rem; letter-spacing: 1px; text-transform: uppercase;
}
.badge-repetida {
    background: #c8a900; color: #1a472a; border-radius: 50%;
    padding: 2px 7px; font-size: 0.75rem; font-weight: 700; display: inline-block;
}
.user-chip {
    background: rgba(255,255,255,0.15); border-radius: 20px;
    padding: 0.3rem 0.8rem; font-size: 0.85rem;
    display: inline-block; margin-bottom: 0.5rem;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a472a 0%, #0d2b18 100%);
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
.sidebar-title {
    font-family: 'Oswald', sans-serif; font-size: 1.4rem; letter-spacing: 2px;
    text-transform: uppercase; color: #c8a900 !important;
    text-align: center; margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = ""


# ─────────────────────────────────────────────
# TELA DE LOGIN / CADASTRO
# ─────────────────────────────────────────────
def tela_login():
    st.markdown("""
    <div class="hero-header">
        <div style="font-size:4rem;">🏆</div>
        <div>
            <p class="hero-title">Álbum Copa do Mundo 2026</p>
            <p class="hero-sub">Faça login para acessar seu álbum pessoal de figurinhas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        aba = st.tabs(["🔑  Entrar", "📝  Criar conta"])

        # ── ABA LOGIN ──
        with aba[0]:
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            username = st.text_input("Usuário", placeholder="seu_usuario", key="login_user")
            senha    = st.text_input("Senha", type="password", placeholder="••••••", key="login_senha")

            col_b1, col_b2 = st.columns([3, 1])
            with col_b1:
                entrar = st.button("Entrar ⚽", use_container_width=True, type="primary", key="btn_entrar")
            
            if entrar:
                if not username or not senha:
                    st.error("Preencha usuário e senha.")
                else:
                    ok, msg, usuario_info = autenticar_usuario(username, senha)
                    if ok:
                        st.session_state.logado = True
                        st.session_state.usuario = username
                        st.session_state.nome_usuario = usuario_info.get("nome", username)
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        # ── ABA CADASTRO ──
        with aba[1]:
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            nome_novo     = st.text_input("Seu nome", placeholder="Ex: João Silva", key="cad_nome")
            username_novo = st.text_input("Usuário", placeholder="Ex: joaosilva (sem espaços)", key="cad_user")
            senha_nova    = st.text_input("Senha", type="password", placeholder="Mínimo 4 caracteres", key="cad_senha")
            senha_conf    = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha", key="cad_conf")

            cadastrar = st.button("Criar conta 🎉", use_container_width=True, type="primary", key="btn_cadastrar")

            if cadastrar:
                if senha_nova != senha_conf:
                    st.error("As senhas não coincidem.")
                else:
                    ok, msg = cadastrar_usuario(nome_novo, username_novo, senha_nova)
                    if ok:
                        st.success(f"✅ {msg} Agora faça login na aba 'Entrar'.")
                    else:
                        st.error(f"❌ {msg}")

    st.markdown("<div style='text-align:center; color:#aaa; margin-top:3rem; font-size:0.8rem;'>🌍 México · Canadá · Estados Unidos &nbsp;|&nbsp; Copa do Mundo 2026</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# APP PRINCIPAL (usuário logado)
# ─────────────────────────────────────────────
def app_principal():
    username   = st.session_state.usuario
    nome       = st.session_state.nome_usuario
    dados      = carregar_dados_usuario(username)

    def salvar(d):
        salvar_dados_usuario(username, d)

    stats = calcular_estatisticas(dados, SECOES_COPA)

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown('<p class="sidebar-title">⚽ Copa 2026</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-chip">👤 {nome}</div>', unsafe_allow_html=True)
        st.markdown("---")
        pagina = st.radio(
            "Navegar para:",
            ["🏠 Painel Geral", "📖 Meu Álbum", "🔁 Repetidas", "📊 Estatísticas", "🔄 Importar / Exportar"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        pct = stats["percentual"]
        st.markdown(f"""
        <div style='text-align:center; padding:0.5rem;'>
            <div style='font-size:0.8rem; color:#aed9b8; margin-bottom:4px;'>PROGRESSO DO ÁLBUM</div>
            <div style='font-family:Oswald; font-size:2rem; color:#c8a900;'>{pct:.1f}%</div>
            <div style='font-size:0.75rem; color:#aed9b8;'>{stats['total_tenho']} de {stats['total_album']} figurinhas</div>
        </div>""", unsafe_allow_html=True)
        st.progress(pct / 100)
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True, key="btn_sair"):
            st.session_state.logado = False
            st.session_state.usuario = None
            st.session_state.nome_usuario = ""
            st.rerun()

    # ── HEADER ──
    st.markdown(f"""
    <div class="hero-header">
        <div style="font-size:4rem;">🏆</div>
        <div>
            <p class="hero-title">Álbum Copa do Mundo 2026</p>
            <p class="hero-sub">Olá, <strong>{nome}</strong>! Seu álbum está {pct:.1f}% completo.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════
    # PAINEL GERAL
    # ══════════════════════════════════════
    if pagina == "🏠 Painel Geral":
        c1, c2, c3, c4 = st.columns(4)
        cards = [
            (c1, "green", stats['total_album'],    "Total do Álbum",  ""),
            (c2, "blue",  stats['total_tenho'],    "Que eu Tenho",    "blue"),
            (c3, "red",   stats['total_faltam'],   "Faltam",          "red"),
            (c4, "gold",  stats['total_repetidas'],"Repetidas",       "gold"),
        ]
        for col, cls, val, label, num_cls in cards:
            with col:
                st.markdown(f"""
                <div class="stat-card {cls}">
                    <div class="stat-number {num_cls}">{val}</div>
                    <div class="stat-label">{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📦 Progresso por Seção")
        for secao in SECOES_COPA:
            figs  = secao["figurinhas"]
            tenho = sum(1 for f in figs if dados.get(str(f), {}).get("tenho", False))
            total = len(figs)
            pct_s = (tenho / total * 100) if total > 0 else 0
            reps  = sum(dados.get(str(f), {}).get("repetidas", 0) for f in figs)

            cn, cb, cnum = st.columns([2, 5, 1])
            with cn:
                st.markdown(f"**{secao['emoji']} {secao['nome']}**")
                if reps > 0:
                    st.caption(f"🔁 {reps} repetidas")
            with cb:
                st.markdown(f"""
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width:{pct_s:.1f}%">
                        {'&nbsp;'+str(round(pct_s))+'%' if pct_s > 10 else ''}
                    </div>
                </div>""", unsafe_allow_html=True)
            with cnum:
                st.markdown(f"**{tenho}/{total}**")

    # ══════════════════════════════════════
    # MEU ÁLBUM
    # ══════════════════════════════════════
    elif pagina == "📖 Meu Álbum":
        st.markdown("### 📖 Marcar Minhas Figurinhas")
        st.caption("Clique para marcar que você tem. Use o campo 🔁 para registrar repetidas.")

        # Criamos o seletor apenas com os nomes das seções para evitar quebras no split
        secao_sel = st.selectbox(
            "Filtrar por seção:",
            ["Todas"] + [f"{s['emoji']} {s['nome']}" for s in SECOES_COPA]
        )
        
        # Filtragem corrigida de forma segura usando partição
        mostrar = SECOES_COPA if secao_sel == "Todas" else [
            s for s in SECOES_COPA if s["nome"] == secao_sel.split(" ", 1)[1]
        ]

        for secao in mostrar:
            figs  = secao["figurinhas"]
            tenho_c = sum(1 for f in figs if dados.get(str(f), {}).get("tenho", False))
            total   = len(figs)
            st.markdown(f'<div class="secao-header">{secao["emoji"]} {secao["nome"]} &nbsp;·&nbsp; {tenho_c}/{total}</div>', unsafe_allow_html=True)

            cols_por_linha = 8
            for i in range(0, len(figs), cols_por_linha):
                lote = figs[i:i + cols_por_linha]
                cols = st.columns(len(lote))
                for j, fig in enumerate(lote):
                    key   = str(fig)
                    info  = dados.get(key, {"tenho": False, "repetidas": 0})
                    tenho = info.get("tenho", False)
                    reps  = info.get("repetidas", 0)
                    
                    # Criamos um ID limpo para o Streamlit substituindo espaços e emojis
                    # "🇲🇽 1" vira um ID seguro como "fig_id_1" ou baseado no hash da string
                    id_seguro = f"fig_{hash(key)}"
                    id_rep_seguro = f"rep_{hash(key)}"
                    
                    with cols[j]:
                        if st.button(
                            f"{'✅' if tenho else '○'} {fig}",
                            key=id_seguro,
                            help=f"Figurinha {fig} {'(tenho)' if tenho else '(não tenho)'}",
                            use_container_width=True,
                            type="primary" if tenho else "secondary"
                        ):
                            if key not in dados:
                                dados[key] = {"tenho": False, "repetidas": 0}
                            dados[key]["tenho"] = not tenho
                            if not dados[key]["tenho"]:
                                dados[key]["repetidas"] = 0
                            salvar(dados)
                            st.rerun()
                            
                        if tenho:
                            rep_val = st.number_input(
                                "🔁", min_value=0, max_value=99, value=reps,
                                key=id_rep_seguro, label_visibility="collapsed", step=1
                            )
                            if rep_val != reps:
                                dados[key]["repetidas"] = rep_val
                                salvar(dados)
                                st.rerun()

        st.markdown("---")
        ca, cb2 = st.columns(2)
        with ca:
            if st.button("✅ Marcar TODAS desta seção como tenho", use_container_width=True):
                for secao in mostrar:
                    for fig in secao["figurinhas"]:
                        k = str(fig)
                        if k not in dados:
                            dados[k] = {"tenho": False, "repetidas": 0}
                        dados[k]["tenho"] = True
                salvar(dados)
                st.success("Todas marcadas!")
                st.rerun()
        with cb2:
            if st.button("❌ Desmarcar TODAS desta seção", use_container_width=True, type="secondary"):
                for secao in mostrar:
                    for fig in secao["figurinhas"]:
                        dados[str(fig)] = {"tenho": False, "repetidas": 0}
                salvar(dados)
                st.warning("Todas desmarcadas.")
                st.rerun()

    # ══════════════════════════════════════
    # REPETIDAS
    # ══════════════════════════════════════
    elif pagina == "🔁 Repetidas":
        st.markdown("### 🔁 Minhas Figurinhas Repetidas")
        st.caption("Ótimas para trocar com amigos!")

        repetidas_lista = [
            {"secao": s["nome"], "emoji": s["emoji"], "figurinha": f,
             "quantidade": dados.get(str(f), {}).get("repetidas", 0)}
            for s in SECOES_COPA for f in s["figurinhas"]
            if dados.get(str(f), {}).get("tenho") and dados.get(str(f), {}).get("repetidas", 0) > 0
        ]

        if not repetidas_lista:
            st.info("🎉 Nenhuma repetida ainda! Vá em **Meu Álbum** para marcar suas repetidas.")
        else:
            total_rep = sum(r["quantidade"] for r in repetidas_lista)
            st.success(f"**{len(repetidas_lista)} figurinhas** repetidas — **{total_rep} unidades** para trocar!")

            secoes_com_rep = {}
            for r in repetidas_lista:
                sec = f"{r['emoji']} {r['secao']}"
                secoes_com_rep.setdefault(sec, []).append(r)

            for sec_nome, items in secoes_com_rep.items():
                st.markdown(f'<div class="secao-header">{sec_nome}</div>', unsafe_allow_html=True)
                cols = st.columns(6)
                for idx, item in enumerate(items):
                    with cols[idx % 6]:
                        st.markdown(f"""
                        <div style='background:#fffbea; border:2px solid #c8a900; border-radius:10px;
                                    padding:0.6rem; text-align:center; margin-bottom:0.5rem;'>
                            <div style='font-family:Oswald; font-size:1.3rem; color:#1a472a;'>{item['figurinha']}</div>
                            <div class='badge-repetida'>x{item['quantidade']}</div>
                        </div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 📋 Lista para compartilhar")
            lista_txt = f"🔁 REPETIDAS DE {nome.upper()} — Copa 2026\n" + "="*40 + "\n"
            for sec_nome, items in secoes_com_rep.items():
                lista_txt += f"\n{sec_nome}:\n  " + ", ".join(f"{i['figurinha']}(x{i['quantidade']})" for i in items) + "\n"
            lista_txt += f"\nTotal: {len(repetidas_lista)} figurinhas ({total_rep} unidades)"
            st.text_area("Copie e envie:", lista_txt, height=200)

    # ══════════════════════════════════════
    # ESTATÍSTICAS
    # ══════════════════════════════════════
    elif pagina == "📊 Estatísticas":
        import pandas as pd
        st.markdown("### 📊 Estatísticas Detalhadas")

        rows = []
        for secao in SECOES_COPA:
            figs  = secao["figurinhas"]
            tenho = sum(1 for f in figs if dados.get(str(f), {}).get("tenho", False))
            reps  = sum(dados.get(str(f), {}).get("repetidas", 0) for f in figs)
            pct_s = round(tenho / len(figs) * 100, 1) if figs else 0
            rows.append({
                "Seção": f"{secao['emoji']} {secao['nome']}",
                "Total": len(figs), "Tenho": tenho,
                "Faltam": len(figs) - tenho, "Repetidas": reps, "Completo (%)": pct_s
            })
        df = __import__("pandas").DataFrame(rows)
        st.dataframe(
            df.style.background_gradient(subset=["Completo (%)"], cmap="Greens")
                    .format({"Completo (%)": "{:.1f}%"}),
            use_container_width=True, hide_index=True
        )

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🏅 Mais completas")
            for _, row in df.sort_values("Completo (%)", ascending=False).head(5).iterrows():
                st.markdown(f"**{row['Seção']}** — {row['Completo (%)']:.1f}%")
                st.progress(row["Completo (%)"] / 100)
        with c2:
            st.markdown("#### 🎯 Mais incompletas")
            for _, row in df.sort_values("Faltam", ascending=False).head(5).iterrows():
                st.markdown(f"**{row['Seção']}** — faltam **{row['Faltam']}**")
                st.progress((row["Total"] - row["Faltam"]) / row["Total"])

        st.markdown("---")
        st.markdown("#### 🔍 Figurinhas que faltam")
        faltam = [f"{s['emoji']} {f}" for s in SECOES_COPA for f in s["figurinhas"]
                  if not dados.get(str(f), {}).get("tenho", False)]
        if faltam:
            st.info(f"Faltam **{len(faltam)}** figurinhas.")
            cols = st.columns(5)
            for idx, f in enumerate(faltam):
                cols[idx % 5].markdown(f"• {f}")
        else:
            st.success("🏆 ÁLBUM COMPLETO! Parabéns!")

    # ══════════════════════════════════════
    # IMPORTAR / EXPORTAR
    # ══════════════════════════════════════
    elif pagina == "🔄 Importar / Exportar":
        st.markdown("### 🔄 Importar e Exportar Dados")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📤 Exportar")
            st.download_button(
                "⬇️ Baixar meus dados (JSON)",
                data=json.dumps(dados, ensure_ascii=False, indent=2),
                file_name=f"album_copa_2026_{username}.json",
                mime="application/json", use_container_width=True
            )
            faltam_txt = f"FALTAM — {nome.upper()} — Copa 2026\n" + "="*35 + "\n"
            for secao in SECOES_COPA:
                fs = [str(f) for f in secao["figurinhas"] if not dados.get(str(f), {}).get("tenho", False)]
                if fs:
                    faltam_txt += f"\n{secao['emoji']} {secao['nome']}:\n  " + ", ".join(fs) + "\n"
            st.download_button(
                "⬇️ Baixar lista de faltantes (TXT)",
                data=faltam_txt, file_name=f"faltam_copa_2026_{username}.txt",
                mime="text/plain", use_container_width=True
            )

        with c2:
            st.markdown("#### 📥 Importar")
            uploaded = st.file_uploader("Escolha o arquivo JSON:", type=["json"])
            if uploaded:
                try:
                    dados_imp = json.loads(uploaded.read())
                    if st.button("✅ Confirmar importação", use_container_width=True, type="primary"):
                        salvar(dados_imp)
                        st.success("Importado com sucesso!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

        st.markdown("---")
        st.markdown("#### ⚠️ Resetar meu álbum")
        st.warning("Isso apaga **todo o seu progresso** pessoal.")
        confirmar = st.checkbox("Confirmo que quero resetar meu álbum")
        if confirmar:
            if st.button("🗑️ Resetar meu álbum", type="primary"):
                salvar({})
                st.success("Álbum resetado.")
                st.rerun()


# ─────────────────────────────────────────────
# ROTEAMENTO PRINCIPAL
# ─────────────────────────────────────────────
if st.session_state.logado:
    app_principal()
else:
    tela_login()
