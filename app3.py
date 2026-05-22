import streamlit as st
import random
from datetime import datetime
from enum import Enum
import math
import os

# ─── Config ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Opération",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Page background */
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

h1, h2, h3 {
    font-family: 'Fredoka One', cursive;
    color: #e94560;
    letter-spacing: 1px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 24px 28px;
    margin: 12px 0;
    backdrop-filter: blur(8px);
}

/* Score badge */
.score-badge {
    display: inline-block;
    background: linear-gradient(90deg, #e94560, #f5a623);
    color: white;
    font-family: 'Fredoka One', cursive;
    font-size: 1.4rem;
    border-radius: 50px;
    padding: 6px 22px;
    margin-bottom: 8px;
    box-shadow: 0 4px 15px rgba(233,69,96,0.4);
}

/* Operation display */
.op-display {
    font-family: 'Fredoka One', cursive;
    font-size: 2.8rem;
    color: #f5f5f5;
    text-align: center;
    padding: 24px;
    background: rgba(233,69,96,0.12);
    border: 2px solid rgba(233,69,96,0.3);
    border-radius: 16px;
    margin: 16px 0;
    letter-spacing: 2px;
}

/* Result correct */
.result-correct {
    background: rgba(39,174,96,0.15);
    border: 2px solid #27ae60;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    color: #2ecc71;
    font-size: 1.4rem;
    font-weight: 700;
}

/* Result wrong */
.result-wrong {
    background: rgba(231,76,60,0.15);
    border: 2px solid #e74c3c;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    color: #e74c3c;
    font-size: 1.4rem;
    font-weight: 700;
}

/* Buttons - override streamlit */
.stButton > button {
    font-family: 'Fredoka One', cursive !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
    border: none !important;
    background: rgba(255,255,255,0.1) !important;
    color: #f0f0f0 !important;
    transition: all 0.2s ease !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
.stButton > button:hover {
    background: rgba(233,69,96,0.4) !important;
    border-color: #e94560 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(233,69,96,0.3) !important;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #e94560, #c0392b) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(233,69,96,0.35) !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.9) !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: black !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.5rem !important;
    text-align: center !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e94560 !important;
    box-shadow: 0 0 0 2px rgba(233,69,96,0.3) !important;
}

/* Number input */
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.5rem !important;
    text-align: center !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,20,40,0.95) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Fredoka One', cursive;
    color: rgba(255,255,255,0.6);
}
.stTabs [aria-selected="true"] {
    background: rgba(233,69,96,0.3) !important;
    color: white !important;
}

/* Text area */
.stTextArea textarea {
    background: rgba(255,255,255,0.06) !important;
    color: #ccc !important;
    border-radius: 10px !important;
    font-family: monospace !important;
    font-size: 0.85rem !important;
}

