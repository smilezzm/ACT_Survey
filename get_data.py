import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect('survey_responses.db')

# Load the table into a DataFrame
df = pd.read_sql_query("SELECT * FROM responses", conn)

# Export to Excel
df.to_excel("responses_export.xlsx", index=False)

# Close the connection
conn.close()
