"""
LinkedIn Product Management Job Tracker with Google Sheets Integration
Personal use job hunting tool
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

class LinkedInJobTracker:
    def __init__(self, use_sheets=False, sheet_name="LinkedIn PM Jobs"):
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.linkedin.com/jobs/',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
        }
        self.jobs = []
        self.use_sheets = use_sheets
        self.sheet_name = sheet_name
        self.sheet = None
        
        if use_sheets:
            self._setup_google_sheets()
    
    def _setup_google_sheets(self):
        """Setup Google Sheets connection"""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Add credentials from JSON file
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                'credentials.json', 
                scope
            )
            
            client = gspread.authorize(creds)
            
            # Try to open existing sheet or create new one
            try:
                self.spreadsheet = client.open(self.sheet_name)
                self.sheet = self.spreadsheet.sheet1
                print(f"📊 Connected to existing Google Sheet: '{self.sheet_name}'")
            except gspread.SpreadsheetNotFound:
                self.spreadsheet = client.create(self.sheet_name)
                self.sheet = self.spreadsheet.sheet1
                
                # Set up headers (Description at end for Agent 2 resume customization)
                headers = [
                    'Job ID', 'Title', 'Company', 'Location', 
                    'Link', 'Found Date', 'Status', 'Notes', 'Description'
                ]
                self.sheet.update('A1:I1', [headers])
                
                # Format header row
                self.sheet.format('A1:I1', {
                    'textFormat': {'bold': True},
                    'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9}
                })
                
                print(f"✨ Created new Google Sheet: '{self.sheet_name}'")
                print(f"🔗 Access it here: {self.spreadsheet.url}")
            
        except FileNotFoundError:
            print("❌ credentials.json not found!")
            print("📝 Please follow the setup guide to create credentials.")
            self.use_sheets = False
        except Exception as e:
            print(f"❌ Error setting up Google Sheets: {str(e)}")
            self.use_sheets = False
    
    def search_jobs(self, keywords="product manager", location="", num_jobs=50):
        """
        Search for jobs on LinkedIn
        
        Args:
            keywords: Job search keywords (default: "product manager")
            location: Location filter - string only (e.g., "India" or "San Francisco, CA")
            num_jobs: Number of jobs to fetch (default: 50)
        """
        # Ensure location is a single string (API ignores/breaks with list)
        if isinstance(location, list):
            location = location[0] if location else ""
        
        print(f"🔍 Searching for '{keywords}' jobs" + (f" in {location}" if location else "") + "...")
        
        self.jobs = []
        jobs_per_page = 25
        start = 0
        
        try:
            while len(self.jobs) < num_jobs:
                params = {
                    'keywords': keywords,
                    'location': location,
                    'start': start,
                    'f_TPR': 'r604800',  # Past 7 days
                }
                
                response = requests.get(
                    self.base_url,
                    params=params,
                    headers=self.headers,
                    timeout=15
                )
                
                if response.status_code != 200:
                    print(f"❌ Error: Status code {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('li')
                
                if not job_cards:
                    print(f"   No more results at start={start}")
                    break
                
                page_count = 0
                for card in job_cards:
                    if len(self.jobs) >= num_jobs:
                        break
                    job_data = self._parse_job_card(card)
                    if job_data:
                        self.jobs.append(job_data)
                        page_count += 1
                
                print(f"   Fetched page {start // jobs_per_page + 1}: +{page_count} jobs (total: {len(self.jobs)})")
                
                if page_count < jobs_per_page:
                    break
                
                start += jobs_per_page
                time.sleep(2)  # Rate limiting between pages
            
            print(f"✅ Found {len(self.jobs)} jobs")
            return self.jobs
                
        except Exception as e:
            print(f"❌ Error fetching jobs: {str(e)}")
            return []
    
    def _parse_job_card(self, card):
        """Extract job information from a job card"""
        try:
            # Find job title and link
            title_elem = card.find('h3', class_='base-search-card__title')
            link_elem = card.find('a', class_='base-card__full-link')
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            location_elem = card.find('span', class_='job-search-card__location')
            
            if not title_elem or not link_elem:
                return None
            
            job_title = title_elem.text.strip()
            job_link = link_elem.get('href', '').split('?')[0]  # Clean URL
            company = company_elem.text.strip() if company_elem else "Unknown"
            location = location_elem.text.strip() if location_elem else "Unknown"
            
            # Extract job ID from URL (format: .../jobs/view/title-company-1234567890)
            job_id_match = re.search(r'-(\d+)(?:\?|$)', job_link) or re.search(r'/(\d+)(?:\?|$)', job_link)
            job_id = job_id_match.group(1) if job_id_match else None
            
            return {
                'job_id': job_id,
                'title': job_title,
                'company': company,
                'location': location,
                'link': job_link,
                'found_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'New',
                'notes': ''
            }
            
        except Exception as e:
            print(f"⚠️  Error parsing job card: {str(e)}")
            return None
    
    def fetch_job_description(self, job_id):
        """
        Fetch full job description from LinkedIn's job posting API (no login required).
        Returns text including Job Overview, What You Will Do, Skills, etc.
        """
        if not job_id:
            return None
        try:
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return None
            html = response.text
            if not html or len(html) < 500:
                return None
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try common LinkedIn description containers (class names may vary)
            desc_div = (
                soup.find('div', class_='description__text') or
                soup.find('div', class_='show-more-less-html__markup') or
                soup.find('section', class_='description') or
                soup.find('div', class_='job-view-layout jobs-details')
            )
            if desc_div:
                text = desc_div.get_text(strip=True, separator='\n')
                if len(text) >= 100:
                    return text
            
            # Fallback: extract from full page text between known markers
            full_text = soup.get_text(separator='\n', strip=True)
            end_pattern = r'(?:Show more|Seniority level|Employment type|Job function|Industries|Referrals|Featured Benefits)'
            for start in ['Job Description', 'Job Overview', 'About the job']:
                match = re.search(
                    f'({re.escape(start)}).*?(?={end_pattern})',
                    full_text,
                    re.DOTALL | re.IGNORECASE
                )
                if match:
                    text = match.group(0).strip()
                    if len(text) >= 200:
                        return text
            
            # Last resort: get body text if it looks like job content
            body = soup.find('body')
            if body:
                text = body.get_text(strip=True, separator='\n')
                if len(text) >= 500 and any(kw in text.lower() for kw in ['responsibilities', 'experience', 'product', 'skills']):
                    return text
            return None
        except Exception:
            return None
    
    def filter_product_management(self):
        """Filter jobs to only include product management related roles"""
        pm_keywords = [
            'product manager',
            'product management',
            'product owner',
            'product lead',
            'group product manager',
            'senior product manager',
            'principal product manager',
            'associate product manager',
            'apm',
            'gpm',
            'spm',
            'head of product',
            'director of product',
            'vp product',
            'chief product officer'
        ]
        
        filtered_jobs = []
        for job in self.jobs:
            title_lower = job['title'].lower()
            if any(keyword in title_lower for keyword in pm_keywords):
                filtered_jobs.append(job)
        
        print(f"🎯 Filtered to {len(filtered_jobs)} product management roles")
        self.jobs = filtered_jobs
        return filtered_jobs
    
    def save_to_sheets(self, fetch_descriptions=True, max_description_fetches=20):
        """
        Save jobs to Google Sheets.
        fetch_descriptions: If True, fetches job descriptions via LinkedIn API
        max_description_fetches: Limit fetches per run to avoid rate limits (default 20)
        """
        if not self.use_sheets or not self.sheet:
            print("❌ Google Sheets not configured")
            return
        
        try:
            # Ensure Description column exists (for existing sheets)
            existing_data = self.sheet.get_all_values()
            headers = existing_data[0] if existing_data else []
            if 'Description' not in headers:
                desc_col = len(headers) + 1
                self.sheet.update_cell(1, desc_col, 'Description')
                print("   Added Description column to sheet")
            
            existing_ids = set()
            if len(existing_data) > 1:
                for row in existing_data[1:]:
                    if row and row[0]:
                        existing_ids.add(str(row[0]))
                    if len(row) > 4 and row[4]:
                        existing_ids.add(row[4])
            
            # Prepare new rows (with descriptions)
            new_rows = []
            fetch_count = 0
            for job in self.jobs:
                job_id = job.get('job_id') or job.get('link', '')
                if job_id not in existing_ids and job.get('link') not in existing_ids:
                    description = ''
                    if fetch_descriptions and job.get('job_id') and fetch_count < max_description_fetches:
                        print(f"   Fetching description for {job.get('title', '')[:40]}...")
                        description = self.fetch_job_description(job['job_id']) or ''
                        fetch_count += 1
                        if description:
                            print(f"      ✓ Got {len(description)} chars")
                        else:
                            print(f"      ⚠ No description")
                        time.sleep(2)  # Rate limiting
                    
                    row = [
                        job['job_id'],
                        job['title'],
                        job['company'],
                        job['location'],
                        job['link'],
                        job['found_date'],
                        job['status'],
                        job['notes'],
                        description
                    ]
                    new_rows.append(row)
            
            if new_rows:
                self.sheet.append_rows(new_rows)
                print(f"📊 Added {len(new_rows)} new jobs to Google Sheets")
                print(f"🔗 View your sheet: {self.spreadsheet.url}")
            else:
                print("ℹ️  No new jobs to add (all jobs already in sheet)")
            
            total_jobs = len(self.sheet.get_all_values()) - 1
            print(f"📈 Total jobs tracked: {total_jobs}")
            
        except Exception as e:
            print(f"❌ Error saving to Google Sheets: {str(e)}")
    
    def save_to_json(self, filename='linkedin_jobs.json'):
        """Save jobs to a JSON file (backup)"""
        try:
            # Load existing jobs if file exists
            existing_jobs = []
            try:
                with open(filename, 'r') as f:
                    existing_jobs = json.load(f)
            except FileNotFoundError:
                pass
            
            # Merge with new jobs (avoid duplicates by job_id or link)
            existing_ids = {str(j.get('job_id')) for j in existing_jobs if j.get('job_id')}
            existing_links = {j.get('link') for j in existing_jobs if j.get('link')}
            new_jobs = [
                job for job in self.jobs
                if job.get('job_id') not in existing_ids and job.get('link') not in existing_links
            ]
            
            all_jobs = existing_jobs + new_jobs
            
            with open(filename, 'w') as f:
                json.dump(all_jobs, f, indent=2)
            
            print(f"💾 Saved {len(new_jobs)} new jobs to {filename} (backup)")
            
        except Exception as e:
            print(f"❌ Error saving to JSON: {str(e)}")
    
    def print_jobs(self):
        """Print jobs in a readable format"""
        if not self.jobs:
            print("No jobs found.")
            return
        
        print(f"\n📋 Found {len(self.jobs)} jobs:\n")
        print("-" * 80)
        
        for i, job in enumerate(self.jobs, 1):
            print(f"{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Link: {job['link']}")
            print(f"   Found: {job['found_date']}")
            print("-" * 80)


def main():
    """Main execution function"""
    print("🚀 LinkedIn Product Management Job Tracker\n")
    
    # Check if credentials exist
    use_sheets = os.path.exists('credentials.json')
    
    if use_sheets:
        print("✅ Found credentials.json - will save to Google Sheets")
    else:
        print("⚠️  No credentials.json found - will save to JSON only")
        print("💡 Follow GOOGLE_SHEETS_SETUP.md to enable Google Sheets\n")
    
    # Initialize tracker
    tracker = LinkedInJobTracker(
        use_sheets=use_sheets,
        sheet_name="LinkedIn PM Jobs"  # You can customize this name
    )
    
    # Search for jobs
    # Customize: location must be a single string (e.g. "India", "Bangalore", "Remote")
    tracker.search_jobs(
        keywords="product manager",
        location="India",
        num_jobs=100   # Number of jobs to fetch
    )
    
    # Filter for product management roles
    tracker.filter_product_management()
    
    # Display results
    tracker.print_jobs()
    
    # Save to Google Sheets (if configured)
    if use_sheets and tracker.sheet:
        tracker.save_to_sheets()
    
    # Always save to JSON as backup
    tracker.save_to_json('linkedin_pm_jobs.json')
    
    print("\n✅ Job search complete!")
    if use_sheets and tracker.sheet:
        print(f"🔗 View your Google Sheet: {tracker.spreadsheet.url}")
    print("💡 Tip: Run this script daily to keep your job list updated.")


if __name__ == "__main__":
    main()
