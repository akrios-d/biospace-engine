import json
import requests
from utils import logger, get_mongo_collection

# MongoDB collection
col = get_mongo_collection()

def classify_with_ollama_free(abstract: str) -> str:
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "GPT-OSS:20B",
        "prompt": f"""
Read the following scientific abstract carefully and assign it a single, concise category 
that best represents its primary content or research focus. Choose the most specific category possible. 
If the abstract spans multiple disciplines, prioritize the main focus. Only respond with the category name.

Abstract: {abstract}
"""
    }

    response = requests.post(url, json=data, headers=headers)
    # Handle streamed/multi-line responses
    for line in response.text.splitlines():
        try:
            obj = json.loads(line)
            if "response" in obj:
                return obj["response"].strip()
        except json.JSONDecodeError:
            continue
    return "Unknown"

def classify_all_publications():
    for pub in col.find():
        abstract = pub.get("abstractText", "")
        if not abstract:
            logger.info(f"Skipping {pub.get('title')} (no abstract)")
            continue

        logger.info(f"Classifying: {pub.get('title')}")
        category = classify_with_ollama_free(abstract)

        # Optional: define tags based on category or other heuristics
        tags_to_add = []
        if category.lower() in ["correction", "erratum"]:
            tags_to_add.append("correction")
        # Example: tag by keywords
        if "mouse" in abstract.lower():
            tags_to_add.append("mouse study")
        if "space" in abstract.lower() or "astronaut" in abstract.lower():
            tags_to_add.append("space biology")

        # Upsert category and tags in MongoDB
        update_doc = {"$set": {"category": category}}
        if tags_to_add:
            update_doc["$addToSet"] = {"tags": {"$each": tags_to_add}}

        col.update_one({"_id": pub["_id"]}, update_doc)
        logger.info(f"Updated: {pub.get('title')} -> {category}, tags: {tags_to_add}")

if __name__ == "__main__":
    logger.info("Starting classification...")
    classify_all_publications()
    logger.info("Classification completed.")
