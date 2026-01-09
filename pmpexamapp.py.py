import streamlit as st
from questions import generate_question_bank, DOMAINS

st.set_page_config(page_title="PMP Exam Simulator", page_icon="🧠", layout="centered")

st.title("🧠 PMP Exam Simulator (200-question bank)")
st.caption("PMP-style scenario questions across Process, People, and Business Environment. Confirm answers to see explanations.")


def init_session():
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = {}  # qid -> {"selected": int, "correct": bool}
    if "confirmed" not in st.session_state:
        st.session_state.confirmed = False
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "seed" not in st.session_state:
        st.session_state.seed = 7


def start_quiz(num_questions: int, selected_domains: list[str], seed: int):
    bank = generate_question_bank(total=200, seed=seed)
    filtered = [q for q in bank if q["domain"] in selected_domains]

    if not filtered:
        st.error("No questions available for the selected domain filters.")
        return

    # Deterministic shuffle for a stable session per seed
    import random
    rng = random.Random(seed)
    rng.shuffle(filtered)

    st.session_state.questions = filtered[: min(num_questions, len(filtered))]
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = {}
    st.session_state.confirmed = False
    st.session_state.selected_option = None
    st.session_state.quiz_started = True
    st.session_state.seed = seed


def reset_quiz():
    for k in list(st.session_state.keys()):
        if k in {
            "quiz_started",
            "questions",
            "idx",
            "score",
            "answered",
            "confirmed",
            "selected_option",
            "seed",
        }:
            del st.session_state[k]
    init_session()


init_session()

with st.sidebar:
    st.header("⚙️ Quiz Settings")

    seed = st.number_input(
        "Random seed (same seed = same quiz order)",
        min_value=1,
        max_value=10_000_000,
        value=int(st.session_state.seed),
        step=1,
    )

    selected_domains = st.multiselect(
        "Domains to include",
        options=DOMAINS,
        default=DOMAINS,
    )

    num_questions = st.slider(
        "Number of questions",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ Start / Restart", use_container_width=True):
            start_quiz(num_questions=num_questions, selected_domains=selected_domains, seed=int(seed))
    with col_b:
        if st.button("♻️ Reset", use_container_width=True):
            reset_quiz()

if not st.session_state.quiz_started:
    st.info("Set your quiz options in the sidebar, then click **Start / Restart**.")
    st.stop()

questions = st.session_state.questions
idx = st.session_state.idx

if idx >= len(questions):
    st.success("🎉 Quiz complete!")
    total = len(questions)
    score = st.session_state.score
    st.metric("Final Score", f"{score} / {total}")

    # Review incorrect
    wrong = []
    for q in questions:
        qid = q["id"]
        if qid in st.session_state.answered and not st.session_state.answered[qid]["correct"]:
            wrong.append(q)

    if wrong:
        st.subheader("🔎 Review Incorrect Answers")
        for q in wrong:
            qid = q["id"]
            a = st.session_state.answered[qid]["selected"]
            correct = q["answer_index"]
            with st.expander(f"{qid} — {q['domain']} — {q['topic']}"):
                st.write(q["question"])
                st.write("**Your answer:**", f"{chr(65+a)}. {q['options'][a]}")
                st.write("**Correct answer:**", f"{chr(65+correct)}. {q['options'][correct]}")
                st.write("**Explanation:**", q["explanation"])
    else:
        st.success("✅ No incorrect answers. Nice.")

    st.stop()

q = questions[idx]
qid = q["id"]

st.progress((idx + 1) / len(questions))
top_cols = st.columns([2, 1, 1])
with top_cols[0]:
    st.subheader(f"Question {idx + 1} of {len(questions)}")
with top_cols[1]:
    st.caption("Domain")
    st.write(f"**{q['domain']}**")
with top_cols[2]:
    st.caption("Score")
    st.write(f"**{st.session_state.score}**")

st.caption(f"Topic: {q['topic']}")
st.write(q["question"])

# If already answered, lock view
already_answered = qid in st.session_state.answered
if already_answered:
    selected = st.session_state.answered[qid]["selected"]
    correct = q["answer_index"]
    is_correct = st.session_state.answered[qid]["correct"]

    st.radio(
        "Select one answer:",
        options=list(range(len(q["options"]))),
        format_func=lambda i: f"{chr(65+i)}. {q['options'][i]}",
        index=selected,
        disabled=True,
        key=f"radio_{qid}",
    )

    if is_correct:
        st.success("✅ Correct")
    else:
        st.error("❌ Incorrect")

    st.write("**Explanation:**")
    st.write(q["explanation"])
    st.write("**Correct answer:**", f"{chr(65+correct)}. {q['options'][correct]}")

else:
    selected = st.radio(
        "Select one answer:",
        options=list(range(len(q["options"]))),
        format_func=lambda i: f"{chr(65+i)}. {q['options'][i]}",
        index=0,
        key=f"radio_{qid}",
    )
    st.session_state.selected_option = selected

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        confirm = st.button("✅ Confirm", use_container_width=True)
    with c2:
        skip = st.button("⏭️ Skip", use_container_width=True)

    if confirm:
        correct_index = q["answer_index"]
        is_correct = (selected == correct_index)
        st.session_state.answered[qid] = {"selected": selected, "correct": is_correct}

        if is_correct:
            st.session_state.score += 1
            st.success("✅ Correct")
        else:
            st.error("❌ Incorrect")

        st.write("**Explanation:**")
        st.write(q["explanation"])
        st.write("**Correct answer:**", f"{chr(65+correct_index)}. {q['options'][correct_index]}")

        st.session_state.confirmed = True

    if skip:
        # Mark as skipped (no score impact)
        st.session_state.answered[qid] = {"selected": selected, "correct": False}
        st.warning("Skipped — counted as incorrect for review purposes (no score penalty unless you want that behavior).")
        st.session_state.confirmed = True

# Navigation
st.divider()
nav1, nav2, nav3 = st.columns([1, 1, 2])

with nav1:
    if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
        st.session_state.idx -= 1
        st.session_state.confirmed = False
        st.rerun()

with nav2:
    if st.button("➡️ Next", use_container_width=True):
        st.session_state.idx += 1
        st.session_state.confirmed = False
        st.rerun()

with nav3:
    st.caption("Tip: PMP questions often test FIRST/NEXT/BEST action logic: assess → collaborate → follow governance → act.")
