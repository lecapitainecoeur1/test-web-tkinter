import streamlit as st
import random

# Configuration de la page
st.set_page_config(
    page_title="Entraîneur Mathématiques",
    page_icon="🧮",
    layout="centered"
)

# Initialisation des variables de session
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'nombre1' not in st.session_state:
    st.session_state.nombre1 = 0
if 'nombre2' not in st.session_state:
    st.session_state.nombre2 = 0
if 'operation' not in st.session_state:
    st.session_state.operation = "addition"
if 'solution' not in st.session_state:
    st.session_state.solution = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

def generer_nombres(operation):
    """Génère deux nombres selon l'opération choisie"""
    if operation == "addition":
        n1 = random.randint(1, 100)
        n2 = random.randint(1, 100)
        solution = n1 + n2
        symbole = "+"
    elif operation == "soustraction":
        n1 = random.randint(10, 100)
        n2 = random.randint(1, n1)  # n2 <= n1 pour éviter les négatifs
        solution = n1 - n2
        symbole = "-"
    elif operation == "multiplication":
        n1 = random.randint(1, 12)
        n2 = random.randint(1, 12)
        solution = n1 * n2
        symbole = "×"
    elif operation == "division":
        n2 = random.randint(2, 12)
        n1 = n2 * random.randint(1, 12)  # Assurer une division exacte
        solution = n1 // n2
        symbole = "÷"
    
    return n1, n2, solution, symbole

def nouvelle_question():
    """Génère une nouvelle question"""
    n1, n2, sol, _ = generer_nombres(st.session_state.operation)
    st.session_state.nombre1 = n1
    st.session_state.nombre2 = n2
    st.session_state.solution = sol
    st.session_state.feedback

# Titre et style
st.title("🧮 Entraîneur Mathématiques")
st.markdown("---")

# Sidebar pour les statistiques
with st.sidebar:
    st.header("📊 Statistiques")
    st.metric("Score", f"{st.session_state.score}/{st.session_state.total}")
    if st.session_state.total > 0:
        pourcentage = (st.session_state.score / st.session_state.total) * 100
        st.metric("Réussite", f"{pourcentage:.1f}%")
    
    st.markdown("---")
    if st.button("🔄 Réinitialiser le score", use_container_width=True):
        st.session_state.score = 0
        st.session_state.total = 0

# Sélection de l'opération
col1, col2 = st.columns([2, 1])
with col1:
    operation = st.selectbox(
        "Choisissez une opération:",
        ["addition", "soustraction", "multiplication", "division"],
        key="operation_select"
    )

with col2:
    if st.button("🎲 Nouvelle question", use_container_width=True):
        st.session_state.operation = operation
        nouvelle_question()

# Initialiser la première question si nécessaire
if st.session_state.nombre1 == 0 and st.session_state.nombre2 == 0:
    st.session_state.operation = operation
    nouvelle_question()

# Afficher le feedback si disponible
if st.session_state.feedback:
    if st.session_state.feedback == "correct":
        st.success("✅ Bravo ! C'est correct !")
        time.sleep(2.5)
    else:
        st.error(f"❌ Incorrect ! La bonne réponse était {st.session_state.solution}")
        time.sleep(2.5)

# Obtenir le symbole de l'opération
_, _, _, symbole = generer_nombres(st.session_state.operation)

# Afficher la question
st.markdown(f"### Question:")
st.markdown(f"# {st.session_state.nombre1} {symbole} {st.session_state.nombre2} = ?")

# Formulaire de réponse
with st.form("reponse_form", clear_on_submit=True):
    reponse = st.number_input("Votre réponse:", value=0, step=1)
    submit = st.form_submit_button("✅ Valider", type="primary", use_container_width=True)
    
    if submit:
        st.session_state.total += 1
        
        if int(reponse) == st.session_state.solution:
            st.session_state.score += 1
            st.session_state.feedback = "correct"
        else:
            st.session_state.feedback = "incorrect"
        
        # Générer automatiquement une nouvelle question
        nouvelle_question()
        st.rerun()

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    1. Choisissez une opération (addition, soustraction, multiplication, division)
    2. Résolvez le calcul affiché
    3. Entrez votre réponse et validez
    4. Le programme vous dit si c'est correct et génère automatiquement une nouvelle question
    5. Votre score est affiché dans la barre latérale
    """)
