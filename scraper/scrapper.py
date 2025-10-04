import os
import requests
from bs4 import BeautifulSoup
import csv
from utils import logger, get_mongo_collection

col = get_mongo_collection()


def handle_correction_page(correction_link, soup):
    """
    Handles correction pages robustly:
    1. Updates the original article document:
       - Adds correction link to 'corrections' array
       - Adds 'correction' tag to 'tags' array
    2. Ensures a document exists for the correction page itself.
    """
    # Find the outer div
    outer_div = soup.find("div", class_="ra xbox p")
    if not outer_div:
        logger.warning(f"No outer div with class 'ra xbox p' found: {correction_link}")
        return True

    # Find <a class="usa-link"> inside outer div
    a_tag = outer_div.find("a", class_="usa-link", href=True)
    if not a_tag:
        logger.warning(f"No <a class='usa-link'> found inside outer div: {correction_link}")
        return True

    corrected_partial = a_tag['href']  # e.g., /articles/PMC6915713/

    # -----------------------------
    # 1️ Update original article
    # -----------------------------
    orig_result = col.update_one(
        {"link": {"$regex": corrected_partial}},  # match original article
        {
            "$addToSet": {
                "corrections": correction_link,  # append this correction link
                "tags": "correction"             # add 'correction' tag
            }
        },
        upsert=True
    )

    if orig_result.upserted_id:
        logger.info(f"Original article not found; created new document with correction: {corrected_partial}")
    elif orig_result.matched_count:
        logger.info(f"Added correction link and tag to existing article: {corrected_partial}")
    else:
        logger.warning(f"Unexpected: No update or insert occurred for original article: {corrected_partial}")

    # -----------------------------
    # 2️ Upsert the correction page itself
    # -----------------------------
    correction_result = col.update_one(
        {"link": correction_link},
        {"$setOnInsert": {"link": correction_link, "abstractText": "", "score": 0, "tags": ["correction"]}},
        upsert=True
    )

    if correction_result.upserted_id:
        logger.info(f"Created document for correction page: {correction_link}")
    else:
        logger.info(f"Correction page document already exists: {correction_link}")

    return True



def get_abstract(link):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; SpaceAppsBot/1.0)"}
        r = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # -----------------------------
        # Handle correction pages
        # -----------------------------
        if "This corrects the article" in soup.get_text():
            handle_correction_page(link, soup)
            return ""  # No abstract stored for correction pages

        # -----------------------------
        # Extract normal abstract by ID
        # -----------------------------
        abstract = ""
        for aid in ["Par2", "abstract2", "abstract1", "Abs1", "ab0005", "abs0010", "ABS1", "aps31197-abs-0001cl"]:
            ab = soup.find(id=aid)
            if ab:
                abstract = " ".join(p.get_text(strip=True) for p in ab.find_all("p"))
                break  # Stop at first match

        # -----------------------------
        # Fallback: look for class="abstract" and take the first <p>
        # -----------------------------
        if not abstract:
            ab_class = soup.find(class_="abstract")
            if ab_class:
                p_tag = ab_class.find("p")
                if p_tag:
                    abstract = p_tag.get_text(strip=True)

        if not abstract:
            logger.error(f"No abstract found for {link}")
            return ""

        # Clean / encode to UTF-8 safely
        abstract = abstract.encode("utf-8", errors="replace").decode("utf-8")

        logger.info(f"Abstract extracted ({link}): {abstract[:100]}...")  # log first 100 chars
        return abstract

    except Exception as e:
        logger.warning(f"Failed to fetch abstract from {link}: {e}")
        return ""

# -------------------------
# Load CSV and upsert into Mongo
# -------------------------
csv_path = os.path.join(os.path.dirname(__file__), "publications.csv")

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row["Title"].strip()
        link = row["Link"].strip()

        # Check if abstract already exists
        existing = col.find_one({"link": link})
        if existing and existing.get("abstractText"):
            # logger.info(f"[>] Skipping (already has abstract): {title}")
            continue

        # Fetch and clean abstract
        abstract = get_abstract(link)

        if not abstract:
            logger.error(f"Skipping update: No abstract found for {title}")
            continue

        # Upsert: insert if not exists, update if exists
        result = col.update_one(
            {"link": link},   # filter by link
            {
                "$set": {
                    "title": title,
                    "abstractText": abstract,
                    "tags": []
                }
            },
            upsert=True
        )

        if result.matched_count:
            logger.info(f"[~] Updated: {title}")
        else:
            logger.info(f"[+] Inserted: {title}")
