import streamlit as st
import asyncio
import edge_tts
import tempfile
import os
import time

# Premium Navy Blue & Grey Theme Setup
st.set_page_config(page_title="PrimeRecap Studio", layout="wide", page_icon="🎬")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3, p, label { color: #0F172A; font-family: 'Montserrat', sans-serif; }
    .stButton>button {
        background-color: #1E3A8A; color: white; border-radius: 8px;
        border: none; padding: 10px 24px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-color: #3B82F6; color: white; }
    .voice-box {
        background-color: white; padding: 20px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 PrimeRecap Studio")
st.markdown("Transform your text into realistic voices and generate professional recap shorts.")
st.markdown("---")

# Voice and Language Selection
st.markdown('<div class="voice-box">', unsafe_allow_html=True)
v_col1, v_col2 = st.columns(2)
with v_col1:
    st.selectbox("Language", ["Burmese"], disabled=True)
with v_col2:
    voice_choice = st.selectbox("Voice", ["Nilar (Female)", "Thiha (Male)"])
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
    
    if st.button("Generate Audio 🚀"):
        if script_text.strip():
            # Edge-TTS အတွက် အသံရွေးချယ်ခြင်း
            voice_name = "my-MM-NilarNeural" if "Nilar" in voice_choice else "my-MM-ThihaNeural"
            
            with st.spinner(f"Generating audio with {voice_choice.split()[0]}'s voice..."):
                try:
                    # Async function ဖြင့် အသံဖန်တီးခြင်း
                    async def generate_audio(text, voice, output_file):
                        communicate = edge_tts.Communicate(text, voice)
                        await communicate.save(output_file)

                    # ယာယီ MP3 ဖိုင်တည်ဆောက်ခြင်း
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    temp_filepath = temp_file.name
                    temp_file.close()

                    # အသံပြောင်းလဲခြင်း လုပ်ငန်းစဉ် စတင်ခြင်း
                    asyncio.run(generate_audio(script_text, voice_name, temp_filepath))
                    
                    st.success("✅ Audio generated successfully!")
                    
                    # ဖန်တီးပြီးသော အသံကို ဖွင့်ပြခြင်း
                    st.audio(temp_filepath, format="audio/mp3")
                    
                    # Download လုပ်ရန် ခလုတ်ဖန်တီးခြင်း
                    with open(temp_filepath, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Audio (MP3)",
                            data=file,
                            file_name="recap_audio.mp3",
                            mime="audio/mp3"
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter your script first to generate audio.")
