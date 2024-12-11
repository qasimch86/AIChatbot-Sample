import re

def parse_input(user_input):
    """Parse user input to extract conditions."""
    # Example: User input might be something like:
    # "Find products where name contains 'ball' and price is greater than 100"

    # Regex to identify conditions like column=value or column operator value
    conditions = []

    # Find "column OPERATOR value" patterns in the user input
    patterns = [
        r"(\w+)\s*(<=|>=|<|>|=)\s*(['\w\s]+)",  # e.g., Name LIKE 'ball' or Price > 100
        r"(\w+)\s*LIKE\s*(['\w\s]+)"  # e.g., Name LIKE 'ball'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, user_input)
        for match in matches:
            column, operator, value = match
            conditions.append((column, operator, value.strip("'")))

    return conditions
