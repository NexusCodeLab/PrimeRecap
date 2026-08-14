import streamlit as st

# Premium Navy Blue & Grey Theme Setup
st.set_page_config(page_title="PrimeRecap Studio", layout="wide", page_icon="🎬")

st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC; /* Light Grey Background */
    }
    h1, h2, h3, p, label {
        color: #0F172A; /* Navy Blue Text */
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button {
        background-color: #1E3A8A; /* Premium Navy Blue */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 PrimeRecap Studio")
st.markdown("Transform your long source videos into professional recap shorts instantly.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("၁။ မူရင်း Video တင်ရန်")
    uploaded_video = st.file_uploader("Choose a video file (MP4)", type=['mp4'])

    st.subheader("၂။ Video ကြာချိန် ရွေးရန်")
    duration = st.radio("Select Duration:", ["၁ မိနစ် (60s)", "၁ မိနစ်ခွဲ (90s)", "၂ မိနစ် (120s)"])

with col2:
    st.subheader("၃။ ဇာတ်လမ်းအကျဉ်း Script")
    script_text = st.text_area("Recap Script စာသားများကို ဤနေရာတွင် ထည့်ပါ...", height=250)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("၄။ Recap ထုတ်လုပ်ရန်")
    if st.button("Generate Recap Video 🚀"):
        if uploaded_video and script_text:
            st.info(f"စနစ်မှ {duration} စာ Recap ဗီဒီယိုကို စတင်ဖန်တီးနေပါပြီ... (Processing)")
            # (နောက်ပိုင်းတွင် ဤနေရာ၌ AI Processing Code များ ထပ်ထည့်ပါမည်)
        else:
            st.warning("ကျေးဇူးပြု၍ Video နှင့် Script စာသားကို အရင်ထည့်ပါ။")
