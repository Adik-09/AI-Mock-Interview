import os
os.environ["PATH"] += os.pathsep + r"C:\Users\adity\Downloads\ffmpeg-2026-05-11-git-17bc88e67f-essentials_build\ffmpeg-2026-05-11-git-17bc88e67f-essentials_build\bin"

import whisper
# Load the 'small' model - balanced for speed and accuracy
model = whisper.load_model("small")

def generate_transcript(audio_file_path: str) -> str:
    """
    Generates a transcript using the small model with a prompt to prime for accents and technical terms.
    """ 
    try:
        # Use a literal prompt to prevent hallucinations and content addition
        result = model.transcribe(
            audio_file_path, 
            initial_prompt="Transcribe the speech exactly as spoken, including technical terms like Python, DBMS, Machine Learning. No summarization."
        )
        return result["text"].strip()
    except Exception as e: 
        error_msg = str(e)
        if "ffprobe" in error_msg or "ffmpeg" in error_msg or "[WinError 2]" in error_msg:
            error_msg = "FFmpeg not found in PATH. You MUST completely close this terminal and open a new one after installing FFmpeg."
        print(f"Whisper transcription failed: {error_msg}", flush=True)
        raise Exception(error_msg)
