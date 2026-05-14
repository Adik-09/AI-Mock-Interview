import json
import os
import re
from collections import Counter

import nltk
import textstat
import spacy
from textblob import TextBlob

from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from keybert import KeyBERT

# Download requirements
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Load Models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')
kw_model = KeyBERT(model)

# Grammar checker (Java-free)
HAS_GRAMMAR_TOOL = True 

# Load golden answers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'golden_answers.json')

with open(DATA_FILE, 'r') as f:
    GOLDEN_ANSWERS = json.load(f)

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text, top_n=10):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_n
    )
    return [kw[0].lower() for kw in keywords]

def semantic_similarity(text1, text2):
    embeddings = model.encode([text1, text2])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(score)

def detect_irrelevant_sentences(transcript, golden_answer):
    sentences = sent_tokenize(transcript)
    irrelevant = []
    relevant_scores = []
    for sentence in sentences:
        score = semantic_similarity(sentence, golden_answer)
        relevant_scores.append(score)
        if score < 0.30:
            irrelevant.append(sentence)
    avg_relevance = sum(relevant_scores) / len(relevant_scores) if relevant_scores else 0
    return irrelevant, avg_relevance

def calculate_vocabulary_metrics(words):
    unique_words = len(set(words))
    total_words = len(words)
    lexical_diversity = (unique_words / total_words if total_words > 0 else 0)
    return round(lexical_diversity * 100, 2)

def detect_confidence_language(transcript):
    transcript = transcript.lower()
    confident_phrases = ["definitely", "clearly", "ensures", "implemented", "optimized", "developed", "resolved", "efficiently"]
    uncertain_phrases = ["i think", "maybe", "probably", "not sure", "i guess", "kind of", "sort of"]
    confident_count = sum(transcript.count(p) for p in confident_phrases)
    uncertain_count = sum(transcript.count(p) for p in uncertain_phrases)
    confidence_score = (70 + (confident_count * 5) - (uncertain_count * 7))
    confidence_score = max(0, min(100, confidence_score))
    return {
        "confidence_score": confidence_score,
        "confident_phrases": confident_count,
        "uncertain_phrases": uncertain_count
    }

def redundancy_analysis(words):
    word_counts = Counter(words)
    repeated_words = [word for word, count in word_counts.items() if count > 4 and len(word) > 3]
    redundancy_penalty = min(len(repeated_words) * 5, 30)
    return {
        "redundancy_score": 100 - redundancy_penalty,
        "repeated_terms": repeated_words[:10]
    }

def grammar_analysis(transcript):
    """
    Java-free grammar analysis using TextBlob for spelling/corrections 
    and SpaCy for structure checks.
    """
    blob = TextBlob(transcript)
    # TextBlob can check for spelling accuracy
    # (Simple heuristic: comparison of original vs corrected)
    corrected = blob.correct()
    
    # Analyze structure with Spacy
    doc = nlp(transcript)
    errors = 0
    
    # Heuristic 1: Sentence capitalization
    for sent in doc.sents:
        if not sent.text[0].isupper():
            errors += 1
            
    # Heuristic 2: Subject-Verb presence
    for sent in doc.sents:
        has_subj = any(tok.dep_ == "nsubj" for tok in sent)
        has_verb = any(tok.pos_ == "VERB" for tok in sent)
        if not has_subj or not has_verb:
            errors += 1

    # Heuristic 3: Fragmented sentences (too short)
    if len(transcript.split()) > 5: # only check if answer is long enough
        for sent in doc.sents:
            if len(sent.text.split()) < 3:
                errors += 1

    grammar_score = max(0, 100 - (errors * 5))
    
    return {
        "grammar_errors": errors,
        "grammar_score": grammar_score
    }

def sentence_complexity(transcript):
    sentences = sent_tokenize(transcript)
    words = word_tokenize(transcript)
    avg_sentence_length = (len(words) / len(sentences) if len(sentences) > 0 else 0)
    readability = textstat.flesch_reading_ease(transcript)
    return {
        "avg_sentence_length": round(avg_sentence_length, 2),
        "readability_score": round(readability, 2)
    }

