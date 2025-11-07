"""
Upwork Job Scraper
Production-ready web scraper with error handling and retries
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
from typing import List, Dict, Optional
from config import Config
from utils.logger import logger
from utils.validators import validate_jobs_list

class UpworkScraper:
    """Upwork job scraper with error handling"""
    
    def __init__(self):
        self.config = Config
        self.driver = None
    
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(self.config.TIMEOUT_SECONDS)
            
            logger.info("✅ Chrome driver initialized")
            return driver
        
        except Exception as e:
            logger.error(f"Failed to setup driver: {e}")
            raise
    
    def scrape_jobs(self, search_query: str, pages: int = 3) -> List[Dict]:
        """
        Scrape Upwork jobs with retry logic
        
        Args:
            search_query: Search term
            pages: Number of pages to scrape
            
        Returns:
            List of job dictionaries
        """
        all_jobs = []
        
        try:
            self.driver = self.setup_driver()
            
            for page in range(1, pages + 1):
                logger.info(f"📄 Scraping page {page}/{pages}")
                
                jobs = self._scrape_page(search_query, page)
                if jobs:
                    all_jobs.extend(jobs)
                    logger.info(f"✅ Page {page}: Found {len(jobs)} jobs")
                else:
                    logger.warning(f"⚠️  Page {page}: No jobs found")
                
                # Rate limiting
                if page < pages:
                    time.sleep(3)
            
            # Validate jobs
            valid_jobs = validate_jobs_list(all_jobs)
            logger.info(f"✅ Total valid jobs: {len(valid_jobs)}")
            
            return valid_jobs
        
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return all_jobs
        
        finally:
            self.cleanup()
    
    def _scrape_page(self, search_query: str, page: int) -> List[Dict]:
        """Scrape single page with retry"""
        for attempt in range(self.config.MAX_RETRIES):
            try:
                url = f"https://www.upwork.com/nx/search/jobs/?q={search_query.replace(' ', '%20')}&page={page}"
                
                self.driver.get(url)
                
                # Wait for jobs to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
                
                time.sleep(2)  # Allow dynamic content to load
                
                job_cards = self.driver.find_elements(By.TAG_NAME, "article")
                jobs = []
                
                for card in job_cards:
                    job_data = self._extract_job_data(card)
                    if job_data:
                        jobs.append(job_data)
                
                return jobs
            
            except TimeoutException:
                logger.warning(f"Timeout on page {page}, attempt {attempt + 1}/{self.config.MAX_RETRIES}")
                if attempt < self.config.MAX_RETRIES - 1:
                    time.sleep(5)
                else:
                    return []
            
            except Exception as e:
                logger.error(f"Error on page {page}: {e}")
                return []
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """Extract data from job card"""
        try:
            # Title
            try:
                title = card.find_element(By.CSS_SELECTOR, "h2, h3, [data-test='job-title']").text.strip()
            except:
                title = "N/A"
            
            # Description
            try:
                desc_elem = card.find_element(By.CSS_SELECTOR, "[data-test='job-description'], .job-description")
                description = desc_elem.text.strip()[:1000]
            except:
                description = card.text.strip()[:1000]
            
            # Skills
            skills = []
            try:
                skill_elements = card.find_elements(By.CSS_SELECTOR, "[data-test='token'], .skill-tag, .up-skill-badge")
                skills = [s.text.strip() for s in skill_elements if s.text.strip()]
            except:
                pass
            
            # Budget/Rate
            budget = "Not specified"
            try:
                budget_elem = card.find_element(By.CSS_SELECTOR, "[data-test='budget'], .budget")
                budget = budget_elem.text.strip()
            except:
                pass
            
            # Posted time
            posted = "Unknown"
            try:
                posted_elem = card.find_element(By.CSS_SELECTOR, "[data-test='posted-on'], .posted-on")
                posted = posted_elem.text.strip()
            except:
                pass
            
            if title and title != "N/A":
                return {
                    "title": title,
                    "description": description,
                    "skills": skills[:20],  # Limit skills
                    "budget": budget,
                    "posted": posted,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            
            return None
        
        except Exception as e:
            logger.debug(f"Error extracting job data: {e}")
            return None
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("🧹 Driver cleaned up")
            except:
                pass

# Global scraper instance
scraper = UpworkScraper()

def scrape_upwork_jobs(search_query: str, pages: int = 3) -> List[Dict]:
    """Main scraping function"""
    return scraper.scrape_jobs(search_query, pages)
