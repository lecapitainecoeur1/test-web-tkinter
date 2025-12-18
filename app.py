import streamlit as st
import math
import random
from datetime import datetime

# --- Initialisation ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "historique" not in st.session_state:
    st.session_state.historique = []

# --- Titre ---
st.title("Operation en ligne")

# --- Pseudo ---
pseudo = st.text_input("Entrez votre pseudo :", value=st.session_state.get("pseudo", ""))
st.session_state.pseudo = pseudo

st.write(f"Bonjour, {pseudo} ! Votre score actuel est {st.session_state.score}.")

# --- Fonction pour calculer ---
def calculer(op_name, nombre_1=None, nombre_2=None):
    solution = None
    erreur = None

    try:
        if op_name == "Addition":
            solution = nombre_1 + nombre_2
        elif op_name == "Soustraction":
            solution = nombre_1 - nombre_2
        elif op_name == "Multiplication":
            solution = nombre_1 * nombre_2
        elif op_name == "Division":
            if nombre_2 != 0:
                solution = nombre_1 / nombre_2
            else:
                erreur = "Division par zéro impossible"
        elif op_name == "Modulo":
            solution = nombre_1 % nombre_2
        elif op_name == "Puissance²":
            solution = nombre_1 ** 2
        elif op_name == "Puissance³":
            solution = nombre_1 ** 3
        elif op_name == "Racine carrée":
            if nombre_1 >= 0:
                solution = math.sqrt(nombre_1)
            else:
                erreur = "Impossible de calculer la racine carrée d'un nombre négatif"
    except Exception as e:
        erreur = str(e)

    if erreur:
        st.error(erreur)
    else:
        st.success(f"Le résultat de {op_name} est : {solution}")
        st.session_state.score += 1
        maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.historique.append(
            f"{maintenant} | {pseudo} | {op_name} | {solution}"
        )

# --- Fonction pour générer nombres aléatoires ---
def get_random_values(op_name):
    if op_name in ["Addition", "Soustraction", "Multiplication", "Division", "Modulo"]:
        return random.randint(1,100), random.randint(1,100)
    else:
        return random.randint(1,20), None

# --- Interface avec boutons identiques à Tkinter ---
st.subheader("Choisissez une opération:")

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
                st.subheader("Historique des calculs (dernières 20 entrées)")
                for ligne in st.session_state.historique[-20:]:
                    st.write(ligne)
            elif op_name == "Calculette":
                st.info("Fonction calculette à venir")
            elif op_name != "À venir":
                n1, n2 = get_random_values(op_name)
                if n2 is not None:
                    n1 = cols[i].number_input("Nombre 1", value=n1, key=f"{op_name}_1")
                    n2 = cols[i].number_input("Nombre 2", value=n2, key=f"{op_name}_2")
                else:
                    n1 = cols[i].number_input("Nombre", value=n1, key=f"{op_name}_1")
                calculer(op_name, n1, n2)

# --- Boutons supplémentaires ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Réinitialiser le score"):
        st.session_state.score = 0
        st.success("Score réinitialisé !")

with col2:
    if st.button("Réinitialiser l'historique"):
        st.session_state.historique = []
        st.success("Historique effacé !")
