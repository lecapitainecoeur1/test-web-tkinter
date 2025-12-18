import streamlit as st
import math
import random
from datetime import datetime

# --- Initialisation session ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "historique" not in st.session_state:
    st.session_state.historique = []
if "pseudo" not in st.session_state:
    st.session_state.pseudo = ""
if "screen" not in st.session_state:
    st.session_state.screen = "main"
if "current_op" not in st.session_state:
    st.session_state.current_op = None
if "n1" not in st.session_state:
    st.session_state.n1 = 0
if "n2" not in st.session_state:
    st.session_state.n2 = 0

# --- Fonctions ---
def calculer(op_name, n1, n2=None):
    solution = None
    erreur = None
    try:
        if op_name == "Addition":
            solution = n1 + n2
        elif op_name == "Soustraction":
            solution = n1 - n2
        elif op_name == "Multiplication":
            solution = n1 * n2
        elif op_name == "Division":
            if n2 != 0:
                solution = n1 / n2
            else:
                erreur = "Division par zéro impossible"
        elif op_name == "Modulo":
            solution = n1 % n2
        elif op_name == "Puissance²":
            solution = n1 ** 2
        elif op_name == "Puissance³":
            solution = n1 ** 3
        elif op_name == "Racine carrée":
            if n1 >= 0:
                solution = math.sqrt(n1)
            else:
                erreur = "Impossible de calculer racine carrée négative"
    except Exception as e:
        erreur = str(e)

    if erreur:
        st.error(erreur)
        return None
    else:
        st.session_state.score += 1
        maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.historique.append(f"{maintenant} | {st.session_state.pseudo} | {op_name} | {solution}")
        return solution

def get_random(op_name):
    if op_name in ["Addition", "Soustraction", "Multiplication", "Division", "Modulo"]:
        return random.randint(1,100), random.randint(1,100)
    else:
        return random.randint(1,20), None

# --- Écran pseudo ---
if st.session_state.pseudo == "":
    st.title("Operation Web - Entrez votre pseudo")
    st.session_state.pseudo = st.text_input("Pseudo :")
    if st.session_state.pseudo != "":
        st.session_state.screen = "main"
    st.stop()

# --- Écran principal ---
if st.session_state.screen == "main":
    st.title(f"Bonjour {st.session_state.pseudo} ! Score : {st.session_state.score}")
    st.subheader("Choisissez une opération :")
    
    rows = [
        ["Multiplication", "Division", "Addition", "Modulo", "Soustraction"],
        ["Puissance²", "Puissance³", "Racine carrée", "Aléatoire", "À venir"],
        ["À venir", "À venir", "À venir", "Calculette", "Historique"]
    ]
    
    for row in rows:
        cols = st.columns(5)
        for i, op_name in enumerate(row):
            if cols[i].button(op_name):
                if op_name == "Historique":
                    st.session_state.screen = "historique"
                elif op_name == "Calculette":
                    st.info("Fonction calculette à venir")
                elif op_name != "À venir":
                    st.session_state.current_op = op_name
                    st.session_state.n1, st.session_state.n2 = get_random(op_name)
                    st.session_state.screen = "operation"
                st.experimental_rerun()
                
# --- Écran opération ---
elif st.session_state.screen == "operation":
    st.subheader(f"Opération : {st.session_state.current_op}")
    n1 = st.number_input("Nombre 1", value=st.session_state.n1, key="op_n1")
    if st.session_state.n2 is not None:
        n2 = st.number_input("Nombre 2", value=st.session_state.n2, key="op_n2")
    else:
        n2 = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Valider"):
            solution = calculer(st.session_state.current_op, n1, n2)
            st.session_state.solution = solution
            st.session_state.screen = "resultat"
            st.experimental_rerun()
    with col2:
        if st.button("Annuler"):
            st.session_state.screen = "main"
            st.experimental_rerun()

# --- Écran résultat ---
elif st.session_state.screen == "resultat":
    st.subheader(f"Résultat de {st.session_state.current_op}")
    st.success(f"{st.session_state.solution}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Rejouer même opération"):
            st.session_state.screen = "operation"
            st.experimental_rerun()
    with col2:
        if st.button("Retour au menu principal"):
            st.session_state.screen = "main"
            st.experimental_rerun()

# --- Écran historique ---
elif st.session_state.screen == "historique":
    st.subheader("Historique des calculs (dernières 20 entrées)")
    for ligne in st.session_state.historique[-20:]:
        st.write(ligne)
    if st.button("Retour au menu principal"):
        st.session_state.screen = "main"
        st.experimental_rerun()
