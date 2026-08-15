import json
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

# Stage 1
conn = sqlite3.connect("Library Database.db")
checkouts_df = pd.read_sql_query("SELECT * FROM checkouts", conn)
members_df = pd.read_sql_query("SELECT * FROM members", conn)
books_db_df = pd.read_sql_query("SELECT * FROM books", conn)
conn.close()

with open("Book Catalog.json", "r", encoding="utf-8") as f:
    books_json_df = pd.DataFrame(json.load(f))

# Stage 2
borrows = checkouts_df.groupby("member_id").size().reset_index(name="member_total_borrows")
members_df = pd.merge(members_df, borrows, on="member_id", how="left")
members_df["member_total_borrows"] = members_df["member_total_borrows"].fillna(0).astype(int)

# Stage 3
stage1 = pd.merge(checkouts_df, members_df, on="member_id", how="left")
full_books = pd.merge(books_db_df, books_json_df, on="book_id", how="left")
combined_df = pd.merge(stage1, full_books, on="book_id", how="left")

# Stage 4
with open("Reading Kickoff Signups.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

html_data = []
for row in soup.find("table").find_all("tr")[1:]:
    cols = row.find_all("td")
    if len(cols) > 0:
        html_data.append({
            "member_id": int(cols[0].text.strip()),
            "book_id": int(cols[1].text.strip()),
            "checkout_date": cols[2].text.strip(),
            "return_date": None
        })

kickoff_df = pd.DataFrame(html_data)
last_id = checkouts_df["checkout_id"].max()
kickoff_df["checkout_id"] = range(last_id + 1, last_id + 1 + len(kickoff_df))

kickoff_df = pd.merge(kickoff_df, members_df, on="member_id", how="left")
kickoff_df = pd.merge(kickoff_df, full_books, on="book_id", how="left")

final_task1 = pd.concat([combined_df, kickoff_df], ignore_index=True)
final_task1.to_csv("EYOUTH-31103161200834-Library-task1_combined_data.csv", index=False)

# Stage 5
clean_df = final_task1.drop_duplicates().copy()

if "neighborhood" in clean_df.columns:
    clean_df["neighborhood"] = clean_df["neighborhood"].astype(str).str.strip().str.title()
    
if "membership_status" in clean_df.columns:
    clean_df["membership_status"] = clean_df["membership_status"].astype(str).str.strip().str.title()

clean_df.to_csv("EYOUTH-31103161200834-Library-task2_cleaned_data.csv", index=False)
print("All done! Files are saved.")