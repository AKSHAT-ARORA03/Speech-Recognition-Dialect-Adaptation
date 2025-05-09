import streamlit as st
import os
from app.transcriber import transcribe_audio
from app.corrector import correct_transcript
from app.utils import compute_wer

st.set_page_config(page_title="Dialect Adaptive Speech Recognition")

st.title("🎙️ Speech Recognition + Dialect Adaptation")

uploaded_file = st.file_uploader("Upload an audio file (.mp3/.wav)", type=["wav", "mp3"])

if uploaded_file:
    # Save the uploaded file temporarily for processing
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.read())

    st.audio("temp_audio.wav", format="audio/wav")

    # Transcribe the audio using Whisper model
    st.write("🧠 Transcribing with Whisper...")
    raw_text = transcribe_audio("temp_audio.wav")
    st.subheader("📝 Raw Transcript:")
    st.text(raw_text)

    # Correct the grammar of the transcription
    st.write("🔧 Correcting grammar...")
    corrected_text = correct_transcript(raw_text)
    st.subheader("✅ Corrected Transcript:")
    st.text(corrected_text)

    # Optional: Calculate Word Error Rate (WER) if a reference is provided
    reference = st.text_input("Enter reference transcript (optional for WER evaluation):")
    if reference:
        error = compute_wer(reference, corrected_text)
        st.write(f"🧪 Word Error Rate (WER): {error:.2%}")
