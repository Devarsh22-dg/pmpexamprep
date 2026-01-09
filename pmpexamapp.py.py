import random
import streamlit as st

# -----------------------------
# Question bank (combined)
# -----------------------------
DOMAINS = ["Process", "People", "Business Environment"]


def _vars(rng: random.Random):
    names = ["Aisha", "Miguel", "Chen", "Priya", "Omar", "Sofia", "Liam", "Fatima", "Kenji", "Elena", "Ravi", "Noah"]
    industries = ["healthcare", "fintech", "manufacturing", "telecom", "retail", "energy", "public sector", "education"]
    approaches = ["predictive", "agile", "hybrid"]
    phases = ["initiating", "planning", "execution", "monitoring and controlling", "closing", "an iteration", "a sprint review"]
    sizes = ["a small", "a major", "an urgent", "a late-breaking"]
    return {
        "name": rng.choice(names),
        "industry": rng.choice(industries),
        "approach": rng.choice(approaches),
        "phase": rng.choice(phases),
        "size": rng.choice(sizes),
    }


def generate_question_bank(total: int = 200, seed: int = 7):
    """
    Returns a list of dict questions:
      {id, domain, topic, question, options, answer_index, explanation}
    Bank is created by mixing PMP-style scenario templates with varied context.
    """
    rng = random.Random(seed)

    # Distribution similar to PMP ECO weighting
    n_process = int(total * 0.50)
    n_people = int(total * 0.40)
    n_business = total - n_process - n_people  # remainder ~10%

    questions = []
    questions += _generate_process(n_process, rng)
    questions += _generate_people(n_people, rng)
    questions += _generate_business(n_business, rng)

    rng.shuffle(questions)
    return questions


def _generate_process(n: int, rng: random.Random):
    templates = []

    templates.append({
        "topic": "Integration / Change control",
        "q": "{name} is managing a {approach} project in {industry}. A stakeholder requests {size} change during {phase} and asks to bypass the agreed change process. What should the project manager do FIRST?",
        "options": [
            "Approve the change to maintain stakeholder engagement",
            "Assess impacts and follow the agreed change control/governance approach",
            "Escalate to the sponsor immediately",
            "Update the schedule baseline and implement the change",
        ],
        "answer": 1,
        "exp": "PMP expects: assess impact → follow governance/change approach. Escalation is not first unless required by policy or repeated noncompliance."
    })

    templates.append({
        "topic": "Scope / Requirements",
        "q": "Deliverables are being produced, but key stakeholders say they do not meet expectations. What should the project manager do FIRST?",
        "options": [
            "Conduct a quality audit to identify nonconformities",
            "Review and confirm requirements and acceptance criteria with stakeholders",
            "Add additional testers to the team",
            "Escalate to the steering committee",
        ],
        "answer": 1,
        "exp": "If stakeholders reject deliverables, first verify requirements and acceptance criteria (definition of done). Audits/resourcing come after confirming what's expected."
    })

    templates.append({
        "topic": "Quality",
        "q": "The team finds the same defect pattern repeatedly even though inspections occur regularly. What should the project manager do NEXT?",
        "options": [
            "Increase inspection frequency",
            "Perform root cause analysis and implement preventive actions",
            "Ask the customer to accept the defects due to schedule pressure",
            "Replace the quality inspector",
        ],
        "answer": 1,
        "exp": "Repeated defects indicate a systemic cause. PMP favors prevention over inspection: root cause analysis (5 Whys, fishbone) → preventive actions."
    })

    templates.append({
        "topic": "Schedule / Forecasting",
        "q": "A key milestone is at risk because remaining work was underestimated. What should the project manager do FIRST?",
        "options": [
            "Require overtime to recover the schedule",
            "Re-estimate remaining work and update the schedule forecast",
            "Rebaseline the schedule immediately",
            "Remove low performers from the team",
        ],
        "answer": 1,
        "exp": "First get accurate data and update the forecast. Rebaselining is a formal decision after analysis and approvals; overtime is an option after planning."
    })

    templates.append({
        "topic": "Risk vs Issue",
        "q": "A supplier missed two deliveries and work is now blocked. What should the project manager do NEXT?",
        "options": [
            "Log it as a risk and monitor",
            "Record it as an issue and implement the issue response/escalation path",
            "Ignore it until the next status meeting",
            "Only update the lessons learned register",
        ],
        "answer": 1,
        "exp": "A current blocking problem is an issue (not a risk). Capture it in the issue log and execute the agreed issue management/escalation process."
    })

    templates.append({
        "topic": "Communications Planning",
        "q": "Stakeholders complain that updates are inconsistent and they do not know what decisions were made. What should the project manager do FIRST?",
        "options": [
            "Send daily status reports to all stakeholders",
            "Review communication requirements and update the communications management plan",
            "Escalate to the sponsor",
            "Replace the communications tool",
        ],
        "answer": 1,
        "exp": "Plan communications based on stakeholder needs: what info, when, how, by whom. 'More reports' is a trap if requirements are unclear."
    })

    templates.append({
        "topic": "Procurement",
        "q": "A vendor proposes a substitute that meets technical specs but changes contract terms. What should the project manager do NEXT?",
        "options": [
            "Accept the substitute to avoid delays",
            "Review the contract and follow the procurement/change control process",
            "Ask the team to decide and proceed immediately",
            "Pay extra to keep the schedule",
        ],
        "answer": 1,
        "exp": "Contract changes must follow contractual and integrated change control. Review terms, approvals, and impacts before accepting substitutions."
    })

    templates.append({
        "topic": "Agile/Hybrid Value Delivery",
        "q": "In a(n) {approach} project, during {phase} a stakeholder says a delivered feature does not provide expected value. What should the project manager do NEXT?",
        "options": [
            "Submit a formal change request",
            "Facilitate backlog refinement and ask the product owner to reprioritize",
            "Reject the feedback because the iteration is complete",
            "Update the scope baseline",
        ],
        "answer": 1,
        "exp": "Agile/hybrid exams prefer adapting through backlog refinement and reprioritization to maximize value. Formal change requests apply if governance requires it."
    })

    templates.append({
        "topic": "Cost / Variance",
        "q": "Performance reports show cost variance is worsening. What should the project manager do FIRST?",
        "options": [
            "Reduce quality activities to save money",
            "Analyze variance causes and develop corrective actions",
            "Replace the cost engineer",
            "Stop reporting cost performance to avoid escalation",
        ],
        "answer": 1,
        "exp": "First analyze causes of variance and plan corrective actions. Cutting quality is a classic PMP trap; personnel changes are rarely the first response."
    })

    templates.append({
        "topic": "Governance / Compliance",
        "q": "Midway through the project, the organization introduces a new governance/compliance requirement. What should the project manager do FIRST?",
        "options": [
            "Stop the project immediately",
            "Assess impacts and determine required updates to plans and baselines",
            "Ignore until project closing",
            "Ask the team to work around it informally",
        ],
        "answer": 1,
        "exp": "New governance/compliance constraints require impact assessment first, then updates through the agreed governance/change process."
    })

    out = []
    for i in range(n):
        t = rng.choice(templates)
        v = _vars(rng)
        out.append({
            "id": f"P{i+1:03d}",
            "domain": "Process",
            "topic": t["topic"],
            "question": t["q"].format(**v),
            "options": t["options"],
            "answer_index": t["answer"],
            "explanation": t["exp"],
        })
    return out


