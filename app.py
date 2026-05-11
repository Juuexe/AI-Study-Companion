import streamlit as st
from document_parser import extract_text, chunk_text
from generator import generate_flashcards, generate_quiz, generate_summary

st.set_page_config(page_title="AI Study Companion", page_icon="")
st.title("AI Study Companion")
st.caption("Upload your notes or lecture slides and let AI do the studying prep for you.")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    with st.spinner("Reading document..."):
        raw_text = extract_text(uploaded)
        chunks = chunk_text(raw_text)
        context = chunks[0]

    st.success(f"Document loaded — {len(raw_text.split())} words found.")

    tab1, tab2, tab3 = st.tabs(["Summary", "Flashcards", "Quiz"])

    with tab1:
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary = generate_summary(context)
            st.markdown(summary)

    with tab2:
        num_cards = st.slider("Number of flashcards", 5, 20, 10)
        if st.button("Generate Flashcards"):
            with st.spinner("Creating flashcards..."):
                cards = generate_flashcards(context, num_cards)
            for i, card in enumerate(cards):
                with st.expander(f"Card {i+1}: {card['question']}"):
                    st.write(card["answer"])

    with tab3:
        num_q = st.slider("Number of questions", 3, 10, 5)
        if st.button("Generate Quiz"):
            with st.spinner("Building quiz..."):
                st.session_state.questions = generate_quiz(context, num_q)
                st.session_state.answers = {}

        if "questions" in st.session_state:
            score = 0
            for i, q in enumerate(st.session_state.questions):
                st.subheader(f"Q{i+1}: {q['question']}")
                choice = st.radio("", q["options"], key=f"q{i}")
                st.session_state.answers[i] = choice

            if st.button("Submit Quiz"):
                for i, q in enumerate(st.session_state.questions):
                    if st.session_state.answers.get(i) == q["answer"]:
                        st.success(f"Q{i+1}: Correct!")
                        score += 1
                    else:
                        st.error(f"Q{i+1}: Incorrect — {q['explanation']}")
                st.info(f"Your score: {score}/{len(st.session_state.questions)}")