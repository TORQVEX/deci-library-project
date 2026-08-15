import sqlite3

conn = sqlite3.connect("Library Database.db")
cursor = conn.cursor()

queries = [
    (
        "Question 1: Checkouts per member",
        "Reasoning: We group the checkouts table by member_id and use COUNT() to find the total borrows for each member, then sort the results descending to see the highest borrowers first.",
        """
        SELECT member_id, COUNT(*) AS total_checkouts
        FROM checkouts
        GROUP BY member_id
        ORDER BY total_checkouts DESC;
        """
    ),
    (
        "Question 2: Books by author pattern",
        "Reasoning: We use the LIKE operator with wildcards (%) to find books where the author's name contains either 'Smith' or 'John', and then sort them alphabetically by title.",
        """
        SELECT book_id, title, author
        FROM books
        WHERE author LIKE '%Smith%' OR author LIKE '%John%'
        ORDER BY title ASC;
        """
    ),
    (
        "Question 3: Top 5 most frequently borrowed books",
        "Reasoning: We join the books table with the checkouts table on book_id to associate checkouts with titles. We then group by book_id, count the checkouts, order descending, and apply a LIMIT of 5 to get the most popular ones.",
        """
        SELECT b.book_id, b.title, COUNT(c.checkout_id) AS borrow_count
        FROM books b
        JOIN checkouts c ON b.book_id = c.book_id
        GROUP BY b.book_id, b.title
        ORDER BY borrow_count DESC
        LIMIT 5;
        """
    ),
    (
        "Question 4: Top 10 members with the most borrowed books",
        "Reasoning: We join the members and checkouts tables on member_id. We group by member_id and name, count total borrows, order them from highest to lowest, and apply a LIMIT of 10 to find the most active readers.",
        """
        SELECT m.member_id, COUNT(c.checkout_id) AS total_borrows
        FROM members m
        JOIN checkouts c ON m.member_id = c.member_id
        GROUP BY m.member_id
        ORDER BY total_borrows DESC
        LIMIT 10;
        """
    ),
    (
        "Question 5: Neighborhood checkouts (looking past the ten most recent)",
        "Reasoning: We join members and checkouts to connect checkouts to neighborhoods. We group by neighborhood, count the checkouts, order descending, and use LIMIT 10 OFFSET 10 to skip the first 10 rows and retrieve the next batch.",
        """
        SELECT m.neighborhood, COUNT(c.checkout_id) AS neighborhood_checkouts
        FROM members m
        JOIN checkouts c ON m.member_id = c.member_id
        GROUP BY m.neighborhood
        ORDER BY neighborhood_checkouts DESC
        LIMIT 10 OFFSET 10;
        """
    ),
]

output_filename = "EYOUTH-31103161200834-Library-task1_sql_answers.txt"

with open(output_filename, "w", encoding="utf-8") as f:
    f.write("=== TASK 1: SQL QUERIES AND ANALYSIS ===\n\n")

    for title, reasoning, sql in queries:
        f.write(f"--- {title} ---\n")
        f.write(f"Reasoning:\n{reasoning}\n\n")
        f.write(f"SQL Query:\n{sql.strip()}\n\nResults:\n")
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            if not rows:
                f.write("No results found.\n")
            for row in rows:
                f.write(f"{row}\n")
        except Exception as e:
            f.write(f"Error executing query: {e}\n")
        f.write("\n" + "=" * 50 + "\n\n")

    reflection = """=== WEB PAGE VS. API INTEGRATION REFLECTION ===

The Reading Kickoff data lived on a web page, which changes how we interact with it compared to a database or API. 

1. Web Page Scraping: A web page is built for a person's browser, meaning the data is wrapped in visual HTML tags (like <table> or <tr>). To get the data, we have to write a parser (like BeautifulSoup) to strip away the visual elements. This is fragile because if the website owner changes the design or layout, the parser will break.

2. API/Database Integration: An API or direct database connection is built to hand data directly to a program in a structured, predictable form (like JSON or direct SQL tables). It is reliable, does not care about visual design, and gives us exactly the data types we request.

Why it matters for this project: Working with the Reading Kickoff HTML required us to manually navigate rows and clean text strings, whereas the SQLite database simply allowed us to query exact columns securely. Combining them meant standardizing the messy web data to match the strict structure of our database.
"""

    f.write(reflection)

conn.close()
print(f"Generated {output_filename} successfully.")