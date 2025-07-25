
#!/usr/bin/env python3
"""
VaultScope – Simple Payment Surface Scanner
Reads URLs from a text file, crawls a small set of common paths,
flags payment‑related keywords, and (optionally) exports JSON or CSV results.

Author: euler707/lumark10  (MIT License)
"""
import requests
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv
import os
import argparse
import csv 
import json
import random


#CONFIGURABLE CONSTANTS
#----------------------

user_agents = [
                # Chrome
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                # Firefox
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
                # Edge
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
                # Safari (macOS)
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            ]

keywords = ['payment', 'billing', 'card', 'wallet', 'checkout', 'saved cards']

high_keywords = ['saved cards', 'manage payment methods', 'card number', 'expiration']

medium_keywords = ['payment', 'billing', 'wallet', 'checkout']

extra_paths = ['', '/terms', '/privacy', '/billing', '/faqs', '/support', '/help']

#-----------------------

#HELPER FUNCS
#-----------------------

def make_headers():
    """Return fresh browser-like headers for requests."""
    return {
            "User-Agent": random.choice(user_agents),
            "Accept": ("text/html,application/xhtml+xml,application/xml;"
            "q=0.9,*/*;q=0.8"),
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "close"
            }
def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

def find_payment_info(url: str, session: requests.Session) -> list[str]:
    try:
        response = session.get(url, headers=make_headers())
        response.raise_for_status() #check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if not soup.body:
            return []
        
        body_text = soup.body.get_text(" ", strip=True).lower()
        return [kw for kw in keywords if kw in body_text]
    
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def assess_risk(found_keywords):
    if any(kw in found_keywords for kw in high_keywords):
        return "High"
    elif any(kw in found_keywords for kw in medium_keywords):
        return "Medium"
    else:
        return "Low"


def safe_open(filename, base_dir = "data"):
    #only allow files in the base_dir
    safe_path = os.path.abspath(os.path.join(base_dir, filename))
    base_path = os.path.abspath(base_dir)
    if not safe_path.startswith(base_path):
        raise ValueError("Unsafe file path detected!")
    with open(safe_path, "r", encoding="utf-8") as f:
        return f.read()
    


def extract_urls_from_file(filename:str, base_dir="data") -> list[str]:
  
    try:
        content = safe_open(filename, base_dir)
        urls = [line.strip() for line in content.splitlines() if line.strip() and is_valid_url(line)]
        seen = set()
        return [u for u in urls if not (u in seen or seen.add(u))]
                
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading URL file: {e}")
    return []

#-----------------------

#EXPORT FUNCS
#-----------------------
def export_json(results: list[dict], outfile: str):
    try:
        with open(outfile, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results exported to -> {outfile}")
    except IOError as e:
        print(f"Error writing JSON file: {e}")
def export_csv(results: list[dict], outfile: str):
    fieldnames = ["url", "risk", "keywords"]
    try:
        with open(outfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow({
                    "url": row["url"],          
                    "risk": row["risk"],
                    "keywords": ";".join(row["keywords"]),
              })
        print(f"Results exported to -> {outfile}")
    except IOError as e:
        print(f"Error writing CSV file: {e}")
 #-----------------------

#MAIN FUNC
#------------------------

def scan(url_file: str, export: str | None):
    session = requests.Session()
   
    urls = extract_urls_from_file(url_file)
    if not urls:
        print("No valid URLs to scan. Exiting.")
        return
    
    results: list[dict] = []
    
    for base in urls:
        for path in extra_paths:
            full = base.rstrip('/') + path
            found = find_payment_info(full, session)
            risk = assess_risk(found)
            
            #output result
            print(f"URL: {full}")
            print(f"Risk level: {risk}")
            if found:
                print(f"Payment-related keywords found: {', '.join(found)}")
            else:
                print("No payment-related keywords found.")
            print("-" * 40)

            results.append({
                "url": full,
                "risk": risk,
                "keywords": found
            })
    
    #export if needed
    if export:
        ext = export.lower()
        if ext.endswith(".json"):
            export_json(results, export)
        elif ext.endswith(".csv"):
            export_csv(results, export)
        else:
            print(f"Unsupported export format: {ext}. Use .json or .csv")


        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VaultScope - payment surface scanner")
    parser.add_argument("file", help="Path to the txt file with URLs")
    parser.add_argument("-o", "--output", help="Output file for results (JSON or CSV). " 
                        "If omitted, results will be only printed to console.",)
    args = parser.parse_args()
    scan(args.file, args.output)
#Note!!! Ensure you have the necessary permissions to scrape on the target websites. Always respect robots.txt and terms of service.
