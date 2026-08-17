import streamlit as st
import os

# Pillow (PIL) Version အသစ်များအတွက် Error ဖြေရှင်းချက်
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

# 1. Page Configuration & Custom CSS
st.set_page_config(page_title="Wave-News Video Editor", page_icon="📰", layout="centered")

matcha_css = """
<style>
    .stApp { background-color: #F1F8F1; }
    h1, h2, h3, p, label { color: #3A5A40 !important; font-family: 'Pyidaungsu', sans-serif; }
    .stButton>button { background-color: #588157; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #3A5A40; color: white; }
</style>
"""
st.markdown(matcha_css, unsafe_allow_html=True)

st.title("📰 Wave-News TikTok Video ဖန်တီးသောစနစ်")
st.markdown("သတင်း Banner များထည့်သွင်းကာ TikTok Size (9:16) ဖြင့် သတင်းဗီဒီယိုများကို အလိုအလျောက် ပေါင်းစပ်ဖန်တီးနိုင်ပါသည်။")

# 2. Input Section
uploaded_audio = st.file_uploader("🎵 သတင်းအသံဖိုင် ထည့်ရန် (Audio)", type=['mp3', 'wav'])
news_banner = st.file_uploader("📰 သတင်း Banner သို့မဟုတ် Logo ထည့်ရန် (နောက်ခံအလွတ် PNG ဖိုင် ဖြစ်ရမည်)", type=['png'])
uploaded_images = st.file_uploader("🖼️ ဓာတ်ပုံများ ထည့်ရန် (ပုံများစွာ ရွေးနိုင်သည်)", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
uploaded_videos = st.file_uploader("🎥 ဗီဒီယို ဖိုင်များ ထည့်ရန် (ဖိုင်များစွာ ရွေးနိုင်သည်)", type=['mp4', 'mov'], accept_multiple_files=True)

st.write("")
generate_btn = st.button("သတင်း Video ဖန်တီးပါ 🎬")

# 3. Video Processing Logic
if generate_btn:
    if uploaded_audio is not None:
        total_visuals = len(uploaded_images) + len(uploaded_videos)
        
        if total_visuals > 0:
            with st.spinner('Wave-News ဗီဒီယိုကို ဖန်တီးနေပါသည်... (ခေတ္တစောင့်ပေးပါ)'):
                try:
                    temp_files = []
                    audio_path = "temp_audio.mp3"
                    video_file = "wave_news_tiktok.mp4"
                    
                    with open(audio_path, "wb") as f:
                        f.write(uploaded_audio.getbuffer())
                    temp_files.append(audio_path)
                    
                    audio_clip = AudioFileClip(audio_path)
                    total_duration = audio_clip.duration
                    item_duration = total_duration / total_visuals
                    
                    TARGET_SIZE = (720, 1280) # TikTok 9:16 Size
                    visual_clips = []
                    
                    # ဓာတ်ပုံများကို Zoom Effect ဖြင့် ပြင်ဆင်ခြင်း
                    for idx, img_file in enumerate(uploaded_images):
                        temp_img = f"temp_img_{idx}.jpg"
                        with open(temp_img, "wb") as f:
                            f.write(img_file.getbuffer())
                        temp_files.append(temp_img)
                        
                        clip = ImageClip(temp_img).set_duration(item_duration)
                        w, h = clip.size
                        if w/h > 720/1280:
                            clip = clip.resize(height=1280)
                        else:
                            clip = clip.resize(width=720)
                        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=720, height=1280)
                        
                        zoomed_clip = clip.resize(lambda t: 1 + 0.05 * (t / item_duration))
                        final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=TARGET_SIZE).set_duration(item_duration)
                        visual_clips.append(final_clip)
                    
                    # Video များကို ပြင်ဆင်ခြင်း
                    for idx, vid_file in enumerate(uploaded_videos):
                        temp_vid = f"temp_vid_{idx}.mp4"
                        with open(temp_vid, "wb") as f:
                            f.write(vid_file.getbuffer())
                        temp_files.append(temp_vid)
                        
                        vid_clip = VideoFileClip(temp_vid)
                        if vid_clip.duration > item_duration:
                            vid_clip = vid_clip.subclip(0, item_duration)
                        else:
                            vid_clip = vid_clip.set_duration(item_duration)
                        
                        w, h = vid_clip.size
                        if w/h > 720/1280:
                            vid_clip = vid_clip.resize(height=1280)
                        else:
                            vid_clip = vid_clip.resize(width=720)
                        vid_clip = vid_clip.crop(x_center=vid_clip.w/2, y_center=vid_clip.h/2, width=720, height=1280)
                        
                        vid_clip = vid_clip.without_audio()
                        visual_clips.append(vid_clip)
                    
                    # အပိုင်းများအားလုံးကို ဆက်ခြင်း
                    final_visual = concatenate_videoclips(visual_clips, method="compose")
                    
                    # သတင်း Banner (Overlay) ထည့်သွင်းခြင်း
                    if news_banner is not None:
                        banner_path = "temp_banner.png"
                        with open(banner_path, "wb") as f:
                            f.write(news_banner.getbuffer())
                        temp_files.append(banner_path)
                        
                        # Banner ကို Video အလျား (720) နှင့် ညီအောင် ချိန်ညှိပြီး အောက်ခြေတွင် ထားခြင်း
                        banner_clip = ImageClip(banner_path).set_duration(final_visual.duration)
                        banner_clip = banner_clip.resize(width=720)
                        banner_clip = banner_clip.set_position(("center", "bottom"))
                        
                        # Video မျက်နှာပြင်ပေါ်တွင် Banner ကို ထပ်အုပ်ခြင်း
                        final_visual = CompositeVideoClip([final_visual, banner_clip])
                    
                    # အသံဖိုင် ပေါင်းထည့်ခြင်း
                    final_video = final_visual.set_audio(audio_clip)
                    
                    # Video ထုတ်ယူခြင်း
                    final_video.write_videofile(
                        video_file, 
                        fps=24, 
                        codec="libx264", 
                        audio_codec="aac",
                        preset="ultrafast"
                    )
                    
                    st.success("✅ သတင်း Video ဖန်တီးမှု အောင်မြင်ပါသည်။")
                    st.video(video_file)
                    
                    # Memory ရှင်းလင်းခြင်း
                    audio_clip.close()
                    final_video.close()
                    for f_path in temp_files:
                        if os.path.exists(f_path):
                            os.remove(f_path)
                            
                except Exception as e:
                    st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
        else:
            st.warning("⚠️ ကျေးဇူးပြု၍ Video တွင်ပြသမည့် ဓာတ်ပုံ (သို့) Video ဖိုင်များ ထည့်သွင်းပေးပါ။")
    else:
        st.warning("⚠️ ကျေးဇူးပြု၍ နောက်ခံအဖြစ် အသုံးပြုမည့် သတင်းအသံဖိုင်ကို အရင်ထည့်သွင်းပေးပါ။")
