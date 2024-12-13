
# Fill missing data with N/A in the sql results
def fill_missing_fields(sql_results):
    """
    Replace missing fields (e.g., None or missing columns) in SQL results with 'N/A'.
    
    Parameters:
        sql_results (list of tuples): The list of rows retrieved from the database.
    
    Returns:
        list of tuples: Updated rows with missing fields replaced with 'N/A'.
    """
    if not sql_results:
        return []

    # Iterate over each row and replace missing values with 'N/A'
    updated_rows = []
    for row in sql_results:
        updated_row = tuple(
            value if value is not None else 'N/A' for value in row
        )
        updated_rows.append(updated_row)
    
    return updated_rows


# Get the collection name based on the user input
def get_collection_name_based_on_input(user_input):
    """Map user input to a corresponding collection name based on keywords."""
    print(user_input)
    if user_input:
        user_input = '0';
    # Convert input to lowercase for case-insensitive matching
    user_input_lower = user_input.lower()
    # Define more sophisticated mappings for collection names
    if "product" in user_input_lower or "item" in user_input_lower:
        return "adventureworks_products"
    elif "sales" in user_input_lower or "revenue" in user_input_lower:
        return "adventureworks_sales"
    elif "order" in user_input_lower or "purchase" in user_input_lower:
        return "adventureworks_orders"
    elif "customer" in user_input_lower or "client" in user_input_lower:
        return "adventureworks_customers"
    elif "inventory" in user_input_lower or "stock" in user_input_lower:
        return "adventureworks_inventory"
    else:
        return "default_collection"  # Fallback to default if no match is found