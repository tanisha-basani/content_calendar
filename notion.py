import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 🔍 Get all items in the database
def get_database_entries():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch database:", response.text)
        return None

# ➕ Add a new content/idea item
def add_item(title, status="Idea", tags=[]):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Name": {
                "title": [
                    { "text": { "content": title } }
                ]
            },
            "Status": {
                "select": { "name": status }
            },
            "Tags": {
                "multi_select": [{ "name": tag } for tag in tags]
            }
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to add item:", response.text)
        return None
