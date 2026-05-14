from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import shutil
import os
import traceback

from services.whisper_service import generate_transcript
from services.nlp_service import (
    evaluate_technical_answer,
    analyze_communication
)
from services.video_service import analyze_video_behavior
from services.report_service import generate_pdf_report

app = FastAPI(
    title="AI Mock Interview API",
    version="2.0.0"
)

# -------------------------------------------------------
# CORS
# -------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# ROOT
# -------------------------------------------------------

@app.get("/")
def read_root():

    return {
        "status": "ok",
        "message": "AI Mock Interview AI Engine Running"
    }

# -------------------------------------------------------
# REPORT MODEL
# -------------------------------------------------------

class ReportData(BaseModel):

    domain: str
    question: str
    transcript: str

    technical_analysis: Dict[str, Any]
    audio_analysis: Dict[str, Any]
    video_analysis: Dict[str, Any]

    overall_score: float

# -------------------------------------------------------
# FILE CLEANUP
# -------------------------------------------------------

def cleanup_files(paths: list):

    for path in paths:

        if path and os.path.exists(path):

            try:
                os.remove(path)

            except Exception as e:
                print(f"Error removing {path}: {e}")

# -------------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------------

@app.get("/api/health")
def health_check():

    return {
        "status": "healthy",
        "services": {
            "nlp": "active",
            "video_analysis": "active",
            "speech_to_text": "active",
            "report_generation": "active"
        }
    }

# -------------------------------------------------------
# MAIN INTERVIEW EVALUATION
# -------------------------------------------------------

