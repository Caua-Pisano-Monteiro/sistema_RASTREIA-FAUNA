import streamlit as st

# ---------------------------------------------------------------
# Estilos
# Paleta: verde-mata (texto), névoa verde (fundo), azul arara (ação)
# ---------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Public+Sans:wght@400;500;600&display=swap');

:root {
  --nevoa: #EAF0EC;
  --mata: #0E2F2A;
  --musgo: #3E6B48;
  --linha: #C5D3CB;
  --arara: #1F4FD8;
}

.stApp { background: var(--nevoa); }
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none; }
.block-container { max-width: 1120px; padding-top: 1.5rem; padding-bottom: 3rem; }

html, body, .stApp, p, li, span, div { font-family: 'Public Sans', system-ui, sans-serif; }
h1, h2, h3, .marca { font-family: 'Bricolage Grotesque', 'Public Sans', sans-serif; color: var(--mata); }

/* Marca */
.marca { font-size: 1.35rem; font-weight: 700; letter-spacing: -0.01em; padding-top: .35rem; }
.marca .ponto { display:inline-block; width:.6rem; height:.6rem; border-radius:50%; background: var(--arara); margin-right:.5rem; }

/* Hero */
.hero-titulo { font-size: clamp(2.3rem, 5vw, 3.7rem); line-height: 1.05; font-weight: 700; letter-spacing: -0.025em; margin: 3rem 0 1.2rem; }
.hero-texto { font-size: 1.12rem; line-height: 1.6; color: #2D4A43; max-width: 34rem; margin-bottom: 1.8rem; }

/* Botões */
.stButton button { border-radius: 999px; padding: .6rem 1.5rem; font-weight: 600; white-space: nowrap; transition: background .15s, border-color .15s; }
[class*="st-key-login"] button { background: transparent; border: 1.5px solid var(--mata); }
[class*="st-key-login"] button, [class*="st-key-login"] button p { color: var(--mata); }
[class*="st-key-login"] button:hover { background: rgba(14,47,42,.08); border-color: var(--mata); }
[class*="st-key-cadastro"] button { background: var(--arara); border: 1.5px solid var(--arara); }
[class*="st-key-cadastro"] button, [class*="st-key-cadastro"] button p { color: #fff; }
[class*="st-key-cadastro"] button:hover { background: #173FB0; border-color: #173FB0; }
.stButton button:focus-visible { outline: 3px solid #8FB0FF; outline-offset: 2px; }
.st-key-login_nav { display: flex; justify-content: flex-end; }

/* Ilustração do rastro */
.rastro { width: 100%; height: auto; }
.rastro .linha { stroke-dasharray: 1; stroke-dashoffset: 1; animation: trilha 2.4s ease-out .3s forwards; }
.rastro .marco { opacity: 0; animation: surgir .4s ease-out forwards; }
@keyframes trilha { to { stroke-dashoffset: 0; } }
@keyframes surgir { to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) {
  .rastro .linha { animation: none; stroke-dashoffset: 0; }
  .rastro .marco { animation: none; opacity: 1; }
}

/* Funcionalidades */
.secao-titulo { font-size: clamp(1.6rem, 3vw, 2.2rem); font-weight: 700; letter-spacing: -0.02em; margin: 4.5rem 0 1.5rem; }
.recursos { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 2rem; }
.recurso { border-left: 3px solid var(--musgo); padding-left: 1.1rem; }
.recurso h3 { font-size: 1.2rem; margin: 0 0 .5rem; }
.recurso p { margin: 0; line-height: 1.6; color: #2D4A43; }

/* Para quem */
.publico { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0 2rem; }
.publico div { border-top: 1px solid var(--linha); padding: 1rem 0; color: var(--mata); font-weight: 500; }

/* Chamada final */
.st-key-chamada { background: var(--mata); border-radius: 20px; padding: 2.8rem 2.5rem; margin-top: 4.5rem; }
.st-key-chamada h2 { color: #fff; font-size: clamp(1.6rem, 3vw, 2.2rem); letter-spacing: -0.02em; margin: 0 0 .6rem; }
.st-key-chamada p { color: #C9DDD3; margin-bottom: 1.4rem; }
.st-key-chamada [class*="st-key-login"] button { border-color: #C9DDD3; }
.st-key-chamada [class*="st-key-login"] button, .st-key-chamada [class*="st-key-login"] button p { color: #fff; }
.st-key-chamada [class*="st-key-login"] button:hover { background: rgba(255,255,255,.1); border-color: #fff; }

.rodape { margin-top: 2.5rem; color: #5B7A70; font-size: .9rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Barra superior
# ---------------------------------------------------------------
topo_marca, topo_acao = st.columns([4, 1])
with topo_marca:
    st.markdown(
        '<div class="marca"><span class="ponto"></span>Rastreia Fauna</div>',
        unsafe_allow_html=True,
    )
with topo_acao:
    if st.button("Entrar", key="login_nav"):
        st.switch_page("login.py")

# ---------------------------------------------------------------
# Hero
# ---------------------------------------------------------------
col_texto, col_arte = st.columns([1.1, 1], gap="large", vertical_alignment="center")

with col_texto:
    st.markdown(
        """
<h1 class="hero-titulo">Saiba onde a fauna está e por onde ela passa.</h1>
<p class="hero-texto">A Rastreia Fauna reúne avistamentos, rotas e espécies da sua área de estudo em um só sistema. A equipe de campo e o escritório trabalham com os mesmos dados.</p>
""",
        unsafe_allow_html=True,
    )
    b1, b2, _ = st.columns([1, 1, 1.4])
    with b1:
        if st.button("Criar conta", key="cadastro_hero"):
            st.switch_page("cadastro.py")
    with b2:
        if st.button("Entrar", key="login_hero"):
            st.switch_page("login.py")

with col_arte:
    st.markdown(
        """
<svg class="rastro" viewBox="0 0 520 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mapa com a trilha de um animal e três avistamentos registrados">
<g fill="none" stroke="#C5D3CB" stroke-width="1.5">
<ellipse cx="270" cy="240" rx="250" ry="190" transform="rotate(-14 270 240)"/>
<ellipse cx="270" cy="240" rx="205" ry="150" transform="rotate(-14 270 240)"/>
<ellipse cx="275" cy="236" rx="160" ry="110" transform="rotate(-14 275 236)"/>
<ellipse cx="280" cy="232" rx="115" ry="72" transform="rotate(-14 280 232)"/>
<ellipse cx="285" cy="228" rx="68" ry="36" transform="rotate(-14 285 228)"/>
</g>
<path class="linha" pathLength="1" d="M40 400 C120 340 90 260 190 250 S330 300 360 200 S430 90 480 60" fill="none" stroke="#1F4FD8" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="40" cy="400" r="6" fill="#0E2F2A"/>
<g class="marco" style="animation-delay:1.0s">
<circle cx="190" cy="250" r="9" fill="#1F4FD8" stroke="#fff" stroke-width="3"/>
<rect x="204" y="258" width="146" height="28" rx="14" fill="#0E2F2A"/>
<text x="277" y="277" text-anchor="middle" font-size="13" font-weight="500" fill="#fff" font-family="Public Sans, sans-serif">Tamanduá-bandeira</text>
</g>
<g class="marco" style="animation-delay:1.7s">
<circle cx="360" cy="200" r="9" fill="#1F4FD8" stroke="#fff" stroke-width="3"/>
<rect x="374" y="208" width="112" height="28" rx="14" fill="#0E2F2A"/>
<text x="430" y="227" text-anchor="middle" font-size="13" font-weight="500" fill="#fff" font-family="Public Sans, sans-serif">Onça-pintada</text>
</g>
<g class="marco" style="animation-delay:2.4s">
<circle cx="480" cy="60" r="9" fill="#1F4FD8" stroke="#fff" stroke-width="3"/>
<rect x="364" y="74" width="98" height="28" rx="14" fill="#0E2F2A"/>
<text x="413" y="93" text-anchor="middle" font-size="13" font-weight="500" fill="#fff" font-family="Public Sans, sans-serif">Arara-azul</text>
</g>
</svg>
""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------
# O que o sistema faz
# ---------------------------------------------------------------
st.markdown(
    """
<h2 class="secao-titulo">Do avistamento ao relatório, sem planilhas soltas</h2>
<div class="recursos">
<div class="recurso"><h3>Registre em campo</h3><p>Anote espécie, local, data e observações na hora do avistamento e anexe fotos ao registro.</p></div>
<div class="recurso"><h3>Veja tudo no mapa</h3><p>Os registros aparecem no mapa da área e podem ser filtrados por espécie, período e equipe.</p></div>
<div class="recurso"><h3>Acompanhe ao longo do tempo</h3><p>Compare períodos, veja quais espécies aparecem mais e exporte relatórios para quem precisa.</p></div>
</div>
<h2 class="secao-titulo">Feito para quem trabalha com fauna</h2>
<div class="publico">
<div>Pesquisadores e equipes de campo</div>
<div>ONGs e unidades de conservação</div>
<div>Consultorias ambientais</div>
<div>Fazendas e reservas particulares</div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Chamada final
# ---------------------------------------------------------------
with st.container(key="chamada"):
    st.markdown(
        "<h2>Comece a registrar a fauna da sua área</h2>"
        "<p>Crie sua conta ou entre para acessar o painel.</p>",
        unsafe_allow_html=True,
    )
    c1, c2, _ = st.columns([1, 1, 2.4])
    with c1:
        if st.button("Criar conta", key="cadastro_cta"):
            st.switch_page("cadastro.py")
    with c2:
        if st.button("Entrar", key="login_cta"):
            st.switch_page("login.py")

st.markdown('<div class="rodape">© 2026 Rastreia Fauna</div>', unsafe_allow_html=True)
