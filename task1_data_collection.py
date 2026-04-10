import requests
import time
import json
import os
from datetime import datetime

# API endpoints
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# categories + keywords
categories = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}

limit_per_category = 25


def find_category(title):
    title = title.lower()

    for cat in categories:
        words = categories[cat]

        for w in words:
            if w in title:
                return cat

    return None


# get top story ids
try:
    res = requests.get(top_url)
    ids = res.json()
except Exception as e:
    print("could not fetch top stories:", e)
    ids = []


all_data = []

for cat in categories:
    print("working on:", cat)
    count = 0

    for story_id in ids:

        if count == limit_per_category:
            break

        try:
            r = requests.get(item_url.format(story_id))
            story = r.json()
        except Exception as e:
            print("error fetching story", story_id)
            continue

        if not story:
            continue

        if "title" not in story:
            continue

        story_cat = find_category(story["title"])

        if story_cat != cat:
            continue

        row = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": cat,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        all_data.append(row)
        count += 1

    time.sleep(2)   # pause between categories


# save file
if not os.path.exists("data"):
    os.makedirs("data")

file_path = "data/trends_20240115.json"

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4)


print("done. total stories:", len(all_data))
print("saved here:", file_path)