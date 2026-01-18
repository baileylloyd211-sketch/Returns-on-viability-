import random
from statistics import pstdev
import streamlit as st
import random
from statistics import pstdev
import streamlit as st

# =========================================================
# 3-Lens Diagnostic (25Q + 10 Follow-ups) — SINGLE FILE
# - Lens selection happens FIRST (setup screen)
# - Session state initialized BEFORE any stage checks
# - Unique widget keys everywhere to avoid DuplicateWidgetID
# ========================================================= 

st.set_page_config(page_title="Trifactor (25Q + 10)", layout="centered")

# --------------------------
# UI Header
# --------------------------
st.title("Trifactor (25 questions)")
st.caption("Three lenses. One pressure point.")

# --------------------------
# Constants / Scale
# --------------------------
LENSES = ["Interpersonal", "Financial", "Big Picture"]

SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

VARIABLE_WEIGHTS = {
    "Baseline": 1.2,
    "Clarity": 1.1,
    "Resources": 1.1,
    "Boundaries": 1.1,
    "Execution": 1.2,
    "Feedback": 1.0,
}

def clamp(n, lo, hi):
    return max(lo, min(hi, n))

def zone_name(score_0_100: float) -> str:
    if score_0_100 < 45:
        return "RED"
    if score_0_100 < 70:
        return "YELLOW"
    return "GREEN"
import random
from statistics import pstdev
import streamlit as st

st.set_page_config(page_title="Trifactor Diagnostic", layout="centered")

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

LENSES = ["Interpersonal", "Financial", "Big Picture"]

SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

VARIABLE_WEIGHTS = {
    "Baseline": 1.2,
    "Clarity": 1.1,
    "Resources": 1.1,
    "Boundaries": 1.1,
    "Execution": 1.2,
    "Feedback": 1.0,
}

# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────

def clamp(n, lo, hi):
    return max(lo, min(hi, n))


def zone_name(score: float) -> str:  # 0–100
    if score < 45:
        return "RED"
    if score < 70:
        return "YELLOW"
    return "GREEN"


def zone_message(zone: str) -> str:
    return {
        "RED": "broken — needs urgent attention",
        "YELLOW": "unstable — fragile under pressure",
        "GREEN": "solid — working well",
    }[zone]


def lens_focus(lens: str) -> str:
    return {
        "Interpersonal": "relationship tension, clarity, boundaries, execution",
        "Financial": "money stability, buffer, boundaries, execution",
        "Big Picture": "mission clarity, resources, focus, execution, feedback",
    }[lens]


def variable_translation(lens: str, var: str) -> str:
    translations = {
        "Interpersonal": {
            "Baseline": "Emotional stability under contact",
            "Clarity": "Knowing what you want / what's true",
            "Resources": "Support & emotional capacity",
            "Boundaries": "Ability to hold limits",
            "Execution": "Following through on difficult conversations",
            "Feedback": "Repair & learning from conflict",
        },
        "Financial": {
            "Baseline": "Stability under financial stress",
            "Clarity": "Knowing your numbers & priorities",
            "Resources": "Income, buffer, tools",
            "Boundaries": "Control over spending & exposure",
            "Execution": "Actually doing the necessary actions",
            "Feedback": "Reviewing & closing leaks",
        },
        "Big Picture": {
            "Baseline": "Overall momentum & stability",
            "Clarity": "Clear direction & next step",
            "Resources": "Energy, support, environment",
            "Boundaries": "Protecting focus & saying no",
            "Execution": "Shipping & completing work",
            "Feedback": "Measuring & iterating",
        },
    }
    return translations.get(lens, {}).get(var, var)


def pressure_focus_summary(lens: str, weakest_var: str) -> str:
    summaries = {
        "Interpersonal": f"Biggest pressure is in **{weakest_var}** — likely too much emotional load or poor resolution patterns.",
        "Financial": f"Biggest pressure is in **{weakest_var}** — usually buffer, system, or leak problem.",
        "Big Picture": f"Biggest pressure is in **{weakest_var}** — goal is real, but structure/support isn't matching.",
    }
    return summaries.get(lens, f"Pressure concentrates in **{weakest_var}**.")


# ──────────────────────────────────────────────────────────────
# Question Bank (placeholder — fill with your real questions)
# ──────────────────────────────────────────────────────────────

QUESTION_BANK = {
    "Interpersonal": [],  # ← your ~75+ questions here
    "Financial": [],      # ← your ~75+ questions here
    "Big Picture": [],    # ← your ~75+ questions here
}

# Note: Make sure every question has unique "id" across ALL lenses
# Recommended structure:
# {"id": "i01", "text": "...", "variable": "Baseline", "weight": 1.2, "reverse": True}

# ──────────────────────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────────────────────

