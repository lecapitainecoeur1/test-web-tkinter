# ─── FONCTION: GENERER QUESTION ──────────────────────────────────────────────
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

# ─── FONCTION: START QUIZ ─────────────────────────────────────────────────────
def start_quiz(op: Op):
    """Initialise une nouvelle question de quiz pour l'opération donnée."""
    try:
        n1, n2, q, sol = generer_question(op)
    except Exception as e:
        st.error(f"Erreur lors de la génération de la question : {e}")
        return

    st.session_state.quiz_op = op
    st.session_state.quiz_nb1 = n1
    st.session_state.quiz_nb2 = n2
    st.session_state.quiz_question = q
    st.session_state.quiz_solution = sol
    st.session_state.quiz_answered = False
    st.session_state.quiz_user_rep = None
    st.session_state.quiz_round = st.session_state.get("quiz_round", 0) + 1
    go("quiz")

# ─── PAGE: QUIZ ──────────────────────────────────────────────────────────────
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
            if st.button("🔄 Rejouer", use_container_width=True, type="primary"):
                start_quiz(op)
                st.rerun()
        with col2:
            if st.button("🏠 Menu", use_container_width=True):
                go("menu")
                st.rerun()
