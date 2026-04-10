import pandas as pd
import matplotlib.pyplot as plt
import os

path = "data/trends_analysed.csv"

# --- load ---
try:
    data = pd.read_csv(path)
except Exception as e:
    print("could not load file:", e)
    exit()

# make output folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")


# --- top 10 stories ---
top = data.sort_values("score", ascending=False).head(10)

names = []
for t in top["title"]:
    if len(t) > 50:
        names.append(t[:50] + "...")
    else:
        names.append(t)

plt.figure()
plt.barh(names, top["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Stories")

plt.savefig("outputs/chart1_top_stories.png")


# --- categories ---
cat = data["category"].value_counts()

plt.figure()
plt.bar(cat.index, cat.values)
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")

plt.savefig("outputs/chart2_categories.png")


# --- scatter plot ---
p1 = data[data["is_popular"] == True]
p2 = data[data["is_popular"] == False]

plt.figure()

plt.scatter(p1["score"], p1["num_comments"], label="popular")
plt.scatter(p2["score"], p2["num_comments"], label="others")

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")


# --- dashboard ---
fig, ax = plt.subplots(1, 3, figsize=(14, 4))

# left
ax[0].barh(names, top["score"])
ax[0].set_title("Top Stories")

# middle
ax[1].bar(cat.index, cat.values)
ax[1].set_title("Categories")

# right
ax[2].scatter(p1["score"], p1["num_comments"], label="pop")
ax[2].scatter(p2["score"], p2["num_comments"], label="other")
ax[2].set_title("Score vs Comments")

fig.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")


print("done. check outputs folder")