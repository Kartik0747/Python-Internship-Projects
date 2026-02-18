import streamlit as st
from transformers import pipeline

# Load the sentiment analysis model (using caching for performance)
@st.cache_resource
def load_model():
    # This will use a pre-trained model to analyze text
    return pipeline("sentiment-analysis")

analyzer = load_model()

# --- Page Setup ---
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="🤖")
st.title("🤖 AI-Based Sentiment Analyzer")
st.markdown("Enter any text below to see if the sentiment is **Positive** or **Negative**.")

# --- User Input ---
user_input = st.text_area(
    "Enter text/review here:", 
    "I am really enjoying this Python internship!"
)

# --- Logic ---
if st.button("Analyze Now"):
    if user_input.strip() != "":
        with st.spinner('AI is processing...'):
            # Running the NLP model
            result = analyzer(user_input)
            label = result[0]['label']
            score = result[0]['score']

        # --- Display Results ---
        st.divider()
        if label == "POSITIVE":
            st.success(f"### Sentiment: {label}")
        else:
            st.error(f"### Sentiment: {label}")
            
        st.write(f"**Confidence Level:** {score:.2f}")
    else:
        st.warning("Please enter some text first.")

# Footer with your professional details
st.sidebar.markdown("---")
st.sidebar.write("Developed by: Kartik Nanasaheb Gaikwad")