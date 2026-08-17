import streamlit as st
import os
import uuid # ဖိုင်နာမည် အသစ်အမြဲပေးရန်

from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips, CompositeVideoClip
import moviepy.video.fx.all as vfx

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

st.title("📰 သတင်း Video တည်းဖြတ်သောစနစ် (No Audio)")
st.error("ယခုစနစ်သည် အသံ (Audio) ကို လုံးဝ ထည့်သွင်းပေးမည်မဟုတ်ပါ။ TikTok Size (9:16) ဖြင့်သာ ထုတ်ပေးပါမည်။")

news_banner = st.file_uploader("📰 သတင်း Banner ထည့်ရန် (နောက်ခံအလွတ် PNG ဖိုင်)", type=['png'])
uploaded_images = st.file_uploader("🖼️ ဓာတ်ပုံများ ထည့်ရန် (Zoom Effect ဖြင့် ၅ စက္ကန့်စီ ပြသပါမည်)", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
uploaded_videos = st.file_uploader("🎥 ဗီဒီယို ဖိုင်များ ထည့်ရန် (TikTok Size သို့ အလိုအလျောက် ဖြတ်တောက်ပါမည်)", type=['mp4', 'mov'], accept_multiple_files=True)

st.write("")
generate_btn = st.button("Video ဖန်တီးပါ 🎬")

def make_tiktok_size(clip):
    w, h = clip.size
    target_ratio = 720 / 1280
    clip_ratio = w / h
    
    if clip_ratio > target_ratio:
        clip = clip.resize(height=1280)
    else:
        clip = clip.resize(width=720)
    
    return clip.fx(vfx.crop, x_center=clip.w/2, y_center=clip.h/2, width=720, height=1280)

if generate_btn:
    total_visuals = len(uploaded_images) + len(uploaded_videos)
    
    if total_visuals > 0:
        with st.spinner('ဗီဒီယိုကို ဖန်တီးနေပါသည်...'):
            try:
                temp_files = []
                
                # ဖြေရှင်းချက် (၁) - Browser က အဟောင်းကို မပြနိုင်အောင် နာမည်ကို အမြဲအသစ်ပေးခြင်း
                unique_id = uuid.uuid4().hex[:8]
                video_file = f"wave_news_{unique_id}.mp4"
                
                TARGET_SIZE = (720, 1280)
                visual_clips = []
                
                for idx, img_file in enumerate(uploaded_images):
                    temp_img = f"temp_img_{unique_id}_{idx}.jpg"
                    with open(temp_img, "wb") as f:
                        f.write(img_file.getbuffer())
                    temp_files.append(temp_img)
                    
                    clip = ImageClip(temp_img).set_duration(5.0)
                    clip = make_tiktok_size(clip)
                    zoomed_clip = clip.resize(lambda t: 1 + 0.10 * (t / 5.0))
                    final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=TARGET_SIZE).set_duration(5.0)
                    visual_clips.append(final_clip)
                
                for idx, vid_file in enumerate(uploaded_videos):
                    temp_vid = f"temp_vid_{unique_id}_{idx}.mp4"
                    with open(temp_vid, "wb") as f:
                        f.write(vid_file.getbuffer())
                    temp_files.append(temp_vid)
                    
                    vid_clip = VideoFileClip(temp_vid)
                    vid_clip = make_tiktok_size(vid_clip)
                    visual_clips.append(vid_clip)
                
                final_visual = concatenate_videoclips(visual_clips, method="compose")
                
                if news_banner is not None:
                    banner_path = f"temp_banner_{unique_id}.png"
                    with open(banner_path, "wb") as f:
                        f.write(news_banner.getbuffer())
                    temp_files.append(banner_path)
                    
                    banner_clip = ImageClip(banner_path).set_duration(final_visual.duration)
                    banner_clip = banner_clip.resize(width=720)
                    banner_clip = banner_clip.set_position(("center", "bottom"))
                    
                    final_visual = CompositeVideoClip([final_visual, banner_clip])
                
                # ဖြေရှင်းချက် (၂) - အသံ လုံးဝမပါလာစေရန် audio=False ထည့်သွင်းခြင်း
                final_visual.write_videofile(
                    video_file, 
                    fps=24, 
                    codec="libx264", 
                    preset="ultrafast",
                    audio=False 
                )
                
                st.success("✅ သတင်း Video အသစ် ဖန်တီးမှု အောင်မြင်ပါသည်။ (အသံ လုံးဝမပါပါ)")
                st.video(video_file)
                
                final_visual.close()
                for f_path in temp_files:
                    if os.path.exists(f_path):
                        os.remove(f_path)
                        
            except Exception as e:
                st.error(f"Error ဖြစ်ပေါ်နေပါသည်: {e}")
    else:
        st.warning("⚠️ ဓာတ်ပုံ (သို့) Video ဖိုင်များ အနည်းဆုံးတစ်ခု ထည့်သွင်းပေးပါ။")
