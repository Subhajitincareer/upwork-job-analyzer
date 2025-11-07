"""
Gemini AI Analyzer
Production-ready AI analysis with error handling
"""

import google.generativeai as genai
import json
from typing import List, Dict, Optional
from config import Config
from utils.logger import logger

class GeminiAnalyzer:
    """Gemini AI job analyzer"""
    
    def __init__(self):
        self.config = Config
        self.model = None
        self._configure()
    
    def _configure(self):
        """Configure Gemini API"""
        try:
            genai.configure(api_key=self.config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini API configured")
        except Exception as e:
            logger.error(f"Failed to configure Gemini: {e}")
            raise
    
    def analyze_jobs(self, jobs: List[Dict], historical_data: Optional[Dict] = None) -> str:
        """
        Analyze jobs with Gemini AI
        
        Args:
            jobs: List of job dictionaries
            historical_data: Previous analysis for comparison
            
        Returns:
            Analysis text
        """
        try:
            # Prepare data
            jobs_summary = self._prepare_summary(jobs)
            
            # Create prompt
            prompt = self._create_prompt(jobs_summary, len(jobs), historical_data)
            
            # Generate analysis
            logger.info("🧠 Generating analysis with Gemini...")
            response = self.model.generate_content(prompt)
            
            analysis = response.text
            logger.info("✅ Analysis generated successfully")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return self._generate_fallback_analysis(jobs)
    
    def _prepare_summary(self, jobs: List[Dict]) -> str:
        """Prepare concise job summary"""
        summary_data = []
        
        for i, job in enumerate(jobs[:50]):  # Limit to 50 for token limits
            summary_data.append({
                "id": i + 1,
                "title": job.get("title", "")[:100],
                "description": job.get("description", "")[:300],
                "skills": job.get("skills", [])[:10],
                "budget": job.get("budget", "Not specified")
            })
        
        return json.dumps(summary_data, indent=2)
    
    def _create_prompt(self, jobs_summary: str, total_jobs: int, historical_data: Optional[Dict]) -> str:
        """Create detailed analysis prompt"""
        
        historical_context = ""
        if historical_data:
            historical_context = f"""
HISTORICAL CONTEXT:
Previous analysis showed {historical_data.get('total_jobs', 0)} jobs.
Compare trends with current data.
"""
        
        prompt = f"""
You are an expert freelance market analyst specializing in AI/ML job trends.

Analyze these {total_jobs} Upwork job postings for AI/ML engineers.

JOBS DATA:
{jobs_summary}

{historical_context}

Provide a comprehensive analysis in this EXACT format:

## 📊 TOP DEMANDED SKILLS
List the top 10 most mentioned skills with their frequency count.
Format: 1. Skill Name - X mentions

## 🔥 COMMON PROJECT PATTERNS
Identify 5 most common types of projects being requested.
For each pattern, explain what clients typically want.

## 📈 TRENDING TECHNOLOGIES
List 5 new or increasingly popular technologies/frameworks.
Explain why each is trending.

## 💰 BUDGET INSIGHTS
- Average hourly rate range
- Average fixed price range
- Highest paying project categories
- Budget distribution (low/mid/high)

## 🎯 PROJECT RECOMMENDATION
Based on the patterns, recommend ONE specific portfolio project to build.
Include:
- Project name and description
- 4-5 key features to implement
- Technologies to use
- Why it's valuable for the market

## 📝 KEY TAKEAWAYS
Provide 5 actionable insights for freelancers.

## 📉 MARKET COMPARISON
{f"Compare with previous data trends." if historical_data else "First analysis - establish baseline."}

Keep the analysis professional, data-driven, and actionable.
"""
        
        return prompt
    
    def _generate_fallback_analysis(self, jobs: List[Dict]) -> str:
        """Generate basic analysis if AI fails"""
        skills_count = {}
        
        for job in jobs:
            for skill in job.get('skills', []):
                skills_count[skill] = skills_count.get(skill, 0) + 1
        
        top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        analysis = f"""
# Upwork Job Analysis (Fallback Mode)

## Total Jobs Analyzed: {len(jobs)}

## Top Skills:
"""
        for i, (skill, count) in enumerate(top_skills, 1):
            analysis += f"{i}. {skill} - {count} mentions\n"
        
        analysis += "\n⚠️ Full AI analysis unavailable. This is a basic summary.\n"
        
        return analysis

# Global analyzer instance
analyzer = GeminiAnalyzer()

def analyze_jobs_with_gemini(jobs: List[Dict], historical_data: Optional[Dict] = None) -> str:
    """Main analysis function"""
    return analyzer.analyze_jobs(jobs, historical_data)
