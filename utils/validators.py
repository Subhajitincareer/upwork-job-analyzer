"""
Validation Utilities
Input validation and sanitization
"""

import re
from typing import Dict, List, Any

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_job_data(job: Dict[str, Any]) -> bool:
    """Validate job data structure"""
    required_fields = ['title', 'description', 'skills', 'scraped_at']
    return all(field in job for field in required_fields)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def validate_jobs_list(jobs: List[Dict]) -> List[Dict]:
    """Validate and filter jobs list"""
    valid_jobs = []
    for job in jobs:
        if validate_job_data(job):
            valid_jobs.append(job)
    return valid_jobs
