#!/usr/bin/env python3
"""
Test script to debug job description fetching.
Run: python test_description_fetch.py
"""
import requests
from bs4 import BeautifulSoup
import re

# Test with a known job ID (Macy's Product Manager)
JOB_ID = "4354633276"
URL = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{JOB_ID}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

print(f"Fetching: {URL}")
response = requests.get(URL, headers=headers, timeout=15)
print(f"Status: {response.status_code}")
print(f"Response length: {len(response.text)} chars")
print()

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for description divs
    for cls in ['description__text', 'show-more-less-html__markup', 'description']:
        el = soup.find(class_=cls)
        if el:
            print(f"Found element with class '{cls}': {len(el.get_text())} chars")
        else:
            print(f"No element with class '{cls}'")
    
    # Try regex fallback
    full_text = soup.get_text(separator='\n', strip=True)
    print(f"\nFull text length: {len(full_text)} chars")
    print(f"Contains 'Job Description': {'Job Description' in full_text}")
    print(f"Contains 'What You Will Do': {'What You Will Do' in full_text}")
    
    match = re.search(r'(Job Description).*?(?=Seniority level)', full_text, re.DOTALL | re.IGNORECASE)
    if match:
        print(f"\nRegex extracted: {len(match.group(0))} chars")
        print("First 500 chars:", match.group(0)[:500])
    else:
        print("\nRegex did not match")
        # Show sample of what we got
        if 'Job Description' in full_text:
            idx = full_text.find('Job Description')
            print("Text around 'Job Description':", full_text[idx:idx+300])
        else:
            print("First 500 chars of response:", full_text[:500])
else:
    print("Response:", response.text[:500])
