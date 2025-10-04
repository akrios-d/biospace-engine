import json
import requests
from utils import logger, get_mongo_collection

col = get_mongo_collection()

def classify_with_ollama_free(abstract: str) -> dict:
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "GPT-OSS:20B",
        "prompt": f"""
Read the following scientific abstract carefully.

Instructions:
1. Assign 1–3 relevant categories that best describe the main topics of the research.
2. If you are not confident or the text is too broad/unclear, use ["Not Categorized"] as the categories list.
3. Suggest up to 5 meaningful tags based on key methods, organisms, field, or implications.
4. If you marked it as "Not Categorized", include the tag "requires human evaluation".
5. Respond ONLY in JSON format exactly like this:

{{
  "categories": ["Category1", "Category2"],
  "tags": ["tag1", "tag2", "tag3"]
}}

Abstract:
{abstract}
"""
    }

    response = requests.post(url, json=data, headers=headers)
    raw_output = ""
    for line in response.text.splitlines():
        try:
            obj = json.loads(line)
            if "response" in obj:
                raw_output += obj["response"]
        except json.JSONDecodeError:
            continue

    # Try parsing model's JSON output
    try:
        result = json.loads(raw_output)
        categories = result.get("categories", [])
        tags = result.get("tags", [])

        # Clean up
        if isinstance(categories, str):
            categories = [c.strip() for c in categories.split(",") if c.strip()]
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        # Safety fallback if model gives nothing
        if not categories:
            categories = ["Not Categorized"]
            if "requires human evaluation" not in tags:
                tags.append("requires human evaluation")

        return {"categories": categories, "tags": tags}

    except json.JSONDecodeError:
        logger.warning(f"Could not parse model output as JSON. Raw: {raw_output}")
        return {
            "categories": ["Not Categorized"],
            "tags": ["requires human evaluation"]
        }

def classify_all_publications():
    for pub in col.find():
        abstract = pub.get("abstractText", "")
        if not abstract:
            logger.info(f"Skipping {pub.get('title')} (no abstract)")
            continue

        logger.info(f"Classifying: {pub.get('title')}")
        result = classify_with_ollama_free(abstract)
        categories = result["categories"]
        tags = result["tags"]

        # Upsert categories and tags into MongoDB
        update_doc = {"$set": {"categories": categories}}
        if tags:
            update_doc["$addToSet"] = {"tags": {"$each": tags}}

        col.update_one({"_id": pub["_id"]}, update_doc)
        logger.info(f"Updated: {pub.get('title')} -> {categories}, tags: {tags}")

if __name__ == "__main__":
    logger.info("Starting classification...")
    classify_all_publications()
    logger.info("Classification completed.")
