import re

def extract_sql_query(input_string):
    # Regular expression to isolate the SQL query containing SELECT and FROM
    pattern = r"(?i)(SELECT\s+.*?\s+FROM\s+\w+;)"  # Matches 'SELECT', 'FROM', table name, case-insensitively
    match = re.search(pattern, input_string)
    if match:
        # print(f"This is match: {match}")
        return match.group(1).strip()  # Return the matched SQL query without extra text
    else:
        print(f"Invalid Query: {match}")
        return "No valid SQL query found."