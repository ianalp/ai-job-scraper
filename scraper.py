"""
AI Job Scraper - Main scraping module
Scrapes job listings from multiple Korean job sites
"""

import asyncio
from playwright.async_api import async_playwright
import sqlite3
from datetime import datetime
import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobScraper:
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with jobs table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                salary TEXT,
                experience TEXT,
                education TEXT,
                url TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                posted_date TEXT,
                scraped_date TEXT NOT NULL,
                keywords TEXT
            )
        """)
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def save_jobs(self, jobs: List[Dict]):
        """Save jobs to database, skip duplicates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for job in jobs:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO jobs 
                    (title, company, location, salary, experience, education, url, source, posted_date, scraped_date, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.get('title'),
                    job.get('company'),
                    job.get('location'),
                    job.get('salary'),
                    job.get('experience'),
                    job.get('education'),
                    job.get('url'),
                    job.get('source'),
                    job.get('posted_date'),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    job.get('keywords', '')
                ))
                if cursor.rowcount > 0:
                    saved_count += 1
            except Exception as e:
                logger.error(f"Error saving job: {e}")
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {saved_count} new jobs (out of {len(jobs)} scraped)")
        return saved_count
    
    async def scrape_saramin(self, keyword: str = "개발자", pages: int = 3) -> List[Dict]:
        """Scrape jobs from Saramin"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                for page_num in range(1, pages + 1):
                    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page_num}"
                    logger.info(f"Scraping Saramin page {page_num}: {url}")
                    
                    await page.goto(url, wait_until="networkidle")
                    await page.wait_for_timeout(2000)
                    
                    # Extract job listings
                    job_items = await page.query_selector_all(".item_recruit")
                    
                    for item in job_items:
                        try:
                            title_elem = await item.query_selector(".job_tit a")
                            company_elem = await item.query_selector(".corp_name a")
                            conditions_elem = await item.query_selector(".job_condition")
                            
                            if title_elem and company_elem:
                                title = await title_elem.inner_text()
                                company = await company_elem.inner_text()
                                job_url = await title_elem.get_attribute("href")
                                
                                conditions = await conditions_elem.inner_text() if conditions_elem else ""
                                conditions_list = conditions.split(",") if conditions else []
                                
                                jobs.append({
                                    'title': title.strip(),
                                    'company': company.strip(),
                                    'location': conditions_list[0].strip() if len(conditions_list) > 0 else "",
                                    'experience': conditions_list[1].strip() if len(conditions_list) > 1 else "",
                                    'education': conditions_list[2].strip() if len(conditions_list) > 2 else "",
                                    'salary': "",
                                    'url': f"https://www.saramin.co.kr{job_url}" if job_url else "",
                                    'source': 'Saramin',
                                    'posted_date': '',
                                    'keywords': keyword
                                })
                        except Exception as e:
                            logger.error(f"Error parsing job item: {e}")
                            continue
                    
                    logger.info(f"Found {len(job_items)} jobs on page {page_num}")
                    await page.wait_for_timeout(1000)
            
            except Exception as e:
                logger.error(f"Error scraping Saramin: {e}")
            finally:
                await browser.close()
        
        return jobs
    
    async def scrape_jobkorea(self, keyword: str = "개발자", pages: int = 3) -> List[Dict]:
        """Scrape jobs from JobKorea"""
        jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                for page_num in range(1, pages + 1):
                    url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}&Page_No={page_num}"
                    logger.info(f"Scraping JobKorea page {page_num}: {url}")
                    
                    await page.goto(url, wait_until="networkidle")
                    await page.wait_for_timeout(2000)
                    
                    # Extract job listings
                    job_items = await page.query_selector_all(".list-default__item")
                    
                    for item in job_items:
                        try:
                            title_elem = await item.query_selector(".information-title a")
                            company_elem = await item.query_selector(".name a")
                            
                            if title_elem and company_elem:
                                title = await title_elem.inner_text()
                                company = await company_elem.inner_text()
                                job_url = await title_elem.get_attribute("href")
                                
                                # Get additional info
                                location_elem = await item.query_selector(".option:has-text('지역')")
                                experience_elem = await item.query_selector(".option:has-text('경력')")
                                education_elem = await item.query_selector(".option:has-text('학력')")
                                
                                location = await location_elem.inner_text() if location_elem else ""
                                experience = await experience_elem.inner_text() if experience_elem else ""
                                education = await education_elem.inner_text() if education_elem else ""
                                
                                jobs.append({
                                    'title': title.strip(),
                                    'company': company.strip(),
                                    'location': location.replace('지역', '').strip(),
                                    'experience': experience.replace('경력', '').strip(),
                                    'education': education.replace('학력', '').strip(),
                                    'salary': "",
                                    'url': f"https://www.jobkorea.co.kr{job_url}" if job_url and not job_url.startswith('http') else job_url,
                                    'source': 'JobKorea',
                                    'posted_date': '',
                                    'keywords': keyword
                                })
                        except Exception as e:
                            logger.error(f"Error parsing job item: {e}")
                            continue
                    
                    logger.info(f"Found {len(job_items)} jobs on page {page_num}")
                    await page.wait_for_timeout(1000)
            
            except Exception as e:
                logger.error(f"Error scraping JobKorea: {e}")
            finally:
                await browser.close()
        
        return jobs
    
    async def scrape_all(self, keywords: List[str] = ["개발자", "데이터분석"], pages_per_site: int = 3):
        """Scrape all job sites with given keywords"""
        all_jobs = []
        
        for keyword in keywords:
            logger.info(f"Scraping for keyword: {keyword}")
            
            # Scrape Saramin
            saramin_jobs = await self.scrape_saramin(keyword, pages_per_site)
            all_jobs.extend(saramin_jobs)
            
            # Scrape JobKorea
            jobkorea_jobs = await self.scrape_jobkorea(keyword, pages_per_site)
            all_jobs.extend(jobkorea_jobs)
            
            await asyncio.sleep(2)  # Be nice to servers
        
        # Save to database
        saved_count = self.save_jobs(all_jobs)
        
        logger.info(f"Total scraped: {len(all_jobs)} jobs")
        logger.info(f"New jobs saved: {saved_count}")
        
        return all_jobs


if __name__ == "__main__":
    scraper = JobScraper()
    
    # Example usage
    keywords = ["Python 개발자", "데이터 엔지니어", "백엔드 개발자"]
    asyncio.run(scraper.scrape_all(keywords=keywords, pages_per_site=2))