def _generate_people(n: int, rng: random.Random):
    templates = []

    templates.append({
        "topic": "Conflict Management",
        "q": "Two team members strongly disagree on a technical approach and the conflict is hurting team morale. What should the project manager do FIRST?",
        "options": [
            "Use authority to pick the solution",
            "Facilitate a collaborative discussion to understand interests and reach agreement",
            "Escalate to functional management",
            "Remove one team member from the project",
        ],
        "answer": 1,
        "exp": "PMP prefers collaborate/problem-solve first. Forcing or escalation is used only when collaboration fails or time/safety constraints demand it."
    })

    templates.append({
        "topic": "Servant Leadership",
        "q": "A high-performing, self-organizing team says the project manager’s frequent oversight is slowing them down. What should the project manager do?",
        "options": [
            "Increase monitoring to ensure standards are met",
            "Adopt servant leadership: empower the team and provide support as needed",
            "Replace team members who resist oversight",
            "Escalate the complaint to HR",
        ],
        "answer": 1,
        "exp": "For mature teams, empower and remove impediments. Over-control reduces ownership and performance—an exam-favorite trap."
    })

    templates.append({
        "topic": "Stakeholder Engagement",
        "q": "A key stakeholder actively resists the project because they fear the change will reduce their influence. What should the project manager do FIRST?",
        "options": [
            "Escalate to the sponsor to overrule the stakeholder",
            "Understand concerns and work with the stakeholder on engagement and change readiness",
            "Ignore the stakeholder and proceed as planned",
            "Remove the stakeholder from communications and decisions",
        ],
        "answer": 1,
        "exp": "Resistance is addressed through engagement: understand concerns, communicate value, involve stakeholders. Escalate only after collaboration attempts."
    })

    templates.append({
        "topic": "Team Development",
        "q": "New team members joined and roles/responsibilities are unclear. What should the project manager do NEXT?",
        "options": [
            "Assign tasks ad hoc and adjust later",
            "Develop/revisit the team charter and clarify roles (e.g., RACI, working agreements)",
            "Wait for the team to self-organize over time",
            "Escalate to the sponsor for direction",
        ],
        "answer": 1,
        "exp": "Clarify roles and working agreements early. Team charters and RACI-style clarity are common PMP correct answers."
    })

    templates.append({
        "topic": "Communication & Culture",
        "q": "A distributed team reports misunderstandings due to cultural and language differences. What should the project manager do NEXT?",
        "options": [
            "Use only written communication to avoid confusion",
            "Tailor communications and establish shared norms, using interactive methods for complex topics",
            "Replace remote members with local staff",
            "Stop meetings to reduce conflict",
        ],
        "answer": 1,
        "exp": "Tailor communication, use cultural awareness, and use interactive methods for complex/sensitive topics. Replacing people is rarely first."
    })

    templates.append({
        "topic": "Coaching & Performance",
        "q": "A team member is underperforming because expectations were not clearly communicated. What should the project manager do FIRST?",
        "options": [
            "Document the issue and escalate to HR",
            "Clarify expectations, provide feedback, and coach the team member",
            "Remove the team member from the project immediately",
            "Ignore it to avoid conflict",
        ],
        "answer": 1,
        "exp": "PMP prefers direct coaching and clear expectations first. Escalation/removal is later if performance does not improve."
    })

    out = []
    for i in range(n):
        t = rng.choice(templates)
        out.append({
            "id": f"PE{i+1:03d}",
            "domain": "People",
            "topic": t["topic"],
            "question": t["q"],
            "options": t["options"],
            "answer_index": t["answer"],
            "explanation": t["exp"],
        })
    return out


