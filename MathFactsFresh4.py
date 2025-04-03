import streamlit as st
import random

st.set_page_config(page_title="Math Facts Game", page_icon="🎓")

# Initialize session state variables
if 'level' not in st.session_state:
    st.session_state.level = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'problems' not in st.session_state:
    st.session_state.problems = []
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None
if 'used_problems' not in st.session_state:
    st.session_state.used_problems = set()
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_won' not in st.session_state:
    st.session_state.game_won = False
if 'trigger_rerun' not in st.session_state:
    st.session_state.trigger_rerun = False

# ✅ Safe rerun logic placed early
if st.session_state.get('trigger_rerun', False):
    st.session_state.trigger_rerun = False
    st.experimental_rerun()


def generate_problems(level):
    if level < 14:
        a = level
        return [(a, b) for b in range(13)]
    else:
        return [(a, b) for a in range(13) for b in range(13)]


def pick_new_problem():
    available = [p for p in st.session_state.problems if p not in st.session_state.used_problems]
    if available:
        problem = random.choice(available)
        st.session_state.used_problems.add(problem)
        return problem
    return None


st.title("🎓 Math Facts Game")

if st.session_state.level is None:
    st.header("Select a Level to Begin")
    level = st.selectbox("Choose Level", list(range(1, 15)))
    if st.button("Start Game"):
        st.session_state.level = level
        st.session_state.score = 0
        st.session_state.problems = generate_problems(level - 1)
        st.session_state.used_problems = set()
        st.session_state.current_problem = pick_new_problem()
        st.session_state.trigger_rerun = True
else:
    st.subheader(f"Level {st.session_state.level}")
    st.write("Answer the problems to reach 15 points!")
    st.progress(st.session_state.score / 15)

    if st.session_state.current_problem:
        a, b = st.session_state.current_problem
        form = st.form(key="answer_form")
        form.write(f"What is {a} + {b}?")
        answer = form.text_input("Your Answer", key="answer")
        submitted = form.form_submit_button("Submit")

        if submitted and answer.strip().isdigit():
            if int(answer.strip()) == a + b:
                st.session_state.score += 1
                st.success("Correct! Great job!")
            else:
                st.session_state.score -= 1
                st.warning(random.choice([
                    "Oops! Try again!",
                    "You're doing great, keep going!",
                    "Don't give up!"
                ]))

            if st.session_state.score >= 15:
                if st.session_state.level == 14:
                    st.session_state.game_won = True
                else:
                    st.session_state.level += 1
                st.session_state.score = 0
                st.session_state.problems = generate_problems(st.session_state.level - 1)
                st.session_state.used_problems = set()

            elif st.session_state.score < 0:
                st.session_state.score = 0
                st.session_state.used_problems = set()
                st.warning("Level restarting. Try again!")

            st.session_state.current_problem = pick_new_problem()
            st.session_state.trigger_rerun = True

    if st.session_state.current_problem is None and not st.session_state.game_won:
        st.session_state.used_problems = set()
        st.session_state.current_problem = pick_new_problem()
        st.session_state.trigger_rerun = True

    if st.session_state.game_won:
        st.balloons()
        st.success("🎉 Congratulations! You've completed all levels! 🎉")
        if st.button("Play Again"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.trigger_rerun = True

    if st.button("Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.trigger_rerun = True
