import streamlit as st
import os

# Pillow (PIL) Error ဖြေရှင်းရန်
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips, CompositeVideoClip
import moviepy.video.fx.all as vfx

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

st.title("📰 သတင်း Video တည်းဖြတ်သောစနစ် (TikTok Size)")
st.markdown("ဓာတ်ပုံများနှင့် ဗီဒီယိုများကို TikTok Size (720x1280) အတိအကျဖြင့် Zoom Effect များပါဝင်သော သတင်းဗီဒီယိုအဖြစ် ပေါင်းစပ်ပေးပါမည်။")

# 2. Input Section
news_banner = st.file_uploader("📰 သတင်း Banner ထည့်ရန် (နောက်ခံအလွတ် PNG ဖိုင်)", type=['png'])
uploaded_images = st.file_uploader("🖼️ ဓာတ်ပုံများ ထည့်ရန် (Zoom Effect ဖြင့် ၅ စက္ကန့်စီ ပြသပါမည်)", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
uploaded_videos = st.file_uploader("🎥 ဗီဒီယို ဖိုင်များ ထည့်ရန် (TikTok Size သို့ အလိုအလျောက် ဖြတ်တောက်ပါမည်)", type=['mp4', 'mov'], accept_multiple_files=True)

st.write("")
generate_btn = st.button("Video ဖန်တီးပါ 🎬")

# TikTok Size (720x1280) အတိအကျ ဖြတ်တောက်ပေးသော Function
def make_tiktok_size(clip):
    w, h = clip.size
    target_ratio = 720 / 1280
    clip_ratio = w / h
    
    if clip_ratio > target_ratio:
        clip = clip.resize(height=1280)
    else:
        clip = clip.resize(width=720)
    
    return clip.fx(vfx.crop, x_center=clip.w/2, y_center=clip.h/2, width=720, height=1280)

# 3. Processing Logic
if generate_btn:
    total_visuals = len(uploaded_images) + len(uploaded_videos)
    
    if total_visuals > 0:
        # Streamlit Cache အဟောင်းများကို ရှင်းလင်းရန်
        st.cache_data.clear() 
        
        with st.spinner('Zoom Effect များထည့်သွင်းကာ ဗီဒီယိုကို ဖန်တီးနေပါသည်... (ခေတ္တစောင့်ပေးပါ)'):
            try:
                temp_files = []
                video_file = "wave_news_tiktok_final.mp4"
                TARGET_SIZE = (720, 1280)
                visual_clips = []
                
                # ဓာတ်ပုံများကို Zoom Effect ၁၀% ဖြင့် ပြင်ဆင်ခြင်း
                for idx, img_file in enumerate(uploaded_images):
                    temp_img = f"temp_img_{idx}.jpg"
                    with open(temp_img, "wb") as f:
                        f.write(img_file.getbuffer())
                    temp_files.append(temp_img)
                    
                    clip = ImageClip(temp_img).set_duration(5.0)
                    clip = make_tiktok_size(clip)
                    
                    # Zoom In (၁၀% ပိုကြီးလာစေရန် ပြင်ဆင်ထားသည်)
                    zoomed_clip = clip.resize(lambda t: 1 + 0.10 * (t / 5.0))
                    final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=TARGET_SIZE).set_duration(5.0)
                    visual_clips.append(final_clip)
                
                # Video များကို TikTok Size အတိအကျ ဖြတ်တောက်ခြင်း
                for idx, vid_file in enumerate(uploaded_videos):
                    temp_vid = f"temp_vid_{idx}.mp4"
                    with open(temp_vid, "wb") as f:
                        f.write(vid_file.getbuffer())
                    temp_files.append(temp_vid)
                    
                    vid_clip = VideoFileClip(temp_vid)
                    vid_clip = make_tiktok_size(vid_clip)
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
                    
                    banner_clip = ImageClip(banner_path).set_duration(final_visual.duration)
                    banner_clip = banner_clip.resize(width=720)
                    banner_clip = banner_clip.set_position(("center", "bottom"))
                    
                    final_visual = CompositeVideoClip([final_visual, banner_clip])
                
                # Video ထုတ်ယူခြင်း
                final_visual.write_videofile(
                    video_file, 
                    fps=24, 
                    codec="libx264", 
                    preset="ultrafast"
                )
                
                st.success("✅ သတင်း Video အသစ် ဖန်တီးမှု အောင်မြင်ပါသည်။")
                st.video(video_file)
                
                # Memory ရှင်းလင်းခြင်း
                final_visual.close()
                for f_path in temp_files:
                    if os.path.exists(f_path):
                        os.remove(f_path)
                        
            except Exception as e:
                st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
    else:
        st.warning("⚠️ ကျေးဇူးပြု၍ ဓာတ်ပုံ (သို့) Video ဖိုင်များ အနည်းဆုံးတစ်ခု ထည့်သွင်းပေးပါ။")
