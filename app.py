import streamlit as st
import asyncio
import edge_tts
import tempfile
import os
from moviepy.editor import VideoFileClip, AudioFileClip

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
st.markdown("Transform your text into realistic voices and auto-trim your video to match audio length.")
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

with col2:
    st.subheader("2. Recap Script")
    script_text = st.text_area("Type or paste your text here...", height=200, placeholder="Enter your recap script in Burmese...")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("3. Generate Output")
    
    if st.button("Generate Sync Video 🚀"):
        if script_text.strip() and uploaded_video:
            
            voice_name = "my-MM-NilarNeural" if "Nilar" in voice_choice else "my-MM-ThihaNeural"
            
            with st.spinner("Processing Audio & Trimming Video..."):
                try:
                    # ၁။ အသံဖန်တီးခြင်း
                    async def generate_audio(text, voice, output_file):
                        communicate = edge_tts.Communicate(text, voice)
                        await communicate.save(output_file)

                    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    audio_path = temp_audio.name
                    temp_audio.close()
                    
                    asyncio.run(generate_audio(script_text, voice_name, audio_path))
                    audio_clip = AudioFileClip(audio_path)
                    target_duration = audio_clip.duration # အသံကြာချိန်ကို အတိအကျ ယူပါမည်
                    
                    # ၂။ ဗီဒီယို ဖိုင်ကို ယာယီသိမ်းဆည်းခြင်း
                    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                    temp_video.write(uploaded_video.read())
                    video_path = temp_video.name
                    temp_video.close()
                    
                    # ၃။ Video ကို ခေါ်ယူပြီး အသံကြာချိန်အတိုင်း ဖြတ်တောက်ခြင်း (Auto-trim)
                    video_clip = VideoFileClip(video_path)
                    final_duration = min(target_duration, video_clip.duration)
                    video_clip = video_clip.subclip(0, final_duration)
                    
                    # ၄။ ဗီဒီယိုထဲသို့ အသံအသစ် ထည့်သွင်းခြင်း
                    final_clip = video_clip.set_audio(audio_clip.subclip(0, final_duration))
                    
                    # ၅။ ဖိုင်အသစ်အဖြစ် ထုတ်ယူခြင်း
                    output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                    final_clip.write_videofile(
                        output_video_path, 
                        codec="libx264", 
                        audio_codec="aac", 
                        preset="ultrafast", 
                        logger=None
                    )
                    
                    st.success("✅ Video correctly synced to audio duration!")
                    
                    # ထွက်လာသော ဗီဒီယိုအား ပြသခြင်းနှင့် Download
                    st.video(output_video_path)
                    
                    with open(output_video_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Synced Video (MP4)",
                            data=file,
                            file_name="synced_recap.mp4",
                            mime="video/mp4"
                        )
                        
                except Exception as e:
                    st.error(f"Error Occurred: {e}. (Free server များတွင် ဖိုင်ဆိုဒ်ကြီးပါက Error ပြနိုင်ပါသည်။)")
                    
        else:
            st.warning("Please upload a video and enter your script first.")
