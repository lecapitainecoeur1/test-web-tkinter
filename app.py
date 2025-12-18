import streamlit as st
import random
from datetime import datetime
from enum import Enum
import math

class Operation(Enum):
    ADDITION = "Addition"
    SOUSTRACTION = "Soustraction"
    MULTIPLICATION = "Multiplication"
    DIVISION = "Division"
    PUISSANCE2 = "Puissance²"
    PUISSANCE3 = "Puissance³"
    RACINE_CARREE = "Racine Carrée"
    MODULO = "Modulo"
    ALEATOIRE = "Aléatoire"

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
if 'question_actuelle' not in st.session_state:
    st.session_state.question_actuelle = None
if 'mode' not in st.session_state:
    st.session_state.mode = "menu"
if 'operation_selectionnee' not in st.session_state:
    st.session_state.operation_selectionnee = None
if 'calc_mode' not in st.session_state:
    st.session_state.calc_mode = None

# Fonctions pour l'historique
def enregistrer_score(user_reponse, solution, score, operation_text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultat = "Réponse correcte" if user_reponse == solution else "Réponse incorrecte"
    
    try:
        with open("scores.txt", "a", encoding="utf-8") as fichier:
            fichier.write(f"{now} | {st.session_state.pseudo} | {resultat} | Score: {score} | Opération: {operation_text} = {user_reponse}\n")
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement: {e}")

def afficher_historique():
    try:
        with open("scores.txt", "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
            if contenu == "":
                return "Il n'y a pas d'historique pour le moment"
            return contenu
    except FileNotFoundError:
        return "Il n'y a pas d'historique pour le moment"

# Fonction pour générer une question
def generer_question(operation):
    if operation == Operation.ALEATOIRE:
        operation = random.choice([
            Operation.ADDITION, Operation.SOUSTRACTION, 
            Operation.MULTIPLICATION, Operation.DIVISION,
            Operation.PUISSANCE2, Operation.PUISSANCE3, 
            Operation.RACINE_CARREE
        ])
    
    if operation == Operation.ADDITION:
        n1, n2 = random.randint(1, 100), random.randint(1, 100)
        question = f"{n1} + {n2}"
        solution = n1 + n2
    elif operation == Operation.SOUSTRACTION:
        n1, n2 = random.randint(1, 100), random.randint(1, 100)
        if n1 < n2:
            n1, n2 = n2, n1
        question = f"{n1} - {n2}"
        solution = n1 - n2
    elif operation == Operation.MULTIPLICATION:
        n1, n2 = random.randint(1, 11), random.randint(1, 11)
        question = f"{n1} × {n2}"
        solution = n1 * n2
    elif operation == Operation.DIVISION:
        n2 = random.randint(2, 10)
        n1 = random.randint(2, 10)
        n2 = n2 * n1
        question = f"{n2} ÷ {n1}"
        solution = n2 // n1
    elif operation == Operation.PUISSANCE2:
        n1 = random.randint(1, 11)
        question = f"{n1}²"
        solution = n1 * n1
    elif operation == Operation.PUISSANCE3:
        n1 = random.randint(1, 5)
        question = f"{n1}³"
        solution = n1 * n1 * n1
    elif operation == Operation.RACINE_CARREE:
        n1 = random.randint(1, 11)
        question = f"√{n1 * n1}"
        solution = n1
    elif operation == Operation.MODULO:
        n1 = random.randint(10, 100)
        n2 = random.randint(1, 10)
        question = f"{n1} mod {n2}"
        solution = n1 % n2
    
    return {
        'question': question,
        'solution': solution,
        'operation': operation.value
    }

# CSS personnalisé
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
    }
    .big-score {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Page de connexion
if not st.session_state.pseudo:
    st.title("🧮 Opérations Mathématiques")
    st.header("Connexion")
    
    pseudo_input = st.text_input("Entrez votre pseudo :", key="pseudo_input")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Valider", type="primary", use_container_width=True):
            if pseudo_input.strip():
                st.session_state.pseudo = pseudo_input.strip()
                st.rerun()
            else:
                st.error("Veuillez entrer un pseudo valide")

# Menu principal
elif st.session_state.mode == "menu":
    st.title(f"🧮 Bienvenue {st.session_state.pseudo} !")
    
    # Affichage du score
    st.markdown(f"<div class='big-score'>Score: {st.session_state.score}</div>", unsafe_allow_html=True)
    
    st.header("Choisissez une opération :")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Addition", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.ADDITION
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.ADDITION)
            st.rerun()
        
        if st.button("🔢 Puissance²", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.PUISSANCE2
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.PUISSANCE2)
            st.rerun()
    
    with col2:
        if st.button("➖ Soustraction", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.SOUSTRACTION
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.SOUSTRACTION)
            st.rerun()
        
        if st.button("🔢 Puissance³", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.PUISSANCE3
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.PUISSANCE3)
            st.rerun()
    
    with col3:
        if st.button("✖️ Multiplication", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.MULTIPLICATION
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.MULTIPLICATION)
            st.rerun()
        
        if st.button("√ Racine Carrée", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.RACINE_CARREE
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.RACINE_CARREE)
            st.rerun()
    
    with col4:
        if st.button("➗ Division", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.DIVISION
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.DIVISION)
            st.rerun()
        
        if st.button("% Modulo", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.MODULO
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.MODULO)
            st.rerun()
    
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎲 Aléatoire", use_container_width=True):
            st.session_state.operation_selectionnee = Operation.ALEATOIRE
            st.session_state.mode = "jeu"
            st.session_state.question_actuelle = generer_question(Operation.ALEATOIRE)
            st.rerun()
    
    with col2:
        if st.button("🧮 Calculette", use_container_width=True):
            st.session_state.mode = "calculette"
            st.rerun()
    
    with col3:
        if st.button("📊 Historique", use_container_width=True):
            st.session_state.mode = "historique"
            st.rerun()
    
    with col4:
        if st.button("❌ Déconnexion", use_container_width=True):
            st.session_state.pseudo = ""
            st.session_state.score = 0
            st.rerun()

# Mode jeu
elif st.session_state.mode == "jeu":
    st.title(f"🧮 {st.session_state.question_actuelle['operation']}")
    st.markdown(f"<div class='big-score'>Score: {st.session_state.score}</div>", unsafe_allow_html=True)
    
    st.header(f"Question : {st.session_state.question_actuelle['question']} = ?")
    
    reponse = st.number_input("Votre réponse :", step=1, format="%d", key="reponse_input")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Valider", type="primary", use_container_width=True):
            if reponse == st.session_state.question_actuelle['solution']:
                st.session_state.score += 1
                st.success(f"✅ Correct ! La réponse était {st.session_state.question_actuelle['solution']}")
            else:
                st.session_state.score -= 1
                st.error(f"❌ Faux ! La bonne réponse était {st.session_state.question_actuelle['solution']}")
            
            enregistrer_score(
                reponse, 
                st.session_state.question_actuelle['solution'],
                st.session_state.score,
                st.session_state.question_actuelle['question']
            )
            
            # Générer nouvelle question
            st.session_state.question_actuelle = generer_question(st.session_state.operation_selectionnee)
    
    with col2:
        if st.button("🔄 Nouvelle Question", use_container_width=True):
            st.session_state.question_actuelle = generer_question(st.session_state.operation_selectionnee)
            st.rerun()
    
    with col3:
        if st.button("🏠 Retour Menu", use_container_width=True):
            st.session_state.mode = "menu"
            st.rerun()

# Mode calculette
elif st.session_state.mode == "calculette":
    st.title("🧮 Calculette")
    
    if st.session_state.calc_mode is None:
        st.header("Choisissez une opération :")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Addition", use_container_width=True):
                st.session_state.calc_mode = "addition"
                st.rerun()
            if st.button("✖️ Multiplication", use_container_width=True):
                st.session_state.calc_mode = "multiplication"
                st.rerun()
            if st.button("🔢 Puissance²", use_container_width=True):
                st.session_state.calc_mode = "puissance2"
                st.rerun()
        
        with col2:
            if st.button("➖ Soustraction", use_container_width=True):
                st.session_state.calc_mode = "soustraction"
                st.rerun()
            if st.button("➗ Division", use_container_width=True):
                st.session_state.calc_mode = "division"
                st.rerun()
            if st.button("🔢 Puissance³", use_container_width=True):
                st.session_state.calc_mode = "puissance3"
                st.rerun()
        
        with col3:
            if st.button("% Modulo", use_container_width=True):
                st.session_state.calc_mode = "modulo"
                st.rerun()
            if st.button("√ Racine Carrée", use_container_width=True):
                st.session_state.calc_mode = "racine"
                st.rerun()
        
        st.write("")
        if st.button("🏠 Retour Menu", use_container_width=True):
            st.session_state.mode = "menu"
            st.rerun()
    
    else:
        operation_names = {
            "addition": "Addition",
            "soustraction": "Soustraction",
            "multiplication": "Multiplication",
            "division": "Division",
            "modulo": "Modulo",
            "puissance2": "Puissance²",
            "puissance3": "Puissance³",
            "racine": "Racine Carrée"
        }
        
        st.header(f"Calcul : {operation_names[st.session_state.calc_mode]}")
        
        n1 = st.number_input("Premier nombre :", value=0, step=1)
        
        if st.session_state.calc_mode in ["addition", "soustraction", "multiplication", "division", "modulo"]:
            n2 = st.number_input("Deuxième nombre :", value=0, step=1)
        
        if st.button("Calculer", type="primary"):
            try:
                if st.session_state.calc_mode == "addition":
                    resultat = n1 + n2
                elif st.session_state.calc_mode == "soustraction":
                    resultat = n1 - n2
                elif st.session_state.calc_mode == "multiplication":
                    resultat = n1 * n2
                elif st.session_state.calc_mode == "division":
                    resultat = n1 // n2
                elif st.session_state.calc_mode == "modulo":
                    resultat = n1 % n2
                elif st.session_state.calc_mode == "puissance2":
                    resultat = n1 ** 2
                elif st.session_state.calc_mode == "puissance3":
                    resultat = n1 ** 3
                elif st.session_state.calc_mode == "racine":
                    resultat = int(math.sqrt(n1))
                
                st.success(f"Résultat : {resultat}")
            except Exception as e:
                st.error(f"Erreur de calcul : {e}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Nouvelle Opération", use_container_width=True):
                st.session_state.calc_mode = None
                st.rerun()
        with col2:
            if st.button("🏠 Retour Menu", use_container_width=True):
                st.session_state.calc_mode = None
                st.session_state.mode = "menu"
                st.rerun()

# Mode historique
elif st.session_state.mode == "historique":
    st.title("📊 Historique des Scores")
    
    historique = afficher_historique()
    st.text_area("Historique :", historique, height=400)
    
    if st.button("🏠 Retour Menu", use_container_width=True):
        st.session_state.mode = "menu"
        st.rerun())