p, label, .stMarkdown {
    color: rgba(255,255,255,0.85);
}
</style>
""", unsafe_allow_html=True)


# ─── Enums ────────────────────────────────────────────────────────────────────
class Op(Enum):
    addition = "addition"
    soustraction = "soustraction"
    multiplication = "multiplication"
    division = "division"
    puissance2 = "puissance²"
    racinecarree = "racine carrée"
    puissance3 = "puissance³"
    modulo = "modulo"


# ─── Fichiers ─────────────────────────────────────────────────────────────────
PSEUDO_FILE = "pseudo.txt"
SCORES_FILE = "scores.txt"

def charger_pseudo():
    try:
        with open(PSEUDO_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def sauvegarder_pseudo(pseudo):
    with open(PSEUDO_FILE, "w") as f:
        f.write(pseudo)

def enregistrer_score(pseudo, user_reponse, solution, score, chaine):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    correct = "✅ Correcte" if user_reponse == solution else "❌ Incorrecte"
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{now} | {pseudo} | {correct} | Score: {score} | {chaine} = {user_reponse}\n")

def charger_historique():
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# ─── Session state init ───────────────────────────────────────────────────────
defaults = {
    "pseudo": charger_pseudo(),
    "score": 0,
    "page": "login",          # login | menu | quiz | calculette | historique | credits
    "quiz_op": None,
    "quiz_nb1": None,
    "quiz_nb2": None,
    "quiz_question": "",
    "quiz_solution": None,
    "quiz_answered": False,
    "quiz_user_rep": None,
    "quiz_round": 0,
    "calc_result": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Helpers ──────────────────────────────────────────────────────────────────
def go(page):
    st.session_state.page = page

def generer_question(op: Op):
    """Génère un couple (nb1, nb2, question, solution) pour une opération donnée."""
    if op == Op.puissance2:
        n = random.randint(1, 11)
        return n, 0, f"{n}²  = ?", n*n
    elif op == Op.puissance3:
        n = random.randint(1, 5)
        return n, 0, f"{n}³  = ?", n**3
    elif op == Op.racinecarree:
        n = random.randint(1, 11)
        return n, 0, f"√{n*n}  = ?", n
    elif op == Op.addition:
        a, b = random.randint(1, 100), random.randint(1, 100)
        return a, b, f"{a} + {b} = ?", a + b
    elif op == Op.soustraction:
        a, b = random.randint(1, 100), random.randint(1, 100)
        if a < b:
            a, b = b, a
        return a, b, f"{a} − {b} = ?", a - b
    elif op == Op.multiplication:
        a, b = random.randint(1, 11), random.randint(1, 11)
        return a, b, f"{a} × {b} = ?", a * b
    elif op == Op.division:
        b = random.randint(2, 10)
        a = b * random.randint(2, 10)
        return a, b, f"{a} ÷ {b} = ?", a // b
    elif op == Op.modulo:
        a = random.randint(10, 100)
        b = random.randint(1, 10)
        return a, b, f"{a} mod {b} = ?", a % b

    # Si aucun cas ne correspond, on lève une erreur claire
    raise ValueError(f"Opération inconnue : {op}")

def start_quiz(op: Op):
    try:
        n1, n2, q, sol = generer_question(op)
    except Exception as e:
        st.error(f"Erreur lors de la génération de la question : {e}")
        return

    # Forcer un nouveau round AVANT tout
    new_round = st.session_state.quiz_round + 1

    # Nettoyer l'ancienne clé d'input pour forcer Streamlit à recréer le widget
    old_key = f"quiz_input_{st.session_state.quiz_round}"
    if old_key in st.session_state:
        del st.session_state[old_key]

    st.session_state.quiz_op       = op
    st.session_state.quiz_nb1      = n1
    st.session_state.quiz_nb2      = n2
    st.session_state.quiz_question = q
    st.session_state.quiz_solution = sol
    st.session_state.quiz_answered = False
    st.session_state.quiz_user_rep = None
    st.session_state.quiz_round    = new_round
    go("quiz")

# ─── PAGE: LOGIN ──────────────────────────────────────────────────────────────
def page_login():
    st.markdown("<h1 style='text-align:center;font-size:3.5rem;'>🧮 Opération</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.5);margin-top:-10px;margin-bottom:30px;'>Entraîne-toi aux opérations mathématiques</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 👤 Quel est ton pseudo ?")
        pseudo_input = st.text_input("", value=st.session_state.pseudo, placeholder="Entre ton pseudo…", label_visibility="collapsed")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Valider", use_container_width=True, type="primary"):
                if pseudo_input.strip():
                    st.session_state.pseudo = pseudo_input.strip()
                    sauvegarder_pseudo(pseudo_input.strip())
                    go("menu")
                    st.rerun()
                else:
                    st.error("Veuillez entrer un pseudo valide.")
        with col2:
            if st.button("➡️ Continuer sans pseudo", use_container_width=True):
                st.session_state.pseudo = "Anonyme"
                go("menu")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ─── PAGE: MENU ───────────────────────────────────────────────────────────────
def page_menu():
    col_title, col_score = st.columns([3, 1])
    with col_title:
        st.markdown(f"<h1>🧮 Opération</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:rgba(255,255,255,0.5);margin-top:-14px;'>Bonjour, <b style='color:#e94560'>{st.session_state.pseudo}</b> !</p>", unsafe_allow_html=True)
    with col_score:
        st.markdown(f"<div style='padding-top:20px;text-align:right;'><span class='score-badge'>⭐ {st.session_state.score}</span></div>", unsafe_allow_html=True)

    st.markdown("### ➕ Choisissez une opération")

    ops = [
        ("➕ Addition",       Op.addition),
        ("➖ Soustraction",   Op.soustraction),
        ("✖️ Multiplication", Op.multiplication),
        ("➗ Division",       Op.division),
        ("🎲 Aléatoire",      None),
        ("√ Racine carrée",  Op.racinecarree),
        ("x² Puissance²",    Op.puissance2),
        ("x³ Puissance³",    Op.puissance3),
        ("% Modulo",         Op.modulo),
    ]

    cols = st.columns(3)
    for i, (label, op_val) in enumerate(ops):
        with cols[i % 3]:
            if st.button(label, use_container_width=True, key=f"op_{i}"):
                chosen = op_val if op_val else Op(random.choice(list(Op)).value)
                start_quiz(chosen)
                st.rerun()

    st.markdown("---")
    st.markdown("### 🛠️ Outils")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔢 Calculette", use_container_width=True):
            go("calculette")
            st.rerun()
    with c2:
        if st.button("📜 Historique", use_container_width=True):
            go("historique")
            st.rerun()
    with c3:
        if st.button("ℹ️ Crédits", use_container_width=True):
            go("credits")
            st.rerun()
    with c4:
        if st.button("🚪 Déconnexion", use_container_width=True):
            go("login")
            st.rerun()

    # GitHub / support links
    st.markdown("""
    <div style='text-align:center;margin-top:10px;color:rgba(255,255,255,0.35);font-size:0.85rem;'>
        <a href='https://github.com/HGVKSHDBQSJBKSQJBF/operation' target='_blank' style='color:#e94560;'>GitHub</a>
        &nbsp;·&nbsp;
        <a href='https://mail.google.com/mail/?view=cm&fs=1&to=lecapitainecoeurytbpro@gmail.com&su=id%C3%A9e%20pour%20votre%20projet%20operation' target='_blank' style='color:#e94560;'>Support</a>
    </div>
    """, unsafe_allow_html=True)


# ─── PAGE: QUIZ ───────────────────────────────────────────────────────────────
def page_quiz():
    op = st.session_state.quiz_op
    question = st.session_state.quiz_question
    solution = st.session_state.quiz_solution
    answered = st.session_state.quiz_answered

    # Header
    col_back, col_score = st.columns([1, 1])
    with col_back:
        if st.button("← Retour au menu"):
            go("menu")
            st.rerun()
    with col_score:
        st.markdown(f"<div style='text-align:right;padding-top:4px;'><span class='score-badge'>⭐ {st.session_state.score}</span></div>", unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align:center;'>{op.value.capitalize()}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='op-display'>{question}</div>", unsafe_allow_html=True)

    if not answered:
        rnd = st.session_state.quiz_round

        def soumettre():
            try:
                user_rep = int(st.session_state[f"quiz_input_{rnd}"])
            except ValueError:
                st.error("Veuillez entrer un nombre valide !")
                return

            if st.session_state.quiz_answered:
                return
            st.session_state.quiz_user_rep = user_rep
            st.session_state.quiz_answered = True
            if user_rep == solution:
                st.session_state.score += 1
            else:
                st.session_state.score -= 1

            enregistrer_score(
                st.session_state.pseudo,
                user_rep,
                solution,
                st.session_state.score,
                question.replace(" = ?", "")
            )

        st.number_input(
            "Ta réponse :",
            step=1,
            value=0,
            key=f"quiz_input_{rnd}",
            on_change=soumettre,
        )

        if st.button("✅ Valider", use_container_width=True, type="primary"):
            soumettre()
            st.rerun()

    else:
        user_rep = st.session_state.quiz_user_rep
        if user_rep == solution:
            st.markdown(f"<div class='result-correct'>🎉 Bonne réponse ! + 1 point</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-wrong'>❌ Faux ! La réponse était <b>{solution}</b>. − 1 point</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='text-align:center;margin:8px 0;color:rgba(255,255,255,0.5);'>Score actuel : <b style='color:#e94560;'>{st.session_state.score}</b></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Rejouer", use_container_width=True, type="primary", key=f"rejouer_{st.session_state.quiz_round}"):
                st.write(st.session_state.quiz_op)
                op_actuel = Op(st.session_state.quiz_op.value)
                n1, n2, q, sol = generer_question(op_actuel)
                old_key = f"quiz_input_{st.session_state.quiz_round}"
                if old_key in st.session_state:
                    del st.session_state[old_key]
                st.session_state.quiz_round    += 1
                st.session_state.quiz_op        = op_actuel
                st.session_state.quiz_nb1       = n1
                st.session_state.quiz_nb2       = n2
                st.session_state.quiz_question  = q
                st.session_state.quiz_solution  = sol
                st.session_state.quiz_answered  = False
                st.session_state.quiz_user_rep  = None
                st.rerun()
        with col2:
            if st.button("🏠 Menu", use_container_width=True, key=f"menu_{st.session_state.quiz_round}"):
                go("menu")
                st.rerun()


# ─── PAGE: CALCULETTE ─────────────────────────────────────────────────────────
def page_calculette():
    if st.button("← Retour"):
        go("menu")
        st.rerun()

    st.markdown("<h2>🔢 Calculette</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        op_label = st.selectbox("Opération", [
            "Addition (+)", "Soustraction (−)", "Multiplication (×)", "Division (÷)",
            "Modulo (%)", "Puissance²", "Puissance³", "Racine carrée (√)"
        ])

        needs_two = op_label not in ("Puissance²", "Puissance³", "Racine carrée (√)")

        col1, col2 = st.columns(2) if needs_two else (st.columns(1)[0], None)
        with col1:
            a = st.number_input("Nombre A", step=1, value=0, key="calc_a")
        if needs_two and col2:
            with col2:
                b = st.number_input("Nombre B", step=1, value=1, key="calc_b")

        if st.button("= Calculer", type="primary", use_container_width=True):
            a = int(a)
            result = None
            try:
                if op_label.startswith("Addition"):
                    result = a + int(b)
                elif op_label.startswith("Soustraction"):
                    result = a - int(b)
                elif op_label.startswith("Multiplication"):
                    result = a * int(b)
                elif op_label.startswith("Division"):
                    if int(b) == 0:
                        st.error("Division par zéro !")
                    else:
                        result = a // int(b)
                elif op_label.startswith("Modulo"):
                    result = a % int(b)
                elif op_label.startswith("Puissance²"):
                    result = a ** 2
                elif op_label.startswith("Puissance³"):
                    result = a ** 3
                elif op_label.startswith("Racine"):
                    if a < 0:
                        st.error("Racine d'un nombre négatif !")
                    else:
                        result = math.isqrt(a)
            except Exception as e:
                st.error(f"Erreur : {e}")

            if result is not None:
                st.session_state.calc_result = result

        if st.session_state.calc_result is not None:
            st.markdown(f"<div class='op-display'>= {st.session_state.calc_result}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ─── PAGE: HISTORIQUE ─────────────────────────────────────────────────────────
def page_historique():
    if st.button("← Retour"):
        go("menu")
        st.rerun()

    st.markdown("<h2>📜 Historique des scores</h2>", unsafe_allow_html=True)
    contenu = charger_historique()
    if contenu.strip():
        lignes = contenu.strip().split("\n")
        lignes.reverse()  # Plus récent en premier
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.text_area("", value="\n".join(lignes), height=400, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Pas encore d'historique. Lance-toi dans une opération !")


# ─── PAGE: CREDITS ────────────────────────────────────────────────────────────
def page_credits():
    if st.button("← Retour"):
        go("menu")
        st.rerun()

    st.markdown("<h2>ℹ️ Crédits</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card' style='text-align:center;'>
        <p style='font-size:1.4rem;color:#e94560;font-weight:700;'>☺ lecapitainecoeur ☺</p>
        <p>Programmeur · Créateur · Imaginateur</p>
        <br>
        <p style='color:rgba(255,255,255,0.4);font-size:0.9rem;'>Projet open-source — suggestions bienvenues !</p>
        <br>
        <a href='https://github.com/HGVKSHDBQSJBKSQJBF/operation' target='_blank'
           style='color:#e94560;font-weight:700;text-decoration:none;'>🐙 GitHub</a>
        &nbsp;&nbsp;
        <a href='https://mail.google.com/mail/?view=cm&fs=1&to=lecapitainecoeurytbpro@gmail.com&su=id%C3%A9e%20pour%20votre%20projet%20operation'
           target='_blank' style='color:#e94560;font-weight:700;text-decoration:none;'>✉️ Contact</a>
    </div>
    """, unsafe_allow_html=True)


# ─── ROUTER ───────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "login":
    page_login()
elif page == "menu":
    page_menu()
elif page == "quiz":
    page_quiz()
elif page == "calculette":
    page_calculette()
elif page == "historique":
    page_historique()
elif page == "credits":
    page_credits()
