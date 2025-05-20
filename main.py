import os
from pathlib import Path
import streamlit as st
from yt_dlp import YoutubeDL

st.set_page_config(page_title="YouTube Audio Downloader")
st.title("YouTube Audio Downloader")
st.markdown("Paste YouTube video link below and download audio ")

url = st.text_input("YouTube Video URL")
quality = st.selectbox("Choose Audio Quality", ["High", "Low"])
download_btn = st.button("Start Download")

def download_audio_no_ffmpeg(link, quality_choice):
    output_folder = Path("downloads")
    output_folder.mkdir(exist_ok=True)

    # Choose best or worst audio format
    fmt = "bestaudio" if quality_choice == "High" else "worstaudio"

    outtmpl = str(output_folder / "%(title).70s.%(ext)s")

    ydl_opts = {
        'format': fmt,
        'outtmpl': outtmpl,
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        # No postprocessors - no FFmpeg
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        downloaded = ydl.prepare_filename(info)
        return downloaded

if download_btn and url:
    try:
        with st.spinner("Downloading audio"):
            file_path = download_audio_no_ffmpeg(url, quality)
        st.success("Download ready!")

        with open(file_path, "rb") as audio_file:
            st.download_button(
                label="Click to Save Audio",
                data=audio_file,
                file_name=os.path.basename(file_path),
                mime="audio/*"  # generic audio mime-type
            )
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
