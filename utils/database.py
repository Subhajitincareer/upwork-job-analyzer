"""Database Functions"""

import json
import os
from datetime import datetime

def save_jobs_data(jobs):
    """Save jobs to JSON"""
    filename = f"data/raw/jobs_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(jobs)} jobs to {filename}")

def load_historical_data():
    """Load previous day's data for comparison"""
    try:
        files = sorted(os.listdir('data/raw'))
        if len(files) >= 2:
            with open(f"data/raw/{files[-2]}", 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return None

