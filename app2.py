import streamlit as st
import random

# ---------- Initialisation ----------
if "a" not in st.session_state:
    st.session_state.a = random.randint(1, 20)
if "b" not in st.session_state:
    st.session_state.b = random.randint(1, 20)
if "operation" not in st.session_state:
    st.session_state.operation = "+"
if "score" not in st.session_state:
    st.session_state.score = 0
if "message" not in st.session_state:
    st.session_state.message = ""

# ---------- Fonctions ----------
def nouvelle_question():
    st.session_state.a = random.randint(1, 20)
    st.session_state.b = random.randint(1, 20)
    st.session_state.message = ""

def calcul_correct():
    a = st.session_state.a
    b = st.session_state.b
    op = st.session_state.operation

    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return round(a / b, 2)

# ---------- Interface ----------
st.title("Jeu de calcul 🧠")
st.write(f"Score : **{st.session_state.score}**")

# Choix opération
st.session_state.operation = st.selectbox(
    "Choisis une opération",
    ["+", "-", "*", "/"]
)

# Question
st.subheader("Calcule :")
st.write(f"### {st.session_state.a} {st.session_state.operation} {st.session_state.b}")

# Réponse utilisateur
reponse = st.number_input("Ta réponse :", step=0.01)

# Vérification
if st.button("Valider"):
    bonne_reponse = calcul_correct()
    if abs(reponse - bonne_reponse) < 0.01:
        st.session_state.message = "✅ Bonne réponse !"
        st.session_state.score += 1
    else:
        st.session_state.message = f"❌ Faux ! La bonne réponse était {bonne_reponse}"

    nouvelle_question()
    st.experimental_rerun()

# Message
if st.session_state.message:
    st.info(st.session_state.message)