defaults = {
    "stage": "setup",
    "lens": "Interpersonal",
    "active_questions": [],
    "answers": {},
    "idx": 0,
    "followup_questions": [],
    "followup_answers": {},
    "followup_idx": 0,
    "followup_targets": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_session():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()


# ──────────────────────────────────────────────────────────────
# UI – Header & Sidebar
# ──────────────────────────────────────────────────────────────

st.title("Trifactor")
st.caption("Pressure mapping across three lenses")

with st.sidebar:
    st.header("Controls")
    st.caption("25 initial questions + targeted follow-ups")
    if st.button("Reset Everything", type="secondary"):
        reset_session()

# ──────────────────────────────────────────────────────────────
# Setup Screen – Lens Selection
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "setup":
    st.subheader("Choose your diagnostic lens")

    st.session_state.lens = st.radio(
        "Which area feels most pressurized right now?",
        options=LENSES,
        index=LENSES.index(st.session_state.lens),
        horizontal=True,
    )

    st.markdown(
        f"**Focus of this lens:** {lens_focus(st.session_state.lens)}  \n"
        "The tool will show you **where** the system is weakest — not how to fix it yet."
    )

    if st.button("Start 25 Questions", type="primary"):
        lens = st.session_state.lens
        bank = QUESTION_BANK.get(lens, [])

        if not bank:
            st.error("Question bank for this lens is empty. Add questions first.")
            st.stop()

        # Random sample of 25 (or all if fewer)
        k = min(25, len(bank))
        st.session_state.active_questions = random.sample(bank, k=k)
        st.session_state.answers = {}
        st.session_state.idx = 0
        st.session_state.stage = "questions"
        st.rerun()

# ──────────────────────────────────────────────────────────────
# Questions Stage (25 questions) — starts here
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "questions":
    # ── Your existing question loop code would go here ──
    pass
def compassionate_zone_line(zone: str) -> str:
    return {
        "RED": "needs support now (signal, not failure)",
        "YELLOW": "workable, but inconsistent under stress",
        "GREEN": "stable and helping you",
    }.get(zone, zone)

def lens_readout_intro(lens: str) -> str:
    if lens == "Interpersonal":
        return "Interpreting through **relationship dynamics**: tension, clarity, boundaries, follow-through."
    if lens == "Financial":
        return "Interpreting through **money stability + control**: clarity, buffer, boundaries, execution."
    return "Interpreting through **mission control**: clarity, focus, resources, execution, feedback loops."

def lens_translation(lens: str, variable: str) -> str:
    mapping = {
        "Interpersonal": {
            "Baseline": "Emotional baseline under contact",
            "Clarity": "What you want / what’s true",
            "Resources": "Support + emotional bandwidth",
            "Boundaries": "Limits + self-respect in action",
            "Execution": "Having the talk / doing the thing",
            "Feedback": "Repair, learning, reality-checking",
        },
----------------------
QUESTION_BANK = {
    "Interpersonal": [
        {"id":"i01","text":"How often do you feel tense before interacting with a specific person?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"i02","text":"How often does one conversation ruin your whole day?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"i03","text":"How often do you avoid a conversation you know you need to have?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"i04","text":"How clear are you about what you want from this relationship/situation?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"i05","text":"How often do you leave a talk unsure what was actually decided?","variable":"Clarity","weight":1.1,"reverse":True},
        {"id":"i06","text":"How often do you say “yes” when you mean “no”?","variable":"Boundaries","weight":1.4,"reverse":True},
        {"id":"i07","text":"How often do you tolerate behavior that you resent later?","variable":"Boundaries","weight":1.3,"reverse":True},
        {"id":"i08","text":"How often do you communicate your limits early rather than late?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"i09","text":"How supported do you feel by at least one person in your life?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"i10","text":"How often do you feel alone carrying the emotional load?","variable":"Resources","weight":1.2,"reverse":True},
        {"id":"i11","text":"How often do conflicts repeat without resolution?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"i12","text":"How often do you reflect after conflict and adjust your approach?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"i13","text":"How often do you interpret neutral behavior as hostile?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"i14","text":"How often do you apologize to restore peace even when you weren’t wrong?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"i15","text":"How often do you directly ask for what you need?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i16","text":"How often do you replay conversations in your head afterward?","variable":"Baseline","weight":1.0,"reverse":True},
        {"id":"i17","text":"How often do you feel respected in the dynamic?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i18","text":"How often do you keep your word when you set a boundary?","variable":"Execution","weight":1.3,"reverse":False},
        {"id":"i19","text":"How often do you use sarcasm/withdrawal instead of stating the issue?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"i20","text":"How often do you feel you must perform to be valued?","variable":"Clarity","weight":1.0,"reverse":True},
        {"id":"i21","text":"How often do you choose timing/location to improve the odds of a good talk?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"i22","text":"How often do you communicate expectations before frustration builds?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"i23","text":"How often do you recover quickly after conflict?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i24","text":"How often do you ask clarifying questions instead of assuming intent?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i25","text":"How often do you feel you’re walking on eggshells?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"i51","text":"How often do you notice resentment building before you name it?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"i52","text":"How often do you recover quickly after interpersonal strain?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i53","text":"How often do you feel conversations require translation instead of clarity?","variable":"Clarity","weight":1.2,"reverse":True},
        {"id":"i54","text":"How often do you address tone instead of content when tension arises?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"i55","text":"How often do you feel relational effort is uneven?","variable":"Resources","weight":1.2,"reverse":True},
        {"id":"i56","text":"How often do you say no without justification?","variable":"Boundaries","weight":1.3,"reverse":False},
        {"id":"i57","text":"How often do misunderstandings persist longer than necessary?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"i58","text":"How often do you revisit unresolved conversations?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"i59","text":"How often do you feel relationally resourced rather than depleted?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"i60","text":"How often do you check assumptions before reacting?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i61","text":"How often do you feel pressure to maintain harmony at your expense?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"i62","text":"How often do you name patterns instead of incidents?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"i63","text":"How often do you feel conversations reset rather than compound?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i64","text":"How often do you feel safe disagreeing?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i65","text":"How often do you delay resolution due to emotional fatigue?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"i66","text":"How often do you follow through on relational agreements?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i67","text":"How often do you feel conversations end cleanly?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"i68","text":"How often do you absorb blame to keep peace?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"i69","text":"How often do you experience mutual accountability?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"i70","text":"How often do you exit interactions with increased trust?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"i71","text":"How often do you recognize emotional debt accumulating?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"i72","text":"How often do you state needs without apology?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"i73","text":"How often do you feel relational stability across time?","variable":"Baseline","weight":1.2,"reverse":False},
        {"id":"i74","text":"How often do you resolve issues before they resurface?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i75","text":"How often do relationships feel directionally improving?","variable":"Resources","weight":1.3,"reverse":False},
    ],
    "Financial": [
        {"id":"f01","text":"How often do you know your exact cash position (today) without guessing?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"f02","text":"How often do bills/fees surprise you?","variable":"Clarity","weight":1.2,"reverse":True},
        {"id":"f03","text":"How often do you feel like you’re one emergency away from collapse?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"f04","text":"How often do you have a buffer (even small) after essentials?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f05","text":"How often do you spend to regulate mood/stress?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"f06","text":"How consistently do you track spending (even roughly)?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"f07","text":"How often do you miss due dates?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"f08","text":"How often do you avoid opening financial mail/notifications?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"f09","text":"How often do you negotiate rates, call providers, or challenge charges?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"f10","text":"How clear are you on your top 3 financial priorities this month?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f11","text":"How often do impulse purchases break your plan?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"f12","text":"How often do you review recurring subscriptions/auto-pay items?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"f13","text":"How often do you make a simple plan before spending (need vs want)?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f14","text":"How often does financial stress disrupt sleep/focus?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f15","text":"How often do you feel your income is stable/predictable?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"f16","text":"How often do you know your minimum survival number per month?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"f17","text":"How often do you take one concrete financial action per week?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f18","text":"How often do you use a system (notes/app/spreadsheet) to reduce chaos?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f19","text":"How often do you borrow/advance money to get through the month?","variable":"Resources","weight":1.1,"reverse":True},
        {"id":"f20","text":"How often do you postpone decisions until they become emergencies?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"f21","text":"How often do you set boundaries with others about money (loans, favors, guilt)?","variable":"Boundaries","weight":1.0,"reverse":False},
        {"id":"f22","text":"How often do you feel ashamed about money (and hide it)?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"f23","text":"How often do you have a realistic plan for the next 30 days?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f24","text":"How often do you follow that plan when stress hits?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f25","text":"How often do you recover quickly after a financial hit?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i26","text":"How often do you feel braced or guarded before contact?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"i27","text":"How often do you feel responsible for managing the other person’s emotions?","variable":"Boundaries","weight":1.3,"reverse":True},
        {"id":"i28","text":"How often do conversations drift instead of landing decisions?","variable":"Clarity","weight":1.1,"reverse":True},
        {"id":"i29","text":"How often do you initiate repair after t
# =========================================================
# 3-Lens Diagnostic (25Q + 10 Follow-ups) — SINGLE FILE
# - Lens selection happens FIRST (setup screen)
# - Session state initialized BEFORE any stage checks
# - Unique widget keys everywhere to avoid DuplicateWidgetID
# ========================================================= 

st.set_page_config(page_title="Trifactor (25Q + 10)", layout="centered")

# --------------------------
# UI Header
# --------------------------
st.title("Trifactor (25 questions)")
st.caption("Three lenses. One pressure point.")

# --------------------------
# Constants / Scale
# --------------------------
LENSES = ["Interpersonal", "Financial", "Big Picture"]

SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

VARIABLE_WEIGHTS = {
    "Baseline": 1.2,
    "Clarity": 1.1,
    "Resources": 1.1,
    "Boundaries": 1.1,
    "Execution": 1.2,
    "Feedback": 1.0,
}

def clamp(n, lo, hi):
    return max(lo, min(hi, n))

def zone_name(score_0_100: float) -> str:
    if score_0_100 < 45:
        return "RED"
    if score_0_100 < 70:
        return "YELLOW"
    return "GREEN"
import random
from statistics import pstdev
import streamlit as st

st.set_page_config(page_title="Trifactor Diagnostic", layout="centered")

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

LENSES = ["Interpersonal", "Financial", "Big Picture"]

SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

VARIABLE_WEIGHTS = {
    "Baseline": 1.2,
    "Clarity": 1.1,
    "Resources": 1.1,
    "Boundaries": 1.1,
    "Execution": 1.2,
    "Feedback": 1.0,
}

# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────

def clamp(n, lo, hi):
    return max(lo, min(hi, n))


def zone_name(score: float) -> str:  # 0–100
    if score < 45:
        return "RED"
    if score < 70:
        return "YELLOW"
    return "GREEN"


def zone_message(zone: str) -> str:
    return {
        "RED": "broken — needs urgent attention",
        "YELLOW": "unstable — fragile under pressure",
        "GREEN": "solid — working well",
    }[zone]


def lens_focus(lens: str) -> str:
    return {
        "Interpersonal": "relationship tension, clarity, boundaries, execution",
        "Financial": "money stability, buffer, boundaries, execution",
        "Big Picture": "mission clarity, resources, focus, execution, feedback",
    }[lens]


def variable_translation(lens: str, var: str) -> str:
    translations = {
        "Interpersonal": {
            "Baseline": "Emotional stability under contact",
            "Clarity": "Knowing what you want / what's true",
            "Resources": "Support & emotional capacity",
            "Boundaries": "Ability to hold limits",
            "Execution": "Following through on difficult conversations",
            "Feedback": "Repair & learning from conflict",
        },
        "Financial": {
            "Baseline": "Stability under financial stress",
            "Clarity": "Knowing your numbers & priorities",
            "Resources": "Income, buffer, tools",
            "Boundaries": "Control over spending & exposure",
            "Execution": "Actually doing the necessary actions",
            "Feedback": "Reviewing & closing leaks",
        },
        "Big Picture": {
            "Baseline": "Overall momentum & stability",
            "Clarity": "Clear direction & next step",
            "Resources": "Energy, support, environment",
            "Boundaries": "Protecting focus & saying no",
            "Execution": "Shipping & completing work",
            "Feedback": "Measuring & iterating",
        },
    }
    return translations.get(lens, {}).get(var, var)


def pressure_focus_summary(lens: str, weakest_var: str) -> str:
    summaries = {
        "Interpersonal": f"Biggest pressure is in **{weakest_var}** — likely too much emotional load or poor resolution patterns.",
        "Financial": f"Biggest pressure is in **{weakest_var}** — usually buffer, system, or leak problem.",
        "Big Picture": f"Biggest pressure is in **{weakest_var}** — goal is real, but structure/support isn't matching.",
    }
    return summaries.get(lens, f"Pressure concentrates in **{weakest_var}**.")


# ──────────────────────────────────────────────────────────────
# Question Bank (placeholder — fill with your real questions)
# ──────────────────────────────────────────────────────────────

QUESTION_BANK = {
    "Interpersonal": [],  # ← your ~75+ questions here
    "Financial": [],      # ← your ~75+ questions here
    "Big Picture": [],    # ← your ~75+ questions here
}

# Note: Make sure every question has unique "id" across ALL lenses
# Recommended structure:
# {"id": "i01", "text": "...", "variable": "Baseline", "weight": 1.2, "reverse": True}

# ──────────────────────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────────────────────

defaults = {
    "stage": "setup",
    "lens": "Interpersonal",
    "active_questions": [],
    "answers": {},
    "idx": 0,
    "followup_questions": [],
    "followup_answers": {},
    "followup_idx": 0,
    "followup_targets": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_session():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()


# ──────────────────────────────────────────────────────────────
# UI – Header & Sidebar
# ──────────────────────────────────────────────────────────────

st.title("Trifactor")
st.caption("Pressure mapping across three lenses")

with st.sidebar:
    st.header("Controls")
    st.caption("25 initial questions + targeted follow-ups")
    if st.button("Reset Everything", type="secondary"):
        reset_session()

# ──────────────────────────────────────────────────────────────
# Setup Screen – Lens Selection
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "setup":
    st.subheader("Choose your diagnostic lens")

    st.session_state.lens = st.radio(
        "Which area feels most pressurized right now?",
        options=LENSES,
        index=LENSES.index(st.session_state.lens),
        horizontal=True,
    )

    st.markdown(
        f"**Focus of this lens:** {lens_focus(st.session_state.lens)}  \n"
        "The tool will show you **where** the system is weakest — not how to fix it yet."
    )

    if st.button("Start 25 Questions", type="primary"):
        lens = st.session_state.lens
        bank = QUESTION_BANK.get(lens, [])

        if not bank:
            st.error("Question bank for this lens is empty. Add questions first.")
            st.stop()

        # Random sample of 25 (or all if fewer)
        k = min(25, len(bank))
        st.session_state.active_questions = random.sample(bank, k=k)
        st.session_state.answers = {}
        st.session_state.idx = 0
        st.session_state.stage = "questions"
        st.rerun()

# ──────────────────────────────────────────────────────────────
# Questions Stage (25 questions) — starts here
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "questions":
    # ── Your existing question loop code would go here ──
    pass
def compassionate_zone_line(zone: str) -> str:
    return {
        "RED": "needs support now (signal, not failure)",
        "YELLOW": "workable, but inconsistent under stress",
        "GREEN": "stable and helping you",
    }.get(zone, zone)

def lens_readout_intro(lens: str) -> str:
    if lens == "Interpersonal":
        return "Interpreting through **relationship dynamics**: tension, clarity, boundaries, follow-through."
    if lens == "Financial":
        return "Interpreting through **money stability + control**: clarity, buffer, boundaries, execution."
    return "Interpreting through **mission control**: clarity, focus, resources, execution, feedback loops."

def lens_translation(lens: str, variable: str) -> str:
    mapping = {
        "Interpersonal": {
            "Baseline": "Emotional baseline under contact",
            "Clarity": "What you want / what’s true",
            "Resources": "Support + emotional bandwidth",
            "Boundaries": "Limits + self-respect in action",
            "Execution": "Having the talk / doing the thing",
            "Feedback": "Repair, learning, reality-checking",
        },
----------------------
QUESTION_BANK = {
    "Interpersonal": [
        {"id":"i01","text":"How often do you feel tense before interacting with a specific person?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"i02","text":"How often does one conversation ruin your whole day?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"i03","text":"How often do you avoid a conversation you know you need to have?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"i04","text":"How clear are you about what you want from this relationship/situation?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"i05","text":"How often do you leave a talk unsure what was actually decided?","variable":"Clarity","weight":1.1,"reverse":True},
        {"id":"i06","text":"How often do you say “yes” when you mean “no”?","variable":"Boundaries","weight":1.4,"reverse":True},
        {"id":"i07","text":"How often do you tolerate behavior that you resent later?","variable":"Boundaries","weight":1.3,"reverse":True},
        {"id":"i08","text":"How often do you communicate your limits early rather than late?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"i09","text":"How supported do you feel by at least one person in your life?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"i10","text":"How often do you feel alone carrying the emotional load?","variable":"Resources","weight":1.2,"reverse":True},
        {"id":"i11","text":"How often do conflicts repeat without resolution?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"i12","text":"How often do you reflect after conflict and adjust your approach?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"i13","text":"How often do you interpret neutral behavior as hostile?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"i14","text":"How often do you apologize to restore peace even when you weren’t wrong?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"i15","text":"How often do you directly ask for what you need?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i16","text":"How often do you replay conversations in your head afterward?","variable":"Baseline","weight":1.0,"reverse":True},
        {"id":"i17","text":"How often do you feel respected in the dynamic?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i18","text":"How often do you keep your word when you set a boundary?","variable":"Execution","weight":1.3,"reverse":False},
        {"id":"i19","text":"How often do you use sarcasm/withdrawal instead of stating the issue?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"i20","text":"How often do you feel you must perform to be valued?","variable":"Clarity","weight":1.0,"reverse":True},
        {"id":"i21","text":"How often do you choose timing/location to improve the odds of a good talk?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"i22","text":"How often do you communicate expectations before frustration builds?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"i23","text":"How often do you recover quickly after conflict?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i24","text":"How often do you ask clarifying questions instead of assuming intent?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i25","text":"How often do you feel you’re walking on eggshells?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"i51","text":"How often do you notice resentment building before you name it?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"i52","text":"How often do you recover quickly after interpersonal strain?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i53","text":"How often do you feel conversations require translation instead of clarity?","variable":"Clarity","weight":1.2,"reverse":True},
        {"id":"i54","text":"How often do you address tone instead of content when tension arises?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"i55","text":"How often do you feel relational effort is uneven?","variable":"Resources","weight":1.2,"reverse":True},
        {"id":"i56","text":"How often do you say no without justification?","variable":"Boundaries","weight":1.3,"reverse":False},
        {"id":"i57","text":"How often do misunderstandings persist longer than necessary?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"i58","text":"How often do you revisit unresolved conversations?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"i59","text":"How often do you feel relationally resourced rather than depleted?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"i60","text":"How often do you check assumptions before reacting?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i61","text":"How often do you feel pressure to maintain harmony at your expense?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"i62","text":"How often do you name patterns instead of incidents?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"i63","text":"How often do you feel conversations reset rather than compound?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i64","text":"How often do you feel safe disagreeing?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i65","text":"How often do you delay resolution due to emotional fatigue?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"i66","text":"How often do you follow through on relational agreements?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i67","text":"How often do you feel conversations end cleanly?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"i68","text":"How often do you absorb blame to keep peace?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"i69","text":"How often do you experience mutual accountability?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"i70","text":"How often do you exit interactions with increased trust?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"i71","text":"How often do you recognize emotional debt accumulating?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"i72","text":"How often do you state needs without apology?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"i73","text":"How often do you feel relational stability across time?","variable":"Baseline","weight":1.2,"reverse":False},
        {"id":"i74","text":"How often do you resolve issues before they resurface?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i75","text":"How often do relationships feel directionally improving?","variable":"Resources","weight":1.3,"reverse":False},
    ],
    "Financial": [
        {"id":"f01","text":"How often do you know your exact cash position (today) without guessing?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"f02","text":"How often do bills/fees surprise you?","variable":"Clarity","weight":1.2,"reverse":True},
        {"id":"f03","text":"How often do you feel like you’re one emergency away from collapse?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"f04","text":"How often do you have a buffer (even small) after essentials?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f05","text":"How often do you spend to regulate mood/stress?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"f06","text":"How consistently do you track spending (even roughly)?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"f07","text":"How often do you miss due dates?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"f08","text":"How often do you avoid opening financial mail/notifications?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"f09","text":"How often do you negotiate rates, call providers, or challenge charges?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"f10","text":"How clear are you on your top 3 financial priorities this month?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f11","text":"How often do impulse purchases break your plan?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"f12","text":"How often do you review recurring subscriptions/auto-pay items?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"f13","text":"How often do you make a simple plan before spending (need vs want)?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f14","text":"How often does financial stress disrupt sleep/focus?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f15","text":"How often do you feel your income is stable/predictable?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"f16","text":"How often do you know your minimum survival number per month?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"f17","text":"How often do you take one concrete financial action per week?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f18","text":"How often do you use a system (notes/app/spreadsheet) to reduce chaos?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f19","text":"How often do you borrow/advance money to get through the month?","variable":"Resources","weight":1.1,"reverse":True},
        {"id":"f20","text":"How often do you postpone decisions until they become emergencies?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"f21","text":"How often do you set boundaries with others about money (loans, favors, guilt)?","variable":"Boundaries","weight":1.0,"reverse":False},
        {"id":"f22","text":"How often do you feel ashamed about money (and hide it)?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"f23","text":"How often do you have a realistic plan for the next 30 days?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f24","text":"How often do you follow that plan when stress hits?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f25","text":"How often do you recover quickly after a financial hit?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i26","text":"How often do you feel braced or guarded before contact?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"i27","text":"How often do you feel responsible for managing the other person’s emotions?","variable":"Boundaries","weight":1.3,"reverse":True},
        {"id":"i28","text":"How often do conversations drift instead of landing decisions?","variable":"Clarity","weight":1.1,"reverse":True},
        {"id":"i29","text":"How often do you initiate repair after tension?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"i30","text":"How often do you suppress irritation to keep things smooth?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"i31","text":"How often do you feel heard without needing to escalate?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i32","text":"How often do you delay speaking until the moment has passed?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"i33","text":"How often do you clarify expectations before conflict arises?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"i34","text":"How often do you feel emotionally safe being direct?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"i35","text":"How often do you feel blamed for things you didn’t cause?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"i36","text":"How often do you notice patterns repeating across different relationships?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i37","text":"How often do you hold back truth to avoid reaction?","variable":"Boundaries","weight":1.3,"reverse":True},
        {"id":"i38","text":"How often do you feel relief when distance increases?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"i39","text":"How often do you set terms before agreeing to help?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"i40","text":"How often do you leave interactions clearer than when you entered?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"i41","text":"How often do you address small issues before they stack?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i42","text":"How often do you feel obligated rather than willing?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"i43","text":"How often do you explicitly close a conversation with next steps?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"i44","text":"How often do you question your own perception after conflict?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"i45","text":"How often do you feel mutual effort in repair?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i46","text":"How often do you avoid topics that matter to you?","variable":"Clarity","weight":1.1,"reverse":True},
        {"id":"i47","text":"How often do you rest instead of ruminating after interaction?","variable":"Baseline","weight":1.0,"reverse":False},
        {"id":"i48","text":"How often do you say what you mean without softening it excessively?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"i49","text":"How often do you recalibrate behavior after feedback?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i50","text":"How often do relationships feel net-supportive rather than draining?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f26","text":"How often do you feel braced when checking your accounts?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f27","text":"How often do you delay looking at numbers you already know are bad?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"f28","text":"How often do you know exactly where the next dollar is coming from?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f29","text":"How often do you plan spending before money arrives?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f30","text":"How often do you spend defensively rather than intentionally?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"f31","text":"How often do you adjust behavior after a bad financial week?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"f32","text":"How often do you know which expense is the main pressure source?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"f33","text":"How often do you choose convenience over cost knowingly?","variable":"Boundaries","weight":1.0,"reverse":True},
        {"id":"f34","text":"How often do you make financial decisions under urgency?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f35","text":"How often do you review outcomes of past financial decisions?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"f36","text":"How often do you avoid commitments you can’t afford?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"f37","text":"How often do you feel your system is fragile?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"f38","text":"How often do you know what *not* to spend on right now?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"f39","text":"How often do you act quickly on small financial improvements?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f40","text":"How often do you feel trapped by past financial choices?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"f41","text":"How often do you consciously reduce exposure to risk?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f42","text":"How often do you maintain at least one financial buffer?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f43","text":"How often do you delay necessary purchases due to fear?","variable":"Baseline","weight":1.0,"reverse":True},
        {"id":"f44","text":"How often do you feel your finances are understandable?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f45","text":"How often do you execute the boring but stabilizing actions?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"f46","text":"How often do you revise plans when reality changes?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"f47","text":"How often do you stop spending before stress kicks in?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f48","text":"How often do you feel supported rather than cornered financially?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"f49","text":"How often do you treat finances as a system instead of emergencies?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"f50","text":"How often do you recover equilibrium after a hit?","variable":"Baseline","weight":1.2,"reverse":False},
        {"id":"f51","text":"How often do you recover financially after an unexpected hit?","variable":"Baseline","weight":1.2,"reverse":False},
        {"id":"f52","text":"How often do financial worries bleed into other decisions?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"f53","text":"How often do you recognize false economies?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"f54","text":"How often do you choose flexibility over optimization?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f55","text":"How often do fixed costs feel constraining?","variable":"Resources","weight":1.2,"reverse":True},
        {"id":"f56","text":"How often do you decline opportunities due to cash timing?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"f57","text":"How often do you feel financially brittle?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f58","text":"How often do you know your break-even point?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"f59","text":"How often do you re-negotiate obligations?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f60","text":"How often do you notice compounding stress from small leaks?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"f61","text":"How often do you act to reduce fragility?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"f62","text":"How often do you feel optional rather than cornered?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f63","text":"How often do you avoid financial commitments that limit exit?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"f64","text":"How often do you track downside as carefully as upside?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"f65","text":"How often do financial decisions age well?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"f66","text":"How often do you feel one bill away from disruption?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f67","text":"How often do you trade short-term relief for long-term pressure?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"f68","text":"How often do you preserve cash as leverage?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f69","text":"How often do you act early instead of waiting for crisis?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"f70","text":"How often do you understand second-order financial effects?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f71","text":"How often do you feel financially boxed in?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"f72","text":"How often do you intentionally simplify finances?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f73","text":"How often do you correct course without self-blame?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"f74","text":"How often do you maintain financial slack?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f75","text":"How often does your financial system feel resilient?","variable":"Baseline","weight":1.2,"reverse":False},
    ],
    "Big Picture": [
        {"id":"b01","text":"How clear is your north star (what you’re building / aiming at)?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b02","text":"How often do you feel scattered across too many threads?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"b03","text":"How often do you know the next smallest step without overthinking?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"b04","text":"How often do you have enough energy/bandwidth to execute?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b05","text":"How often do you burn time on tasks that don’t move the mission?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"b06","text":"How often do you ship something (even small) rather than refine forever?","variable":"Execution","weight":1.3,"reverse":False},
        {"id":"b07","text":"How often do you change direction mid-week?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"b08","text":"How often do you measure progress with a real metric (not vibes)?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"b09","text":"How often do you review what worked and adjust your plan?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"b10","text":"How often do you ignore obvious signals because they’re inconvenient?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"b11","text":"How often do you protect focus time from interruptions?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"b12","text":"How often do you feel you’re operating without a buffer?","variable":"Resources","weight":1.1,"reverse":True},
        {"id":"b13","text":"How often do you have a simple weekly plan you can actually follow?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b14","text":"How often do you let urgency from others rewrite your priorities?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"b15","text":"How often do you know what to say “no” to right now?","variable":"Clarity","weight":1.0,"reverse":False},
        {"id":"b16","text":"How often do you feel meaningful momentum?","variable":"Baseline","weight":1.0,"reverse":False},
        {"id":"b17","text":"How often do you procrastinate on the one scary keystone task?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"b18","text":"How often do you have access to help/support/tools when stuck?","variable":"Resources","weight":1.0,"reverse":False},
        {"id":"b19","text":"How often do you document decisions so you don’t relitigate them?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"b20","text":"How often do you feel your environment is aligned with your goals?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"b21","text":"How often do you stop to simplify when complexity rises?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"b22","text":"How often do you complete what you start?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"b23","text":"How often do you experience “mission drift” after setbacks?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"b24","text":"How often do you pick one lever and push it hard for 7 days?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b25","text":"How often do you feel the goal is real and reachable?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"b26","text":"How often do you feel the mission pulling rather than pushing you?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"b27","text":"How often do you know what *not* to work on right now?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b28","text":"How often do you feel the system is overloaded?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"b29","text":"How often do you simplify when complexity increases?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"b30","text":"How often do you feel supported by your environment?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b31","text":"How often do you complete cycles rather than abandon them?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"b32","text":"How often do you drift due to external noise?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"b33","text":"How often do you identify the true bottleneck?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b34","text":"How often do you act without waiting for certainty?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b35","text":"How often do you revisit assumptions that may be outdated?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"b36","text":"How often do you protect energy as a strategic resource?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b37","text":"How often do you feel reactive instead of deliberate?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"b38","text":"How often do you reduce scope instead of adding more?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"b39","text":"How often do you experience false urgency?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"b40","text":"How often do you know the next stabilizing move?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"b41","text":"How often do you execute despite incomplete information?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b42","text":"How often do you feel constrained by system limits?","variable":"Resources","weight":1.0,"reverse":True},
        {"id":"b43","text":"How often do you notice drift early?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"b44","text":"How often do you consciously slow the system down?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"b45","text":"How often do you feel aligned with the direction?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"b46","text":"How often do you cut losses instead of doubling down?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"b47","text":"How often do you choose leverage over effort?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b48","text":"How often do you maintain momentum without burnout?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b49","text":"How often do you execute the smallest viable step?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b50","text":"How often does the system feel directionally sound?","variable":"Baseline","weight":1.2,"reverse":False},
        {"id":"b51","text":"How often do you feel effort exceeds return?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"b52","text":"How often do you feel directionally aligned?","variable":"Baseline","weight":1.2,"reverse":False},
        {"id":"b53","text":"How often do you notice leverage decay?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"b54","text":"How often do you prune initiatives intentionally?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"b55","text":"How often do you experience strategic drift?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"b56","text":"How often do you simplify the system to regain control?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"b57","text":"How often do you feel supported by structure?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b58","text":"How often do you recognize misaligned incentives?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b59","text":"How often do you feel busy but ineffective?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"b60","text":"How often do you redesign instead of push harder?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"b61","text":"How often do you maintain coherence across efforts?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"b62","text":"How often do you stop initiatives that aren’t working?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"b63","text":"How often do constraints feel informative rather than limiting?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"b64","text":"How often do you feel pulled off-mission?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"b65","text":"How often do you re-anchor to first principles?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b66","text":"How often do you reduce entropy intentionally?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b67","text":"How often do you feel leverage compounding?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b68","text":"How often do you notice when effort stops scaling?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"b69","text":"How often do you choose focus over expansion?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"b70","text":"How often does the system self-correct?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"b71","text":"How often do you exit paths cleanly?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"b72","text":"How often do you maintain strategic slack?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"b73","text":"How often do you see around second-order effects?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"b74","text":"How often do you course-correct without panic?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"b75","text":"How often does the direction still feel worth pursuing?","variable":"Baseline","weight":1.2,"reverse":False},
    ],
}

# --------------------------
# Scoring + Follow-ups
# -----import random
from statistics import pstdev
import streamlit as st

st.set_page_config(page_title="Trifactor Diagnostic", layout="centered")

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

LENSES = ["Interpersonal", "Financial", "Big Picture"]

SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

VARIABLE_WEIGHTS = {
    "Baseline": 1.2,
    "Clarity": 1.1,
    "Resources": 1.1,
    "Boundaries": 1.1,
    "Execution": 1.2,
    "Feedback": 1.0,
}

# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────

def clamp(n, lo, hi):
    return max(lo, min(hi, n))


def zone_name(score: float) -> str:  # 0–100
    if score < 45:
        return "RED"
    if score < 70:
        return "YELLOW"
    return "GREEN"


def zone_message(zone: str) -> str:
    return {
        "RED": "broken — needs urgent attention",
        "YELLOW": "unstable — fragile under pressure",
        "GREEN": "solid — working well",
    }[zone]


def lens_focus(lens: str) -> str:
    return {
        "Interpersonal": "relationship tension, clarity, boundaries, execution",
        "Financial": "money stability, buffer, boundaries, execution",
        "Big Picture": "mission clarity, resources, focus, execution, feedback",
    }[lens]


def variable_translation(lens: str, var: str) -> str:
    translations = {
        "Interpersonal": {
            "Baseline": "Emotional stability under contact",
            "Clarity": "Knowing what you want / what's true",
            "Resources": "Support & emotional capacity",
            "Boundaries": "Ability to hold limits",
            "Execution": "Following through on difficult conversations",
            "Feedback": "Repair & learning from conflict",
        },
        "Financial": {
            "Baseline": "Stability under financial stress",
            "Clarity": "Knowing your numbers & priorities",
            "Resources": "Income, buffer, tools",
            "Boundaries": "Control over spending & exposure",
            "Execution": "Actually doing the necessary actions",
            "Feedback": "Reviewing & closing leaks",
        },
        "Big Picture": {
            "Baseline": "Overall momentum & stability",
            "Clarity": "Clear direction & next step",
            "Resources": "Energy, support, environment",
            "Boundaries": "Protecting focus & saying no",
            "Execution": "Shipping & completing work",
            "Feedback": "Measuring & iterating",
        },
    }
    return translations.get(lens, {}).get(var, var)


def pressure_focus_summary(lens: str, weakest_var: str) -> str:
    summaries = {
        "Interpersonal": f"Biggest pressure is in **{weakest_var}** — likely too much emotional load or poor resolution patterns.",
        "Financial": f"Biggest pressure is in **{weakest_var}** — usually buffer, system, or leak problem.",
        "Big Picture": f"Biggest pressure is in **{weakest_var}** — goal is real, but structure/support isn't matching.",
    }
    return summaries.get(lens, f"Pressure concentrates in **{weakest_var}**.")


# ──────────────────────────────────────────────────────────────
# Question Bank (placeholder — fill with your real questions)
# ──────────────────────────────────────────────────────────────

QUESTION_BANK = {
    "Interpersonal": [],  # ← your ~75+ questions here
    "Financial": [],      # ← your ~75+ questions here
    "Big Picture": [],    # ← your ~75+ questions here
}

# Note: Make sure every question has unique "id" across ALL lenses
# Recommended structure:
# {"id": "i01", "text": "...", "variable": "Baseline", "weight": 1.2, "reverse": True}

# ──────────────────────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────────────────────

defaults = {
    "stage": "setup",
    "lens": "Interpersonal",
    "active_questions": [],
    "answers": {},
    "idx": 0,
    "followup_questions": [],
    "followup_answers": {},
    "followup_idx": 0,
    "followup_targets": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_session():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()


# ──────────────────────────────────────────────────────────────
# UI – Header & Sidebar
# ──────────────────────────────────────────────────────────────

st.title("Trifactor")
st.caption("Pressure mapping across three lenses")

with st.sidebar:
    st.header("Controls")
    st.caption("25 initial questions + targeted follow-ups")
    if st.button("Reset Everything", type="secondary"):
        reset_session()

# ──────────────────────────────────────────────────────────────
# Setup Screen – Lens Selection
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "setup":
    st.subheader("Choose your diagnostic lens")

    st.session_state.lens = st.radio(
        "Which area feels most pressurized right now?",
        options=LENSES,
        index=LENSES.index(st.session_state.lens),
        horizontal=True,
    )

    st.markdown(
        f"**Focus of this lens:** {lens_focus(st.session_state.lens)}  \n"
        "The tool will show you **where** the system is weakest — not how to fix it yet."
    )

    if st.button("Start 25 Questions", type="primary"):
        lens = st.session_state.lens
        bank = QUESTION_BANK.get(lens, [])

        if not bank:
            st.error("Question bank for this lens is empty. Add questions first.")
            st.stop()

        # Random sample of 25 (or all if fewer)
        k = min(25, len(bank))
        st.session_state.active_questions = random.sample(bank, k=k)
        st.session_state.answers = {}
        st.session_state.idx = 0
        st.session_state.stage = "questions"
        st.rerun()

# ──────────────────────────────────────────────────────────────
# Questions Stage (25 questions) — starts here
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "questions":
    # ── Your existing question loop code would go here ──
    pass
    if len(picked) < n:
        c2 = [q for q in bank if (q["id"] not in already_asked_ids) and (q not in picked)]
        random.shuffle(c2)
        picked.extend(c2[: (n - len(picked))])

    if len(picked) < n:
        c3 = [q for q in bank if (q["variable"] in targets) and (q not in picked)]
        random.shuffle(c3)
        picked.extend(c3[: (n - len(picked))])

    if len(picked) < n:
        c4 = [q for q in bank if q not in picked]
        random.shuffle(c4)
        picked.extend(c4[: (n - len(picked))])

    return picked[:n]

# --------------------------
# Session State Initialization (must be ABOVE stage checks)
# --------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "setup"

if "lens" not in st.session_state:
    st.session_state.lens = "Interpersonal"

if "active_questions" not in st.session_state:
    st.session_state.active_questions = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "idx" not in st.session_state:
    st.session_state.idx = 0

if "followup_questions" not in st.session_state:
    st.session_state.followup_questions = []

if "followup_answers" not in st.session_state:
    st.session_state.followup_answers = {}  # (qid, idx) -> val

if "followup_idx" not in st.session_state:
    st.session_state.followup_idx = 0

if "followup_targets" not in st.session_state:
    st.session_state.followup_targets = []

def reset_run():
    st.session_state.stage = "setup"
    st.session_state.active_questions = []
    st.session_state.answers = {}
    st.session_state.idx = 0
    st.session_state.followup_questions = []
    st.session_state.followup_answers = {}
    st.session_state.followup_idx = 0
    st.session_state.followup_targets = []

# --------------------------
# Sidebar (Reset only)
# --------------------------
with st.sidebar:
    st.header("Controls")
    st.write("Initial questions: **25**")
    st.write("Follow-ups: **10**")
    if st.button("Reset", key="btn_reset_sidebar_v1"):
        reset_run()
        st.rerun()

# --------------------------
# Setup Screen (Lens Picker)
# --------------------------
if st.session_state.stage == "setup":
    st.subheader("Pick a lens to begin")

    st.session_state.lens = st.radio(
        "Is this interpersonal, financial, or big picture?",
        LENSES,
        index=LENSES.index(st.session_state.lens),
        key="radio_lens_setup_v1",
    )

    st.caption(
    "This doesn’t give insight. It gives prioritization."
    "You’ll see which part is actually costing you the most right now."
)

    if st.button("Start 25 questions", type="primary", key="btn_start_25_v1"):
        lens = st.session_state.lens
        bank = QUESTION_BANK[lens][:]
        random.shuffle(bank)

        k = min(25, len(bank))
        st.session_state.active_questions = random.sample(bank, k=k)
        st.session_state.answers = {}
        st.session_state.idx = 0

        st.session_state.followup_questions = []
        st.session_state.followup_answers = {}
        st.session_state.followup_idx = 0
        st.session_state.followup_targets = []

        st.session_state.stage = "questions"
        st.rerun()

# --------------------------
# Questions (25)
# --------------------------
if st.session_state.stage == "questions":
    lens = st.session_state.lens
    qs = st.session_state.active_questions
    total = len(qs)
    idx = st.session_state.idx

    st.subheader(f"{lens} lens — Question {idx+1} of {total}")
    st.progress((idx) / total)

    q = qs[idx]
    st.write(f"**{q['text']}**")
    st.caption(f"Measures: {lens_translation(lens, q['variable'])}")

    current = st.session_state.answers.get(q["id"], None)
    options = list(SCALE_LABELS.keys())

    choice = st.radio(
        "Choose one:",
        options,
        index=options.index(current) if current in options else 2,
        format_func=lambda x: SCALE_LABELS[x],
        key=f"radio_main_{q['id']}_{idx}_v1",
    )
    st.session_state.answers[q["id"]] = int(choice)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Back", disabled=(idx == 0), key=f"btn_back_{idx}_v1"):
            st.session_state.idx = max(0, idx - 1)
            st.rerun()
    with col2:
        if st.button("Next", disabled=(idx >= total - 1), key=f"btn_next_{idx}_v1"):
            st.session_state.idx = min(total - 1, idx + 1)
            st.rerun()
    with col3:
        if st.button("Finish & Score", type="primary", key="btn_finish_score_v1"):
            st.session_state.stage = "results"
            st.rerun()

# --------------------------
# Readout renderer
# --------------------------
def render_readout(title, lens, questions_all, answers_all):
    overall, per_variable, scored_qs_sorted = compute_scores(questions_all, answers_all)

    st.subheader(title)
    st.write(lens_readout_intro(lens))
    st.metric("Overall Score (0–100)", f"{overall:.1f}")

    st.write("### Category scores")
    for v in VARIABLE_WEIGHTS.keys():
        if v not in per_variable:
            continue
        info = per_variable[v]
        label = lens_translation(lens, v)
        st.write(
            f"- **{label}**: **{info['pct']:.1f}** — {compassionate_zone_line(info['zone'])} "
            f"(volatility {info['volatility']:.0f}/100)"
        )
    # Explain volatility cause (new)
    var_items = [t for t in scored_qs_sorted if t[0] == v]
    if len(var_items) >= 2:
        weakest = sorted(var_items, key=lambda t: t[1])[0]
        strongest = sorted(var_items, key=lambda t: -t[1])[0]

        if abs(strongest[1] - weakest[1]) >= 2:
            st.caption(
                f"Volatility here comes from inconsistency between: "
                f"“{strongest[3]['text']}” and “{weakest[3]['text']}”."
        )

    vars_present_sorted = sorted(
        [(v, per_variable[v]["pct"]) for v in per_variable],
        key=lambda x: x[1]
    )
    targets = choose_followup_targets(per_variable)

    if vars_present_sorted:
        lowest = vars_present_sorted[0][0]
        highest = vars_present_sorted[-1][0]
        low_label = lens_translation(lens, lowest)
        high_label = lens_translation(lens, highest)

        # Verdict line (new)
        st.markdown(
            f"**Right now, the system isn’t failing everywhere — it’s failing most at _{low_label}_.**"
        )

        st.write("### Where you are")
        st.write(f"- **What’s holding steady:** {high_label} (**{per_variable[highest]['pct']:.1f}**)")
        st.write(
            f"- **Where pressure is building:** {low_label} (**{per_variable[lowest]['pct']:.1f}**) — "
            f"{compassionate_zone_line(per_variable[lowest]['zone'])}"
        )
        st.write(compassionate_summary(lens, low_label))

        st.write("### What’s dragging you down (lowest signals)")
        for v, s, w, q, a in scored_qs_sorted[:5]:
            st.write(f"- {q['text']}  \n  ↳ signal **{s}/4** (weight {w})")

        # Renamed header (new)
        st.write("### Start here (smallest stabilizing lever)")
        low_var_items = [t for t in scored_qs_sorted if t[0] == lowest]
        if low_var_items:
            lever = sorted(low_var_items, key=lambda t: (t[1], -t[2]))[0]
            v, s, w, q, a = lever
            st.write(f"**Start here:** {q['text']}")
            st.caption("You’re not fixing everything at once. You’re stabilizing the weakest point first.")

        # Leash block (new)
        st.divider()
        st.markdown(
            "**This tool shows you where the pressure is.**  \n"
            "**It does not design the fix.**"
        )
        st.markdown(
            "If you’re trying to resolve something complex, layered, or long-standing, "
            "the next step isn’t more questions — it’s interpretation."
        )
        st.markdown("All contact and follow-up options are provided inside the app.")
        st.caption(
            "Trifactor is a pressure-mapping tool for clarity and prioritization. "
            "It is not therapy, coaching, or professional advice."
        )
        st.caption(
            "Run this once a week. If the lowest area doesn’t change after two runs, "
            "you’re pushing the wrong lever."
        )

        st.write("### Continue evaluation focus")
        st.write("- We’ll ask 10 follow-ups mainly in these areas:")
        for v in targets:
            st.write(f"  - {lens_translation(lens, v)}")

    return overall, per_variable, scored_qs_sorted, targets


# --------------------------
# Leash / Completion Framing
# --------------------------
st.divider()

st.markdown(
    "**This tool shows you where the pressure is.**  \n"
    "**It does not design the fix.**"
)

st.markdown(
    "Trifactor is a first-pass diagnostic. If you’re dealing with something complex, layered, "
    "or long-standing, the next step isn’t more questions — it’s interpretation."
)

st.markdown(
    "If you want to work this through properly, contact me."
)

st.markdown(
    "**Email:** contributionism@giveittogot.com  \n"
    "**Subject:** Trifactor follow-up"
)

st.caption(
    "Trifactor is not therapy, coaching, or professional advice. "
    "It’s a pressure-mapping tool. What you do next matters more than the score."
)

# --------------------------
# Results (after 25)
# --------------------------
if st.session_state.stage == "results":
    lens = st.session_state.lens
    qs = st.session_state.active_questions
    answers = st.session_state.answers

    overall, per_variable, scored_sorted, targets = render_readout(
        title="Readout (after 25 questions)",
        lens=lens,
        questions_all=qs,
        answers_all=answers,
    )

    st.divider()

    already = set([q["id"] for q in qs])
    followups = pick_followup_questions(lens, targets, already_asked_ids=already, n=10)
    if any(q["id"] in already for q in followups):
        st.info("Follow-ups may repeat right now because each lens only has 25 questions. Add more questions to remove repeats.")

    colA, colB, colC = st.columns([2, 1, 1])
    with colA:
        if st.button("Continue evaluation (10 follow-ups)", type="primary", key="btn_continue_fu_v1"):
            st.session_state.followup_targets = targets
            st.session_state.followup_questions = followups
            st.session_state.followup_answers = {}
            st.session_state.followup_idx = 0
            st.session_state.stage = "followups"
            st.rerun()
    with colB:
        if st.button("New run (same lens)", key="btn_new_run_same_v1"):
            bank = QUESTION_BANK[lens][:]
            random.shuffle(bank)
            k = min(25, len(bank))
            st.session_state.active_questions = random.sample(bank, k=k)
            st.session_state.answers = {}
            st.session_state.idx = 0
            st.session_state.stage = "questions"
            st.rerun()
    with colC:
        if st.button("Change lens", key="btn_change_lens_v1"):
            reset_run()
            st.rerun()

    st.write("### Export (copy/paste)")
    st.code(
        {
            "lens": lens,
            "phase": "after_25",
            "overall": round(overall, 2),
            "variables": {v: round(per_variable[v]["pct"], 2) for v in per_variable},
            "answers": answers,
            "targets": targets,
        },
        language="python",
    )

# --------------------------
# Follow-ups (10)
# --------------------------
if st.session_state.stage == "followups":
    lens = st.session_state.lens
    fqs = st.session_state.followup_questions
    total = len(fqs)
    idx = st.session_state.followup_idx

    st.subheader(f"Follow-ups — {idx+1} of {total}")
    st.caption("Targeted to your lowest zones. Same scoring.")
    st.progress((idx) / total)

    q = fqs[idx]
    st.write(f"**{q['text']}**")
    st.caption(f"Measures: {lens_translation(lens, q['variable'])}")

    current = st.session_state.followup_answers.get((q["id"], idx), None)
    options = list(SCALE_LABELS.keys())

    choice = st.radio(
        "Choose one:",
        options,
        index=options.index(current) if current in options else 2,
        format_func=lambda x: SCALE_LABELS[x],
        key=f"radio_follow_{q['id']}_{idx}_v1",
    )
    st.session_state.followup_answers[(q["id"], idx)] = int(choice)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Back", disabled=(idx == 0), key=f"btn_fu_back_{idx}_v1"):
            st.session_state.followup_idx = max(0, idx - 1)
            st.rerun()
    with col2:
        if st.button("Next", disabled=(idx >= total - 1), key=f"btn_fu_next_{idx}_v1"):
            st.session_state.followup_idx = min(total - 1, idx + 1)
            st.rerun()
    with col3:
         if st.button("Finish follow-ups & Re-score", type="primary", key="btn_fu_finish_v1"):
            st.session_state.stage = "export_form"
            st.rerun()
# --------------------------
# Export Form (between followups and results2)
# --------------------------
if st.session_state.stage == "export_form":
    lens = st.session_state.lens

    base_qs = st.session_state.active_questions
    base_answers = st.session_state.answers

    fqs = st.session_state.followup_questions
    fu_answers_raw = st.session_state.followup_answers  # (qid, idx) -> val

    merged_questions = base_qs[:] + fqs[:]
    merged_answers = dict(base_answers)
    for (qid, _i), val in fu_answers_raw.items():
        merged_answers[qid] = int(val)

    # (Optional) compute the numbers now so you can paste them into the form
    overall2, per_var2, scored2, targets2 = render_readout(
        title="Readout (after 25 + 10 follow-ups) — preview",
        lens=lens,
        questions_all=merged_questions,
        answers_all=merged_answers,
    )

    st.divider()
    st.write("### Save this run (Google Form)")
    st.caption("Fill the form, then come back here and press Continue.")

    # IMPORTANT: use your *embed* URL (docs.google.com/forms/d/e/.../viewform?embedded=true)
    st.markdown(
        """
        <iframe
        src=https://docs.google.com/forms/d/e/1FAIpQLSciFAyvy7W5cwepglPL_zrC0PfoQK951sbuO_1eMCPfZ6fW9w/viewform?usp=dialog
        width="100%"
        height="1200"
        frameborder="0"
        marginheight="0"
        marginwidth="0">
        Loading…
        </iframe>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("### Export (copy/paste into form)")
        st.code(
            {
                "lens": lens,
                "phase": "after_25_plus_10",
                "overall": round(overall2, 2),
                "variables": {v: round(per_var2[v]["pct"], 2) for v in per_var2},
                "answers": merged_answers,
                "targets": targets2,
            },
            language="python",
        )

    with col2:
        if st.button("Continue to Results", type="primary", key="btn_continue_results2_v1"):
            st.session_state.stage = "results2"
            st.rerun()
# --------------------------
# Results (after 25 + 10)
# --------------------------
if st.session_state.stage == "results2":
    lens = st.session_state.lens

    base_qs = st.session_state.active_questions
    base_answers = st.session_state.answers

    fqs = st.session_state.followup_questions
    fu_answers_raw = st.session_state.followup_answers  # (qid, idx) -> val

    merged_questions = base_qs[:] + fqs[:]
    merged_answers = dict(base_answers)
    for (qid, _i), val in fu_answers_raw.items():
        merged_answers[qid] = int(val)

    overall2, per_var2, scored2, targets2 = render_readout(
        title="Readout (after 25 + 10 follow-ups)",
        lens=lens,
        questions_all=merged_questions,
        answers_all=merged_answers,
    )

    st.divider()
    st.write("### Export (copy/paste)")
    st.code(
        {
            "lens": lens,
            "phase": "after_25_plus_10",
            "overall": round(overall2, 2),
            "variables": {v: round(per_var2[v]["pct"], 2) for v in per_var2},
            "answers": merged_answers,
            "targets": targets2,
        },
        language="python",
    )

    colA, colB, colC = st.columns([2, 1, 1])
    with colA:
        if st.button("Run another 10 follow-ups", type="primary", key="btn_more_fu_v1"):
            next_targets = choose_followup_targets(per_var2)
            already_ids = set([q["id"] for q in merged_questions])
            next_fus = pick_followup_questions(lens, next_targets, already_asked_ids=already_ids, n=10)

            st.session_state.followup_targets = next_targets
            st.session_state.followup_questions = next_fus
            st.session_state.followup_answers = {}
            st.session_state.followup_idx = 0
            st.session_state.stage = "followups"
            st.rerun()
    with colB:
        if st.button("New run (same lens)", key="btn_new_run_same2_v1"):
            bank = QUESTION_BANK[lens][:]
            random.shuffle(bank)
            k = min(25, len(bank))
            st.session_state.active_questions = random.sample(bank, k=k)
            st.session_state.answers = {}
            st.session_state.idx = 0
            st.session_state.followup_questions = []
            st.session_state.followup_answers = {}
            st.session_state.followup_idx = 0
            st.session_state.stage = "questions"
            st.rerun()
    with colC:
        if st.button("Change lens", key="btn_change_lens2_v1"):
            reset_run()
            st.rerun()

# --------------------------
# Sidebar footer hint
# --------------------------
st.sidebar.divider()
st.sidebar.caption("Add more questions by appending dicts into QUESTION_BANK for each lens (unique ids like i26, f26, b26...).")
