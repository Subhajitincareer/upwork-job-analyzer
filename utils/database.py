"""
Database/Storage Operations
JSON-based data storage with error handling
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from config import Config
from utils.logger import logger

class JobDatabase:
    """Job data storage manager"""
    
    def __init__(self):
        self.raw_dir = Config.RAW_DATA_DIR
        self.processed_dir = Config.PROCESSED_DATA_DIR
    
    def save_jobs(self, jobs: List[Dict], data_type='raw') -> Optional[str]:
        """
        Save jobs to JSON file
        
        Args:
            jobs: List of job dictionaries
            data_type: 'raw' or 'processed'
            
        Returns:
            Filename if successful, None otherwise
        """
        try:
            if data_type == 'raw':
                directory = self.raw_dir
            else:
                directory = self.processed_dir
            
            directory.mkdir(parents=True, exist_ok=True)
            
            filename = directory / f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'count': len(jobs),
                    'jobs': jobs
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved {len(jobs)} jobs to {filename}")
            return str(filename)
        
        except Exception as e:
            logger.error(f"Error saving jobs: {e}")
            return None
    
    def load_latest_jobs(self, data_type='raw') -> Optional[List[Dict]]:
        """Load most recent jobs"""
        try:
            if data_type == 'raw':
                directory = self.raw_dir
            else:
                directory = self.processed_dir
            
            files = sorted(directory.glob('jobs_*.json'), reverse=True)
            
            if not files:
                logger.warning("No previous data files found")
                return None
            
            with open(files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('jobs', [])
        
        except Exception as e:
            logger.error(f"Error loading jobs: {e}")
            return None
    
    def get_historical_stats(self, days=7) -> Dict:
        """Get historical statistics"""
        try:
            files = sorted(self.raw_dir.glob('jobs_*.json'), reverse=True)
            
            total_jobs = 0
            all_skills = {}
            
            for file in files[:days]:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    jobs = data.get('jobs', [])
                    total_jobs += len(jobs)
                    
                    for job in jobs:
                        for skill in job.get('skills', []):
                            all_skills[skill] = all_skills.get(skill, 0) + 1
            
            top_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                'total_jobs': total_jobs,
                'files_analyzed': len(files[:days]),
                'top_skills': top_skills,
                'average_jobs_per_day': total_jobs / min(days, len(files)) if files else 0
            }
        
        except Exception as e:
            logger.error(f"Error getting historical stats: {e}")
            return {}

# Global database instance
db = JobDatabase()

# Compatibility functions for old imports
def save_jobs_data(jobs: List[Dict]) -> Optional[str]:
    """Backward compatibility wrapper"""
    return db.save_jobs(jobs, 'raw')

def load_historical_data() -> Optional[Dict]:
    """Backward compatibility wrapper"""
    return db.get_historical_stats(days=7)
