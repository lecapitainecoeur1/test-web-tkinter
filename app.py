import streamlit as st
import random
from datetime import datetime
from enum import Enum
import os

class Operation(Enum):
    ADDITION = "addition"
    SOUSTRACTION = "soustraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    PUISSANCE2 = "puissance2"
    RACINE_CARRE = "racine_carree"
    PUISSANCE3 = "puissance3"
    MODULO = "modulo"

# Configuration de la page
st.set_page_config(
    page_title="Opérations Mathématiques",
    page_icon="🧮",
    layout="wide"
)

# Initialisation des variables de session
if 'pseudo' not in st.session_state:
    st.session_state.pseudo = ""
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_operation' not in st.session_state:
    st.session_state.current_operation = None
if 'nombre_1' not in st.session_state:
    st.session_state.nombre_1 = 0
if 'nombre_2' not in st.session_state:
    st.session_state.nombre_2 = 0
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'solution' not in st.session_state:
    st.session_state.solution = 0
if 'mode' not in st.session_state:
    st.session_state.mode = "menu"
if 'calc_result' not in st.session_state:
    st.session_state.calc_result = None
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'user_response' not in st.session_state:
    st.session_state.user_response = 0

# Fonctions utilitaires
def charger_pseudo():
    try:
        with open("pseudo.txt", "r", encoding="utf-8") as fichier:
            return fichier.read().strip()
    except FileNotFoundError:
        return ""

def sauvegarder_pseudo(pseudo):
    with open("pseudo.txt", "w", encoding="utf-8") as fichier:
        fichier.write(pseudo)

def enregistrer_score(user_reponse, solution, score, question, pseudo):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("scores.txt", "a", encoding="utf-8") as fichier:
            if user_reponse == solution:
                fichier.write(f"{now} | {pseudo} | Réponse correcte | Score: {score} | operation: {question} = {user_reponse}\n")
            else:
                fichier.write(f"{now} | {pseudo} | Réponse incorrecte | Score: {score} | operation: {question} = {user_reponse} (attendu: {solution})\n")
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement: {e}")
        return False

