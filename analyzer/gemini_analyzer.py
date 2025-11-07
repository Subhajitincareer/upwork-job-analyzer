"""Gemini AI Analyzer"""

import google.generativeai as genai
import os
import json
import logging

def configure_gemini():
    """Configure Gemini API"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def analyze_jobs_with_gemini(jobs_data):
    """
    Analyze jobs with Gemini AI
    
    Args:
        jobs_data: List of jobs
        
    Returns:
        Analysis text
    """
    model = configure_gemini()
    
    # Prepare summary
    jobs_summary = json.dumps([
        {
            "title": job["title"],
            "description": job["description"][:300],
            "skills": job["skills"]
        }
        for job in jobs_data
    ], indent=2)
    
    # Create prompt
    prompt = f"""
Analyze these {len(jobs_data)} AI/ML Upwork job postings.

JOBS DATA:
{jobs_summary}

Provide detailed analysis in this format:

## 📊 TOP DEMANDED SKILLS
List top 10 skills with counts.

## 🔥 COMMON PROJECT PATTERNS
What types of projects are most common?

## 📈 TRENDING TECHNOLOGIES
What's new or increasing?

## 💰 BUDGET INSIGHTS
Average ranges and high-paying types.

## 💡 PROJECT RECOMMENDATION
Suggest ONE specific portfolio project based on patterns.

## 📝 KEY TAKEAWAYS
3-5 actionable insights.
"""
    
    logging.info("Analyzing with Gemini...")
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return f"Analysis failed: {e}"

