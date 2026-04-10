import pandas as pd
import numpy as np

path = "data/trends_clean.csv"

# ---- load file ----
try:
    data = pd.read_csv(path)
except Exception as e:
    print("could not read file:", e)
    exit()

print("Loaded data:", data.shape)

print("\nFirst 5 rows:")
print(data.head())


# ---- averages ----
avg_score = data["score"].mean()
avg_comments = data["num_comments"].mean()

print("\nAverage score   :", int(avg_score))
print("Average comments:", int(avg_comments))


# ---- numpy stuff ----
arr = data["score"].values

print("\n--- NumPy Stats ---")

print("Mean score   :", int(np.mean(arr)))
print("Median score :", int(np.median(arr)))
print("Std deviation:", int(np.std(arr)))
print("Max score    :", int(np.max(arr)))
print("Min score    :", int(np.min(arr)))


# which category has most stories
counts = data["category"].value_counts()

top_cat = counts.index[0]
top_count = counts.iloc[0]

print("\nMost stories in:", top_cat, "(", top_count, "stories)")


# most commented story
try:
    idx = data["num_comments"].idxmax()
    row = data.loc[idx]

    print("\nMost commented story:", row["title"], " —", int(row["num_comments"]), "comments")
except:
    print("\ncould not find most commented story")


# ---- new columns ----
data["engagement"] = data["num_comments"] / (data["score"] + 1)

data["is_popular"] = False
data.loc[data["score"] > avg_score, "is_popular"] = True


# ---- save ----
output = "data/trends_analysed.csv"

data.to_csv(output, index=False)

print("\nSaved to", output)