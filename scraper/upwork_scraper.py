"""Upwork Job Scraper"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import logging

def setup_driver():
    """Setup Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_upwork_jobs(search_query, pages=3):
    """
    Scrape Upwork jobs
    
    Args:
        search_query: Search term
        pages: Number of pages
        
    Returns:
        List of jobs
    """
    driver = setup_driver()
    jobs = []
    
    try:
        for page in range(1, pages + 1):
            url = f"https://www.upwork.com/nx/search/jobs/?q={search_query.replace(' ', '%20')}&page={page}"
            
            logging.info(f"Scraping page {page}")
            driver.get(url)
            time.sleep(3)
            
            # Extract jobs
            try:
                job_cards = driver.find_elements(By.TAG_NAME, "article")
                
                for card in job_cards:
                    try:
                        job = extract_job_data(card)
                        if job:
                            jobs.append(job)
                    except Exception as e:
                        logging.warning(f"Error extracting job: {e}")
                        continue
                
                logging.info(f"Page {page}: Found {len(job_cards)} jobs")
            except Exception as e:
                logging.error(f"Page {page} error: {e}")
            
            time.sleep(2)
    
    finally:
        driver.quit()
    
    return jobs

def extract_job_data(card):
    """Extract data from job card"""
    try:
        # Title
        title = card.find_element(By.CSS_SELECTOR, "h2, h3").text.strip()
        
        # Description (first 500 chars)
        desc = card.text.strip()[:500]
        
        # Skills
        skills = []
        try:
            skill_elements = card.find_elements(By.CSS_SELECTOR, "[data-test='token'], .skill")
            skills = [s.text.strip() for s in skill_elements if s.text.strip()]
        except:
            pass
        
        return {
            "title": title,
            "description": desc,
            "skills": skills,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except Exception as e:
        return None

