import streamlit as st
import random

def generate_question(level):
    if level == 14:
        num1 = random.randint(0, 12)
    else:
        num1 = level - 1 if level < 14 else random.randint(0, 12)
    num2 = random.randint(0, 12)
    return num1, num2, num1 + num2

def main():
    st.title("Math Facts Game")
    
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "num1" not in st.session_state:
        st.session_state.num1, st.session_state.num2, st.session_state.answer = generate_question(st.session_state.level)
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""
    if "avatar" not in st.session_state:
        st.session_state.avatar = "😊"
    
    st.sidebar.header("Select Level")
    level_selection = st.sidebar.selectbox("Choose your starting level:", list(range(1, 15)), index=st.session_state.level - 1)
    st.session_state.avatar = st.sidebar.selectbox("Choose your avatar:", ["😊", "😎", "🤓", "👾", "🐱"])
    
    if st.sidebar.button("Start Game"):
        st.session_state.level = level_selection
        st.session_state.score = 0
        st.session_state.num1, st.session_state.num2, st.session_state.answer = generate_question(st.session_state.level)
        st.session_state.feedback = ""
        st.rerun()
    
    st.write(f"### Level {st.session_state.level} {st.session_state.avatar}")
    st.write(f"### Score: {st.session_state.score}")
    st.progress(st.session_state.score / 15)
    st.write(f"## {st.session_state.num1} + {st.session_state.num2} = ?")
    
    answer = st.text_input("Enter your answer:", key="user_answer", on_change=lambda: check_answer(st.session_state.user_answer))
    
    if st.session_state.feedback:
        st.markdown(st.session_state.feedback, unsafe_allow_html=True)
    
    def check_answer(answer):
        try:
            user_answer = int(answer)
            if user_answer == st.session_state.answer:
                st.session_state.score += 1
                st.session_state.feedback = "✅ <span style='color:green;'>Yes! Great job!</span>"
            else:
                st.session_state.score -= 1
                st.session_state.feedback = "❌ <span style='color:red;'>Oops! Try again.</span>"
        except ValueError:
            st.session_state.feedback = "⚠️ <span style='color:orange;'>Please enter a valid number.</span>"
        
        if st.session_state.score >= 15:
            st.balloons()
            if st.session_state.level == 14:
                st.session_state.feedback = "🎉 <span style='color:blue;'>YOU WON THE GAME!</span> 🎉"
                st.session_state.score = 0
            else:
                st.session_state.level += 1
                st.session_state.score = 0
                st.session_state.feedback = "🎉 <span style='color:purple;'>Congratulations! Level Up!</span>"
                st.balloons()
        elif st.session_state.score < 0:
            st.session_state.score = 0
            st.session_state.feedback = "🔄 <span style='color:red;'>You lost! Restarting level...</span>"
            st.session_state.num1, st.session_state.num2, st.session_state.answer = generate_question(st.session_state.level)
        
        st.session_state.user_answer = ""
        st.rerun()

if __name__ == "__main__":
    main()
