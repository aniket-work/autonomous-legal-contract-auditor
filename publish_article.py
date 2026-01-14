import requests
import os
import json
import re

API_URL = "https://dev.to/api/articles"
ENV_PATH = "../.env"
ARTICLE_PATH = "generated_article.md"

def get_api_key():
    try:
        with open(ENV_PATH, "r") as f:
            for line in f:
                if line.strip().startswith("DEVTO_API_KEY"):
                    return line.strip().split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        print(f"Error: {ENV_PATH} not found.")
        return None
    return None

def parse_article(path):
    with open(path, "r") as f:
        content = f.read()
    
    # Simple frontmatter parser
    frontmatter_match = re.match(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not frontmatter_match:
        print("Error: Could not parse frontmatter.")
        return None, None
    
    fm_text = frontmatter_match.group(1)
    body = frontmatter_match.group(2)
    
    metadata = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    
    return metadata, body

def main():
    api_key = get_api_key()
    if not api_key:
        print("Failed to find API Key.")
        return

    metadata, body = parse_article(ARTICLE_PATH)
    if not metadata:
        return

    # Parse tags
    tags = [t.strip() for t in metadata.get("tags", "").split(",") if t.strip()]

    payload = {
        "article": {
            "title": metadata.get("title"),
            "body_markdown": body,
            "published": True,
            "tags": tags[:4]
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    print(f"Publishing '{metadata.get('title')}'...")
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code in [200, 201]:
        data = response.json()
        print("Success!")
        print(f"URL: {data['url']}")
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