def afficher_historique():
    try:
        with open("scores.txt", "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
        if contenu == "":
            return "Il n'y a pas d'historique pour le moment"
        return contenu
    except FileNotFoundError:
        return "Il n'y a pas d'historique pour le moment"

def generer_operation(operation):
    nombre_1 = 0
    nombre_2 = 0
    question = ""
    
    if operation == Operation.PUISSANCE2:
        nombre_1 = random.randint(1, 11)
        question = f"{nombre_1}²"
        solution = nombre_1 * nombre_1
    elif operation == Operation.MODULO:
        nombre_1 = random.randint(10, 100)
        nombre_2 = random.randint(1, 10)
        question = f"{nombre_1} modulo {nombre_2}"
        solution = nombre_1 % nombre_2
    elif operation == Operation.RACINE_CARRE:
        nombre_1 = random.randint(1, 11)
        question = f"√{nombre_1 * nombre_1}"
        solution = nombre_1
    elif operation == Operation.ADDITION:
        nombre_1 = random.randint(1, 100)
        nombre_2 = random.randint(1, 100)
        question = f"{nombre_1} + {nombre_2}"
        solution = nombre_1 + nombre_2
    elif operation == Operation.SOUSTRACTION:
        nombre_1 = random.randint(1, 100)
        nombre_2 = random.randint(1, 100)
        if nombre_1 < nombre_2:
            nombre_1, nombre_2 = nombre_2, nombre_1
        question = f"{nombre_1} - {nombre_2}"
        solution = nombre_1 - nombre_2
    elif operation == Operation.DIVISION:
        nombre_2 = random.randint(2, 10)
        nombre_1 = random.randint(2, 10)
        nombre_2 = nombre_2 * nombre_1
        question = f"{nombre_2} ÷ {nombre_1}"
        solution = nombre_2 // nombre_1
    elif operation == Operation.MULTIPLICATION:
        nombre_1 = random.randint(1, 11)
        nombre_2 = random.randint(1, 11)
        question = f"{nombre_1} × {nombre_2}"
        solution = nombre_1 * nombre_2
    elif operation == Operation.PUISSANCE3:
        nombre_1 = random.randint(1, 5)
        question = f"{nombre_1}³"
        solution = nombre_1 * nombre_1 * nombre_1
    
    return nombre_1, nombre_2, question, solution

def calculer(operation, val1, val2=None):
    if operation == "multiplication":
        return val1 * val2
    elif operation == "division":
        return val1 // val2 if val2 != 0 else "Erreur: division par zéro"
    elif operation == "addition":
        return val1 + val2
    elif operation == "soustraction":
        return val1 - val2
    elif operation == "puissance2":
        return val1 * val1
    elif operation == "puissance3":
        return val1 * val1 * val1
    elif operation == "racine_carree":
        return int(val1 ** 0.5)
    elif operation == "modulo":
        return val1 % val2 if val2 != 0 else "Erreur: division par zéro"

# CSS personnalisé
st.markdown("""
    <style>
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .score-font {
        font-size: 30px !important;
        font-weight: bold;
        color: #2ca02c;
    }
    </style>
    """, unsafe_allow_html=True)

# Page de connexion
if st.session_state.pseudo == "":
    st.title("🎮 Bienvenue dans Opérations Mathématiques")
    st.write("### Entrez votre pseudo pour commencer")
    
    pseudo_input = st.text_input("Pseudo:", value=charger_pseudo(), key="pseudo_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Valider", type="primary", use_container_width=True):
            if pseudo_input.strip() != "":
                st.session_state.pseudo = pseudo_input
                sauvegarder_pseudo(pseudo_input)
                st.rerun()
            else:
                st.error("Veuillez entrer un pseudo valide.")
    with col2:
        if st.button("❌ Quitter", use_container_width=True):
            st.stop()

# Application principale
else:
    # Sidebar
    with st.sidebar:
        st.title(f"👤 {st.session_state.pseudo}")
        st.markdown(f'<p class="score-font">Score: {st.session_state.score}</p>', unsafe_allow_html=True)
        st.divider()
        
        if st.button("🏠 Menu Principal", use_container_width=True):
            st.session_state.mode = "menu"
            st.session_state.last_result = None
            st.rerun()
        
        if st.button("🧮 Calculette", use_container_width=True):
            st.session_state.mode = "calculette"
            st.rerun()
        
        if st.button("📊 Historique", use_container_width=True):
            st.session_state.mode = "historique"
            st.rerun()
        
        if st.button("ℹ️ Crédits", use_container_width=True):
            st.session_state.mode = "credits"
            st.rerun()
        
        st.divider()
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.pseudo = ""
            st.session_state.score = 0
            st.rerun()
    
    # Mode Menu
    if st.session_state.mode == "menu":
        st.title("🎯 Choisissez une opération")
        
        col1, col2, col3, col4 = st.columns(4)
        
        operations = [
            ("✖️ Multiplication", Operation.MULTIPLICATION),
            ("➗ Division", Operation.DIVISION),
            ("➖ Soustraction", Operation.SOUSTRACTION),
            ("➕ Addition", Operation.ADDITION),
            ("🎲 Aléatoire", "aleatoire"),
            ("√ Racine Carrée", Operation.RACINE_CARRE),
            ("² Puissance 2", Operation.PUISSANCE2),
            ("³ Puissance 3", Operation.PUISSANCE3),
            ("% Modulo", Operation.MODULO),
        ]
        
        cols = [col1, col2, col3, col4]
        for idx, (label, op) in enumerate(operations):
            with cols[idx % 4]:
                if st.button(label, key=f"op_{idx}", use_container_width=True):
                    if op == "aleatoire":
                        op = random.choice([o for _, o in operations if o != "aleatoire"])
                    st.session_state.current_operation = op
                    n1, n2, q, sol = generer_operation(op)
                    st.session_state.nombre_1 = n1
                    st.session_state.nombre_2 = n2
                    st.session_state.question = q
                    st.session_state.solution = sol
                    st.session_state.mode = "exercice"
                    st.session_state.last_result = None
                    st.rerun()
    
    # Mode Exercice
    elif st.session_state.mode == "exercice":
        st.title("📝 Résolvez l'opération")
        
        # Afficher le dernier résultat s'il existe
        if st.session_state.last_result:
            if st.session_state.last_result == "correct":
                st.success(f"✅ Correct ! La réponse était bien {st.session_state.solution}")
            else:
                st.error(f"❌ Incorrect ! La réponse était {st.session_state.solution}")
        
        st.markdown(f'<p class="big-font">{st.session_state.question} = ?</p>', unsafe_allow_html=True)
        
        # Formulaire pour capturer la réponse
        with st.form(key="answer_form", clear_on_submit=True):
            reponse = st.number_input("Votre réponse:", value=0, step=1, key="user_input")
            submit = st.form_submit_button("✅ Valider", type="primary", use_container_width=True)
            
            if submit:
                st.session_state.user_response = int(reponse)
                if reponse == st.session_state.solution:
                    st.session_state.score += 1
                    st.session_state.last_result = "correct"
                else:
                    st.session_state.score -= 1
                    st.session_state.last_result = "incorrect"
                
                # Enregistrer dans le fichier
                enregistrer_score(
                    int(reponse), 
                    st.session_state.solution, 
                    st.session_state.score, 
                    st.session_state.question,
                    st.session_state.pseudo
                )
                st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Nouvelle question", use_container_width=True, key="new_q"):
                n1, n2, q, sol = generer_operation(st.session_state.current_operation)
                st.session_state.nombre_1 = n1
                st.session_state.nombre_2 = n2
                st.session_state.question = q
                st.session_state.solution = sol
                st.session_state.last_result = None
                st.rerun()
        
        with col2:
            if st.button("🏠 Retour au menu", use_container_width=True, key="back_menu"):
                st.session_state.mode = "menu"
                st.session_state.last_result = None
                st.rerun()
    
    # Mode Calculette
    elif st.session_state.mode == "calculette":
        st.title("🧮 Calculette")
        
        operation_calc = st.selectbox(
            "Choisissez une opération:",
            ["multiplication", "division", "addition", "soustraction", 
             "puissance2", "puissance3", "racine_carree", "modulo"]
        )
        
        val1 = st.number_input("Premier nombre:", value=0.0, key="calc_val1")
        
        if operation_calc in ["multiplication", "division", "addition", "soustraction", "modulo"]:
            val2 = st.number_input("Deuxième nombre:", value=0.0, key="calc_val2")
        else:
            val2 = None
        
        if st.button("🔢 Calculer", type="primary"):
            result = calculer(operation_calc, val1, val2)
            st.success(f"Résultat: {result}")
    
    # Mode Historique
    elif st.session_state.mode == "historique":
        st.title("📊 Historique des Scores")
        historique = afficher_historique()
        st.text_area("", historique, height=400, key="hist_area")
        
        if st.button("🗑️ Effacer l'historique", type="secondary"):
            try:
                with open("scores.txt", "w", encoding="utf-8") as fichier:
                    fichier.write("")
                st.success("Historique effacé !")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur: {e}")
    
    # Mode Crédits
    elif st.session_state.mode == "credits":
        st.title("ℹ️ Crédits")
        st.markdown("""
        ### 👨‍💻 Programmeur: ☺lecapitainecoeur☺
        ### 🎨 Créateur: ☺lecapitainecoeur☺
        ### 💡 Imaginateur: ☺lecapitainecoeur☺
        
        ---
        
        📧 Support: lecapitainecoeurytbpro@gmail.com
        
        🔗 GitHub: [github.com/HGVKSHDBQSJBKSQJBF/operation](https://github.com/HGVKSHDBQSJBKSQJBF/operation)
        """)