@app.post("/api/evaluate")
async def evaluate_interview(

    background_tasks: BackgroundTasks,

    video: UploadFile = File(...),

    domain: str = Form(...),

    question: str = Form(...)

):

    """
    PROFESSIONAL AI MOCK INTERVIEW PIPELINE

    PIPELINES:
    1. Video Behavioral Analysis
    2. Speech-to-Text
    3. Communication Intelligence
    4. Semantic NLP Evaluation
    5. AI Scoring Engine
    """

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    temp_dir = os.path.join(
        BASE_DIR,
        "temp_uploads"
    )

    os.makedirs(temp_dir, exist_ok=True)

    video_path = os.path.abspath(
        os.path.join(temp_dir, video.filename)
    )

    print(f"\n[INFO] Saving video to: {video_path}")

    # -------------------------------------------------------
    # SAVE VIDEO
    # -------------------------------------------------------

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    pdf_path = None

    try:

        # ===================================================
        # 1. VIDEO ANALYSIS
        # ===================================================

        print("\n[PIPELINE] Starting Video Analysis...")

        video_analysis = analyze_video_behavior(
            video_path
        )

        duration_sec = video_analysis.get(
            "duration_sec",
            60
        )

        print("[SUCCESS] Video Analysis Completed")

        # ===================================================
        # 2. SPEECH TO TEXT
        # ===================================================

        print("\n[PIPELINE] Starting Speech-to-Text...")

        transcript = generate_transcript(
            video_path
        )

        transcript = transcript.strip()

        print("[SUCCESS] Transcript Generated")
        print(f"\nTRANSCRIPT:\n{transcript}\n")

        # ===================================================
        # 3. COMMUNICATION ANALYSIS
        # ===================================================

        print("\n[PIPELINE] Starting Communication Analysis...")

        audio_analysis = analyze_communication(
            transcript,
            duration_sec
        )

        print("[SUCCESS] Communication Analysis Completed")

        # ===================================================
        # 4. NLP TECHNICAL ANALYSIS
        # ===================================================

        print("\n[PIPELINE] Starting NLP Semantic Analysis...")

        technical_analysis = evaluate_technical_answer(
            domain,
            question,
            transcript
        )

        print("[SUCCESS] NLP Analysis Completed")

        # ===================================================
        # 5. AI SCORING ENGINE
        # ===================================================

        print("\n[PIPELINE] Calculating AI Interview Score...")

        # ---------------------------------------------------
        # TECHNICAL INTELLIGENCE
        # ---------------------------------------------------

        technical_score = (
            technical_analysis.get("score", 0)
        )

        semantic_score = (
            technical_analysis.get(
                "semantic_similarity",
                0
            )
        )

        relevance_score = (
            technical_analysis.get(
                "topic_relevance",
                0
            )
        )

        # ---------------------------------------------------
        # COMMUNICATION INTELLIGENCE
        # ---------------------------------------------------

        fluency_score = (
            audio_analysis.get(
                "fluency_score",
                0
            )
        )

        vocabulary_score = (
            audio_analysis.get(
                "vocabulary_score",
                0
            )
        )

        grammar_score = (
            audio_analysis.get(
                "grammar_score",
                0
            )
        )

        confidence_score = (
            audio_analysis.get(
                "confidence_score",
                0
            )
        )

        # ---------------------------------------------------
        # VIDEO INTELLIGENCE
        # ---------------------------------------------------

        behavioral_score = (
            video_analysis.get(
                "behavior_score",
                0
            )
        )

        engagement_score = (
            video_analysis.get(
                "engagement_score",
                0
            )
        )

        movement_score = (
            video_analysis.get(
                "movement_stability",
                0
            )
        )

        # ===================================================
        # PROFESSIONAL WEIGHTED AI SCORING
        # ===================================================

        overall_score = (

            # TECHNICAL AI
            (technical_score * 0.30) +

            # SEMANTIC UNDERSTANDING
            (semantic_score * 0.15) +

            # TOPIC RELEVANCE
            (relevance_score * 0.10) +

            # COMMUNICATION
            (fluency_score * 0.10) +

            # GRAMMAR
            (grammar_score * 0.05) +

            # VOCABULARY
            (vocabulary_score * 0.05) +

            # CONFIDENCE
            (confidence_score * 0.10) +

            # BEHAVIOR
            (behavioral_score * 0.10) +

            # ENGAGEMENT
            (engagement_score * 0.03) +

            # STABILITY
            (movement_score * 0.02)
        )

        overall_score = round(
            min(100, max(0, overall_score)),
            1
        )

        print(
            f"[SUCCESS] FINAL AI SCORE: {overall_score}"
        )

        # ===================================================
        # AI PERFORMANCE SUMMARY
        # ===================================================

        performance_summary = {

            "technical_performance":
                "Excellent"
                if technical_score >= 80 else
                "Good"
                if technical_score >= 60 else
                "Needs Improvement",

            "communication_quality":
                audio_analysis.get(
                    "communication_quality",
                    "Average"
                ),

            "behavioral_analysis":
                video_analysis.get(
                    "analysis_summary",
                    {}
                ),

            "overall_rating":
                "Outstanding"
                if overall_score >= 85 else
                "Strong"
                if overall_score >= 70 else
                "Average"
                if overall_score >= 55 else
                "Needs Improvement"
        }

        # ===================================================
        # FINAL RESPONSE
        # ===================================================

        results = {

            "domain": domain,

            "question": question,

            "transcript": transcript,

            "technical_analysis":
                technical_analysis,

            "audio_analysis":
                audio_analysis,

            "video_analysis":
                video_analysis,

            "performance_summary":
                performance_summary,

            "overall_score":
                overall_score
        }

        print("\n[INFO] AI Evaluation Completed Successfully\n")

        # background_tasks.add_task(
        #     cleanup_files,
        #     [video_path]
        # )

        return results

    # =======================================================
    # ERROR HANDLING
    # =======================================================

    except Exception as e:

        error_msg = str(e)

        traceback.print_exc()

        if (
            "ffprobe" in error_msg or
            "ffmpeg" in error_msg or
            "[WinError 2]" in error_msg
        ):

            error_msg = (
                "FFmpeg not found. "
                "Please install FFmpeg and "
                "add it to your PATH."
            )

        print(f"\n[ERROR] {error_msg}\n")

        return {
            "status": "error",
            "message": error_msg
        }

# -------------------------------------------------------
# PDF REPORT GENERATION
# -------------------------------------------------------

@app.post("/api/download_report")
async def download_report(

    data: ReportData,

    background_tasks: BackgroundTasks

):

    pdf_path = None

    try:

        print("\n[PIPELINE] Generating PDF Report...")

        pdf_path = generate_pdf_report(
            data.dict()
        )

        print("[SUCCESS] PDF Generated")

        # background_tasks.add_task(
        #     cleanup_files,
        #     [pdf_path]
        # )

        return FileResponse(

            path=pdf_path,

            media_type="application/pdf",

            filename=(
                f"AI_Mock_Interview_Report_"
                f"{data.domain}.pdf"
            )
        )

    except Exception as e:

        cleanup_files([pdf_path])

        print(f"\n[ERROR] PDF Generation Failed: {e}\n")

        return {
            "status": "error",
            "message": str(e)
        }

# -------------------------------------------------------
# START SERVER
# -------------------------------------------------------

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )