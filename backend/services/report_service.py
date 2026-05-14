from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import uuid

def generate_pdf_report(results: dict) -> str:
    """
    Generates a PDF report and returns the absolute file path.
    """
    reports_dir = "temp_reports"
    os.makedirs(reports_dir, exist_ok=True)
    filename = f"report_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []
    
    # Title
    Story.append(Paragraph("AI Mock Interview Assessment Report", styles['Title']))
    Story.append(Spacer(1, 12))
    
    # Overview
    Story.append(Paragraph(f"<b>Domain:</b> {str(results.get('domain', '')).upper()}", styles['Normal']))
    Story.append(Paragraph(f"<b>Question:</b> {results.get('question', '')}", styles['Normal']))
    Story.append(Paragraph(f"<b>Overall Score:</b> {results.get('overall_score', 0)} / 10", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    # Technical Analysis
    tech = results.get("technical_analysis", {})
    Story.append(Paragraph("Technical Analysis", styles['Heading3']))
    Story.append(Paragraph(f"Score: {tech.get('score', 0)} / 10", styles['Normal']))
    Story.append(Paragraph(f"Feedback: {tech.get('feedback', '')}", styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Communication Analysis
    comm = results.get("audio_analysis", {})
    Story.append(Paragraph("Communication Analysis", styles['Heading3']))
    Story.append(Paragraph(f"Fluency Score: {comm.get('fluency_score', 0)} / 10", styles['Normal']))
    Story.append(Paragraph(f"Words Per Minute: {comm.get('wpm', 0)}", styles['Normal']))
    Story.append(Paragraph(f"Filler Words Used: {comm.get('filler_count', 0)}", styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Video Analysis
    vid = results.get("video_analysis", {})
    Story.append(Paragraph("Visual Behavioral Analysis", styles['Heading3']))
    Story.append(Paragraph(f"Behavior Score: {vid.get('behavior_score', 0)} / 10", styles['Normal']))
    Story.append(Paragraph(f"Face Presence Ratio: {vid.get('face_presence_ratio', 0)}%", styles['Normal']))
    Story.append(Paragraph(f"Eye Contact Ratio: {vid.get('eye_contact_ratio', 0)}%", styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Strengths and Weaknesses
    strengths = []
    weaknesses = []
    
    if tech.get('score', 0) >= 7: strengths.append("Strong technical knowledge and accuracy.")
    else: weaknesses.append("Needs improvement in technical correctness of the answer.")
        
    if comm.get('fluency_score', 0) >= 8: strengths.append("Excellent fluency and communication pacing.")
    else: weaknesses.append("Consider reducing filler words to sound more confident.")
        
    if vid.get('behavior_score', 0) >= 7: strengths.append("Good camera presence and eye contact.")
    else: weaknesses.append("Try to maintain better eye contact with the camera.")
    
    Story.append(Paragraph("Strengths", styles['Heading3']))
    for s in strengths:
        Story.append(Paragraph(f"- {s}", styles['Normal']))
    Story.append(Spacer(1, 12))
        
    Story.append(Paragraph("Areas for Improvement", styles['Heading3']))
    for w in weaknesses:
        Story.append(Paragraph(f"- {w}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Transcript
    Story.append(Paragraph("Full Transcript", styles['Heading3']))
    Story.append(Paragraph(f"{results.get('transcript', 'No transcript generated.')}", styles['Normal']))
        
    doc.build(Story)
    return filepath
