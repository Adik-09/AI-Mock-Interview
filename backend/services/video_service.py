import cv2
import os
import math
import numpy as np

def analyze_video_behavior(video_path: str) -> dict:

    """
    PROFESSIONAL AI VIDEO INTERVIEW ANALYSIS

    Features:
    - Face Presence Detection
    - Eye Contact Detection
    - Multiple Person Detection
    - Head Movement Analysis
    - Motion Stability
    - Frame Centering
    - Behavioral Confidence
    - Engagement Analysis
    - Distraction Detection
    """

    if not os.path.exists(video_path):
        return {
            "error": "Video file not found"
        }

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0 or fps == 0:
        return {
            "error": "Invalid video file"
        }

    duration_sec = total_frames / fps

    # -----------------------------
    # LOAD MODELS
    # -----------------------------

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        'haarcascade_frontalface_default.xml'
    )

    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        'haarcascade_eye.xml'
    )

    # -----------------------------
    # METRICS
    # -----------------------------

    processed_frames = 0
    sampled_frames = 0

    face_detected_frames = 0
    eye_contact_frames = 0
    multiple_people_frames = 0
    centered_face_frames = 0
    distraction_frames = 0

    movement_scores = []

    previous_face_center = None

    # Process ~5 FPS
    frame_skip = max(1, int(fps / 5))

    # -----------------------------
    # PROCESS VIDEO
    # -----------------------------

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        if processed_frames % frame_skip != 0:
            processed_frames += 1
            continue

        processed_frames += 1
        sampled_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame_height, frame_width = gray.shape

        # -----------------------------
        # FACE DETECTION
        # -----------------------------

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

                # MULTIPLE PERSON DETECTION

        if len(faces) > 1:
            multiple_people_frames += 1

        if len(faces) > 0:

            face_detected_frames += 1

            # Use largest detected face
            largest_face = max(
                faces,
                key=lambda rect: rect[2] * rect[3]
            )

            x, y, w, h = largest_face

            # -----------------------------
            # FACE CENTER ANALYSIS
            # -----------------------------

            face_center_x = x + w / 2
            face_center_y = y + h / 2

            frame_center_x = frame_width / 2
            frame_center_y = frame_height / 2

            distance_from_center = math.sqrt(
                (face_center_x - frame_center_x) ** 2 +
                (face_center_y - frame_center_y) ** 2
            )

            normalized_distance = (
                distance_from_center /
                math.sqrt(frame_width**2 + frame_height**2)
            )

            if normalized_distance < 0.18:
                centered_face_frames += 1

            # -----------------------------
            # HEAD MOVEMENT ANALYSIS
            # -----------------------------

            if previous_face_center is not None:

                movement = math.sqrt(
                    (face_center_x - previous_face_center[0]) ** 2 +
                    (face_center_y - previous_face_center[1]) ** 2
                )

                movement_scores.append(movement)

            previous_face_center = (
                face_center_x,
                face_center_y
            )

            # -----------------------------
            # EYE CONTACT ANALYSIS
            # -----------------------------

            roi_gray = gray[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(
                roi_gray
            )

            if len(eyes) >= 2:
                eye_contact_frames += 1

            # -----------------------------
            # DISTRACTION DETECTION
            # -----------------------------

            face_area = w * h

            frame_area = frame_width * frame_height

            face_ratio = face_area / frame_area

            # Tiny face = too far away / distracted
            if face_ratio < 0.03:
                distraction_frames += 1

            # Extreme side movement
            if normalized_distance > 0.30:
                distraction_frames += 1

        else:
            distraction_frames += 1

    cap.release()

    # -----------------------------
    # SAFETY
    # -----------------------------

    if sampled_frames == 0:
        sampled_frames = 1

    # -----------------------------
    # METRIC CALCULATIONS
    # -----------------------------

    face_presence_ratio = (
        face_detected_frames /
        sampled_frames
    ) * 100

    eye_contact_ratio = (
        eye_contact_frames /
        sampled_frames
    ) * 100

    centered_face_ratio = (
        centered_face_frames /
        sampled_frames
    ) * 100

    multiple_people_ratio = (
        multiple_people_frames /
        sampled_frames
    ) * 100

    distraction_ratio = (
        distraction_frames /
        sampled_frames
    ) * 100

    # -----------------------------
    # MOVEMENT STABILITY
    # -----------------------------

    avg_movement = (
        np.mean(movement_scores)
        if movement_scores else 0
    )

    # Lower movement = more stable
    movement_stability = max(
        0,
        100 - (avg_movement * 2)
    )

    movement_stability = min(
        100,
        movement_stability
    )

    # -----------------------------
    # ENGAGEMENT SCORE
    # -----------------------------

    engagement_score = (
        (eye_contact_ratio * 0.4) +
        (centered_face_ratio * 0.3) +
        (face_presence_ratio * 0.3)
    )

    engagement_score = min(100, engagement_score)

    # -----------------------------
    # BEHAVIORAL CONFIDENCE
    # -----------------------------

    behavioral_confidence = (
        (face_presence_ratio * 0.25) +
        (eye_contact_ratio * 0.30) +
        (movement_stability * 0.20) +
        (centered_face_ratio * 0.15) -
        (multiple_people_ratio * 0.05) -
        (distraction_ratio * 0.05)
    )

    behavioral_confidence = max(
        0,
        min(100, behavioral_confidence)
    )

    # -----------------------------
    # FINAL AI BEHAVIOR SCORE
    # -----------------------------

    behavior_score = (
        behavioral_confidence * 0.5 +
        engagement_score * 0.3 +
        movement_stability * 0.2
    )

    behavior_score = max(
        0,
        min(100, behavior_score)
    )

    # -----------------------------
    # PERFORMANCE INSIGHTS
    # -----------------------------

    strengths = []
    weaknesses = []

    if eye_contact_ratio > 70:
        strengths.append(
            "Maintained strong eye contact"
        )

    if centered_face_ratio > 75:
        strengths.append(
            "Maintained professional camera framing"
        )

    if movement_stability > 75:
        strengths.append(
            "Displayed stable and composed posture"
        )

    if face_presence_ratio < 70:
        weaknesses.append(
            "Face visibility was inconsistent"
        )

    if distraction_ratio > 20:
        weaknesses.append(
            "Frequent distractions or movement detected"
        )

    if multiple_people_ratio > 5:
        weaknesses.append(
            "Multiple individuals appeared during interview"
        )

    if eye_contact_ratio < 50:
        weaknesses.append(
            "Limited eye contact detected"
        )

    # -----------------------------
    # RETURN FINAL AI ANALYTICS
    # -----------------------------

    return {

        "duration_sec": round(duration_sec, 1),

        "face_presence_ratio":
            round(face_presence_ratio, 1),

        "eye_contact_ratio":
            round(eye_contact_ratio, 1),

        "centered_face_ratio":
            round(centered_face_ratio, 1),

        "multiple_people_ratio":
            round(multiple_people_ratio, 1),

        "distraction_ratio":
            round(distraction_ratio, 1),

        "movement_stability":
            round(movement_stability, 1),

        "engagement_score":
            round(engagement_score, 1),

        "behavioral_confidence":
            round(behavioral_confidence, 1),

        "behavior_score":
            round(behavior_score, 1),

        "strengths":
            strengths,

        "weaknesses":
            weaknesses,

        "analysis_summary": {

            "camera_presence":
                "Excellent"
                if face_presence_ratio > 85 else
                "Good"
                if face_presence_ratio > 65 else
                "Needs Improvement",

            "eye_contact":
                "Strong"
                if eye_contact_ratio > 70 else
                "Average"
                if eye_contact_ratio > 50 else
                "Weak",

            "stability":
                "Stable"
                if movement_stability > 75 else
                "Moderate"
                if movement_stability > 50 else
                "Unstable",

            "engagement":
                "Highly Engaged"
                if engagement_score > 80 else
                "Moderately Engaged"
                if engagement_score > 60 else
                "Low Engagement"
        }
    }