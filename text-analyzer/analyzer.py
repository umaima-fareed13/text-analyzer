import streamlit as st

# Custom CSS to style text inputs, text area, and placeholder text
st.markdown("""
    <style>
    /* Change placeholder text color */
    ::placeholder {
        color: black !important;
        opacity: 1 !important; /* Ensure visibility */
    }

    /* Style for input fields */
    .stTextInput input, .stTextArea textarea {
        color: white !important; /* Entered text color */
        background-color: rgba(0, 0, 0, 0.3) !important; /* Slightly transparent dark background */
        border: 2px solid #007BFF !important;
        border-radius: 5px;
        padding: 10px;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #007BFF;
        color: white;
        font-size: 16px;
        padding: 8px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "text" not in st.session_state:
    st.session_state.text = ""

if "results" not in st.session_state:
    st.session_state.results = {}

if "search_word" not in st.session_state:
    st.session_state.search_word = ""

if "replace_word" not in st.session_state:
    st.session_state.replace_word = ""

# Function to analyze text
def analyze_text(text):
    words = text.split()
    word_count = len(words)
    char_count = len(text)

    # Count vowels
    vowels = "aeiouAEIOU"
    vowel_count = sum(1 for char in text if char in vowels)

    # Convert text to uppercase & lowercase
    uppercase_text = text.upper()
    lowercase_text = text.lower()

    # Check if "Python" is in the text
    contains_python = "Python" in text

    # Calculate average word length
    avg_word_length = char_count / word_count if word_count > 0 else 0

    return {
        "word_count": word_count,
        "char_count": char_count,
        "vowel_count": vowel_count,
        "uppercase_text": uppercase_text,
        "lowercase_text": lowercase_text,
        "contains_python": contains_python,
        "avg_word_length": avg_word_length
    }

# Streamlit UI
st.markdown('<h1>📖 Text Analyzer</h1>', unsafe_allow_html=True)

# User Input
st.session_state.text = st.text_area("📝 Enter a paragraph:", st.session_state.text, placeholder="Type here...")

# Button to trigger analysis
if st.button("Analyze Text"):
    if st.session_state.text.strip():  # Ensure input is not empty
        st.session_state.results = analyze_text(st.session_state.text)
    else:
        st.warning("⚠️ Please enter a paragraph before analyzing.")

# Display results if available
if st.session_state.results:
    results = st.session_state.results

    st.markdown(f"<h2>🔍 Text Analysis Results</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='highlight'>📝 <b>Total Words:</b> {results['word_count']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='highlight'>🔢 <b>Total Characters (including spaces):</b> {results['char_count']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='highlight'>🔡 <b>Vowel Count:</b> {results['vowel_count']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='highlight'>🐍 <b>Contains 'Python':</b> {'✅ Yes' if results['contains_python'] else '❌ No'}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='highlight'>📊 <b>Average Word Length:</b> {results['avg_word_length']:.2f}</p>", unsafe_allow_html=True)

    st.markdown(f"<h2>🔠 Uppercase & Lowercase Conversion</h2>", unsafe_allow_html=True)
    st.code(results['uppercase_text'], language="text")
    st.code(results['lowercase_text'], language="text")

    # Search & Replace Feature
    st.markdown("<h2>🔄 Search & Replace</h2>", unsafe_allow_html=True)

    # Preserve input fields using session state
    st.session_state.search_word = st.text_input("🔍 Enter a word to search for:", st.session_state.search_word)
    st.session_state.replace_word = st.text_input("✏️ Enter a word to replace it with:", st.session_state.replace_word)

    if st.button("Replace Word"):
        if st.session_state.search_word in st.session_state.text:
            st.session_state.text = st.session_state.text.replace(st.session_state.search_word, st.session_state.replace_word)
            st.success("✅ Modified Text:")
            st.code(st.session_state.text, language="text")
        else:
            st.warning("⚠️ Word not found in the text!")