def _generate_business(n: int, rng: random.Random):
    templates = []

    templates.append({
        "topic": "Compliance / Regulatory",
        "q": "Mid-project, a new regulatory requirement is announced that may affect the product design. What should the project manager do FIRST?",
        "options": [
            "Ignore it until the next phase to avoid delays",
            "Assess the impact and determine required changes to remain compliant",
            "Ask the team to implement changes immediately without analysis",
            "Close the project early",
        ],
        "answer": 1,
        "exp": "Compliance is non-negotiable. First assess impacts, then follow governance/change control to implement required changes."
    })

    templates.append({
        "topic": "Business Value / Benefits",
        "q": "Deliverables are being completed on schedule, but expected business benefits are not being realized. What should the project manager do NEXT?",
        "options": [
            "Continue focusing only on completing deliverables",
            "Review the benefits management plan and engage stakeholders to realign to outcomes",
            "Increase reporting frequency",
            "Reduce scope to finish earlier",
        ],
        "answer": 1,
        "exp": "PMP emphasizes value delivery: verify benefits realization and realign via governance. Outputs ≠ outcomes is a core exam theme."
    })

    templates.append({
        "topic": "Strategy Alignment",
        "q": "A project supports a strategic objective, but market conditions changed and the objective may no longer be valid. What should the project manager do FIRST?",
        "options": [
            "Hide the information to prevent cancellation",
            "Raise the concern through governance and request a business case/strategy review",
            "Push the team to deliver faster to prove value",
            "Reduce quality to meet deadlines",
        ],
        "answer": 1,
        "exp": "When strategy shifts, the PM should surface it through governance so leadership can decide to continue, pivot, pause, or terminate."
    })

    templates.append({
        "topic": "Governance / Policy",
        "q": "The sponsor requests a feature that conflicts with an organizational policy. What should the project manager do?",
        "options": [
            "Implement the feature because the sponsor requested it",
            "Explain the constraint, assess options, and follow governance for a compliant decision",
            "Ask the team to implement it quietly",
            "Remove the policy from project documentation",
        ],
        "answer": 1,
        "exp": "Policy/compliance constraints must be respected. Communicate constraints, assess alternatives, and use governance for approvals."
    })

    out = []
    for i in range(n):
        t = rng.choice(templates)
        out.append({
            "id": f"B{i+1:03d}",
            "domain": "Business Environment",
            "topic": t["topic"],
            "question": t["q"],
            "options": t["options"],
            "answer_index": t["answer"],
            "explanation": t["exp"],
        })
    return out


# -----------------------------
# Streamlit app (combined)
# -----------------------------
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
    if "seed" not in st.session_state:
        st.session_state.seed = 7


def start_quiz(num_questions: int, selected_domains: list[str], seed: int):
    bank = generate_question_bank(total=200, seed=seed)
    filtered = [q for q in bank if q["domain"] in selected_domains]

    if not filtered:
        st.error("No questions available for the selected domain filters.")
        return

    rng = random.Random(seed)
    rng.shuffle(filtered)

    st.session_state.questions = filtered[: min(num_questions, len(filtered))]
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = {}
    st.session_state.quiz_started = True
    st.session_state.seed = seed


def reset_quiz():
    for k in ["quiz_started", "questions", "idx", "score", "answered", "seed"]:
        if k in st.session_state:
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
            start_quiz(num_questions=int(num_questions), selected_domains=selected_domains, seed=int(seed))
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

    st.success("✅ Correct") if is_correct else st.error("❌ Incorrect")

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

    c1, c2 = st.columns([1, 1])
    confirm = c1.button("✅ Confirm", use_container_width=True)
    skip = c2.button("⏭️ Skip", use_container_width=True)

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

    if skip:
        # Mark as skipped (no score impact; reviewed as incorrect)
        st.session_state.answered[qid] = {"selected": selected, "correct": False}
        st.warning("Skipped — saved for review as incorrect (no score added).")

st.divider()
nav1, nav2 = st.columns([1, 1])

if nav1.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
    st.session_state.idx -= 1
    st.rerun()

if nav2.button("➡️ Next", use_container_width=True):
    st.session_state.idx += 1
    st.rerun()
