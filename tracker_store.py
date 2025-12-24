import json
import os

FILE = "tracked_items.json"

def load_items():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_items(items):
    with open(FILE, "w") as f:
        json.dump(items, f, indent=2)

def add_item(url, size):
    items = load_items()

    for item in items:
        if item["url"] == url:
            if size not in item["sizes"]:
                item["sizes"].append(size)
            save_items(items)
            return

    items.append({
        "url": url,
        "sizes": [size]
    })
    save_items(items)