def evaluate_technical_answer(domain: str, question: str, transcript: str) -> dict:
    transcript = clean_text(transcript)
    golden_answer = GOLDEN_ANSWERS.get(domain, {}).get(question, "")
    if not golden_answer or not transcript:
        return {"score": 0.0, "feedback": "Missing transcript or golden answer.", "suggestions": []}

    sim_score = semantic_similarity(transcript, golden_answer)
    golden_keywords = extract_keywords(golden_answer)
    transcript_keywords = extract_keywords(transcript)
    matched_keywords = list(set(golden_keywords).intersection(set(transcript_keywords)))
    missing_keywords = list(set(golden_keywords) - set(transcript_keywords))
    concept_coverage = (len(matched_keywords) / len(golden_keywords) if golden_keywords else 0)
    irrelevant_sentences, relevance_score = detect_irrelevant_sentences(transcript, golden_answer)
    words = [w.lower() for w in word_tokenize(transcript) if w.isalpha()]
    vocabulary_score = calculate_vocabulary_metrics(words)
    confidence_metrics = detect_confidence_language(transcript)
    redundancy_metrics = redundancy_analysis(words)
    grammar_metrics = grammar_analysis(transcript)
    complexity_metrics = sentence_complexity(transcript)

    final_score = (
        (sim_score * 40) +
        (concept_coverage * 20) +
        (relevance_score * 15) +
        (vocabulary_score / 100 * 10) +
        (confidence_metrics["confidence_score"] / 100 * 5) +
        (grammar_metrics["grammar_score"] / 100 * 5) +
        (redundancy_metrics["redundancy_score"] / 100 * 5)
    )

    final_score = round(min(100, max(0, final_score)), 2)
    strengths = []
    weaknesses = []
    if sim_score > 0.75: strengths.append("Strong semantic understanding")
    if vocabulary_score > 60: strengths.append("Rich vocabulary usage")
    if grammar_metrics["grammar_score"] > 85: strengths.append("Clear sentence structure")
    if confidence_metrics["confidence_score"] > 75: strengths.append("Confident communication")
    if irrelevant_sentences: weaknesses.append("Occasional off-topic remarks")
    if grammar_metrics["grammar_errors"] > 5: weaknesses.append("Sentence structure issues detected")
    if redundancy_metrics["repeated_terms"]: weaknesses.append("Repetitive terminology")

    feedback = ("Excellent performance." if final_score >= 80 else "Good effort with room for growth." if final_score >= 60 else "The response lacked depth and clarity.")
    suggestions = []
    if missing_keywords: suggestions.append(f"Try using terms like: {', '.join(missing_keywords[:5])}")
    if irrelevant_sentences: suggestions.append("Stay focused on the core question.")

    return {
        "score": final_score,
        "semantic_similarity": round(sim_score * 100, 2),
        "concept_coverage": round(concept_coverage * 100, 2),
        "topic_relevance": round(relevance_score * 100, 2),
        "feedback": feedback,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "irrelevant_sentences": irrelevant_sentences[:5],
        "metrics": {
            "matched_keywords": matched_keywords[:10],
            "missing_keywords": missing_keywords[:10],
            "vocabulary_score": vocabulary_score,
            "confidence_score": confidence_metrics["confidence_score"],
            "grammar_score": grammar_metrics["grammar_score"],
            "grammar_errors": grammar_metrics["grammar_errors"],
            "redundancy_score": redundancy_metrics["redundancy_score"],
            "repeated_terms": redundancy_metrics["repeated_terms"],
            "avg_sentence_length": complexity_metrics["avg_sentence_length"],
            "readability_score": complexity_metrics["readability_score"]
        }
    }

def analyze_communication(transcript: str, duration_sec: float) -> dict:
    transcript = clean_text(transcript)
    filler_words_list = ['um', 'uh', 'like', 'you know', 'actually', 'basically', 'literally']
    lower_transcript = transcript.lower()
    filler_count = sum(len(re.findall(r'\b' + re.escape(f) + r'\b', lower_transcript)) for f in filler_words_list)
    words = re.findall(r'\w+', transcript)
    total_words = len(words)
    wpm = (total_words / duration_sec) * 60 if duration_sec > 0 else 0
    vocabulary_score = calculate_vocabulary_metrics(words)
    grammar_metrics = grammar_analysis(transcript)
    confidence_metrics = detect_confidence_language(transcript)
    redundancy_metrics = redundancy_analysis(words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'of', 'in', 'that', 'i', 'it'}
    word_freq = {}
    for word in words:
        w = word.lower()
        if len(w) > 2 and w not in stop_words and w not in filler_words_list:
            word_freq[w] = word_freq.get(w, 0) + 1
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    word_distribution = [{"word": k, "count": v} for k, v in top_words]
    fluency_score = max(0, min(100, 100 - (filler_count * 3) - (abs(140 - wpm) * 0.5)))

    return {
        "wpm": round(wpm, 2),
        "total_words": total_words,
        "filler_count": filler_count,
        "fluency_score": round(fluency_score, 2),
        "vocabulary_score": vocabulary_score,
        "confidence_score": confidence_metrics["confidence_score"],
        "grammar_score": grammar_metrics["grammar_score"],
        "word_distribution": word_distribution,
        "communication_quality": ("Excellent" if fluency_score >= 80 else "Good" if fluency_score >= 60 else "Needs Improvement")
    }