import streamlit as st
import os
from document_parser import extract_text, chunk_text
from generator import generate_flashcards, generate_quiz, generate_summary

st.set_page_config(page_title="AI Study Companion", page_icon=None, layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #000000;
            color: #FFFFFF;
        }

        .block-container {
            padding-top: 3rem;
            max-width: 720px;
        }

        h1 {
            color: #1DB954;
            font-size: 2.4rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: -0.5px;
        }

        .subtitle {
            text-align: center;
            color: #B3B3B3;
            font-size: 0.95rem;
            margin-top: -0.8rem;
            margin-bottom: 2rem;
        }

        [data-testid="stFileUploader"] {
            background-color: #282828;
            border: 1.5px solid #1DB954;
            border-radius: 12px;
            padding: 1.5rem;
        }

        [data-testid="stFileUploader"] label {
            color: #B3B3B3 !important;
        }

        .stButton > button {
            background-color: #1DB954;
            color: #000000;
            font-weight: 700;
            border: none;
            border-radius: 500px;
            padding: 0.5rem 2rem;
            font-size: 0.9rem;
            letter-spacing: 0.5px;
            transition: transform 0.1s ease, background-color 0.2s ease;
            width: 100%;
        }

        .stButton > button:hover {
            background-color: #1ed760;
            transform: scale(1.02);
            color: #000000;
        }

        .stTabs [data-baseweb="tab-list"] {
            background-color: #000000;
            border-bottom: 1px solid #282828;
            gap: 1rem;
        }

        .stTabs [data-baseweb="tab"] {
            color: #B3B3B3;
            font-weight: 600;
            font-size: 0.9rem;
            padding-bottom: 0.75rem;
        }

        .stTabs [aria-selected="true"] {
            color: #1DB954 !important;
            border-bottom: 2px solid #1DB954 !important;
        }

        [data-testid="stExpander"] {
            background-color: #282828;
            border: none;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        [data-testid="stExpander"] summary {
            color: #FFFFFF;
            font-weight: 600;
        }

        .stRadio label {
            color: #B3B3B3;
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #121212; }
        ::-webkit-scrollbar-thumb { background: #535353; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #1DB954; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Study Companion</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your notes or lecture slides and let AI do the studying prep for you.</p>', unsafe_allow_html=True)

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
                        st.image(os.path.join(os.getcwd(), "static", "right.jpg"))
                        score += 1
                    else:
                        st.error(f"Q{i+1}: Incorrect — {q['explanation']}")
                        st.image(os.path.join(os.getcwd(), "static", "wrong.jpg"))
                st.info(f"Your score: {score}/{len(st.session_state.questions)}")