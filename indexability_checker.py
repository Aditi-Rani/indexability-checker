import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import sys

def is_allowed_by_robots(url):
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except:
        return False

def check_indexability(url):
    try:
        print(f"\n🔍 Checking: {url}")
        
        if not is_allowed_by_robots(url):
            print("🚫 Blocked by robots.txt")
            return

        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for noindex in meta
        meta_robots = soup.find("meta", attrs={"name": "robots"})
        if meta_robots and "noindex" in meta_robots.get("content", "").lower():
            print("🚫 noindex directive found in meta tag.")
        else:
            print("✅ Page is indexable (no 'noindex' tag).")

        # Check for canonical tag
        canonical_tag = soup.find("link", rel="canonical")
        if canonical_tag and canonical_tag.get("href"):
            print(f"🔗 Canonical URL: {canonical_tag['href']}")
        else:
            print("⚠️ No canonical tag found.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    url = input("Enter the full URL to check: ").strip()
    check_indexability(url)
