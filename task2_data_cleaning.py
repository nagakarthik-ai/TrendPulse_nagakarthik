import pandas as pd
import json

# change this if your file name is different
file = "data/trends_20240115.json"


# -------- load data --------
try:
    f = open(file, "r", encoding="utf-8")
    raw = json.load(f)
    f.close()
except Exception as e:
    print("problem reading file:", e)
    exit()

df = pd.DataFrame(raw)
print("Loaded", len(df), "stories from", file)


# -------- cleaning --------

# duplicates
before = len(df)
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# missing values
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# fix types (just in case)
try:
    df["score"] = df["score"].astype(int)
except:
    pass

# num_comments might have nulls
df["num_comments"] = df["num_comments"].fillna(0)

try:
    df["num_comments"] = df["num_comments"].astype(int)
except:
    pass

# remove low score
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# clean titles
df["title"] = df["title"].str.strip()


# -------- save --------
out = "data/trends_clean.csv"
df.to_csv(out, index=False)

print("\nSaved", len(df), "rows to", out)


# -------- summary --------
print("\nStories per category:")

counts = df["category"].value_counts()

for c in counts.index:
    print(" ", c, " ", counts[c])