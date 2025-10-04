import os
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import csv

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/spaceapps")
client = MongoClient(mongo_uri)
db = client["spaceapps"]
col = db["publications"]

# Load CSV (mounted in container)
with open("publications.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row["Title"].strip()
        link = row["Link"].strip()
        # Skip if already exists
        if col.find_one({"link": link}):
            continue

        # Scrape abstract (simple example)
        abstract = ""
        try:
            r = requests.get(link, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            ab = soup.find("div", {"class": "abstract"})
            if ab:
                abstract = ab.get_text(strip=True)
        except Exception as e:
            print(f"[!] Failed {link}: {e}")

        col.insert_one({
            "title": title,
            "link": link,
            "abstractText": abstract,
            "tags": [],
            "score": 0
        })
        print(f"[+] Added: {title}")
