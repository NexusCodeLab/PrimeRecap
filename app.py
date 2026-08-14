import streamlit as st
import time

# Premium Navy Blue & Grey Theme Setup
st.set_page_config(page_title="PrimeRecap Studio", layout="wide", page_icon="🎬")

st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC; 
    }
    h1, h2, h3, p, label {
        color: #0F172A; 
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
        background-color: #1E3A8A; 
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
    }
    .voice-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 PrimeRecap Studio")
st.markdown("Transform your text into realistic voices and generate professional recap shorts.")
st.markdown("---")

# Voice and Language Selection (Inspired by the Crikk UI)
st.markdown('<div class="voice-box">', unsafe_allow_html=True)
v_col1, v_col2 = st.columns(2)
with v_col1:
    st.selectbox("Language", ["Burmese"], disabled=True)
with v_col2:
    voice = st.selectbox("Voice", ["Nilar (Female)", "Thiha (Male)"])
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Source Video")
    uploaded_video = st.file_uploader("Choose a video file (MP4)", type=['mp4'])

    st.subheader("2. Select Duration")
    duration = st.radio("Recap Length:", ["60 Seconds", "90 Seconds", "120 Seconds"])

with col2:
    st.subheader("3. Recap Script")
    script_text = st.text_area("Type or paste your text here...", height=200, placeholder="Enter your recap script in Burmese...")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("4. Generate Output")
    
    if st.button("Generate Recap Video 🚀"):
        if uploaded_video and script_text:
            selected_voice = "Nilar's" if "Nilar" in voice else "Thiha's"
            
            with st.spinner(f"Generating your {duration} recap with {selected_voice} voice..."):
                # Backend processing simulation
                time.sleep(5) 
                st.success("✅ Video generation completed successfully!")
                st.info("💡 Note: Full video processing requires premium cloud hosting.")
        else:
            st.warning("Please upload a video and enter your script first.")
