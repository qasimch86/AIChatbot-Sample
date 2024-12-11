from flask import Flask, request, jsonify, render_template
from chatbot.llm.llm import generate_response
from chatbot.retrieval.retriever import retrieve_context

app = Flask(__name__)

# Route for the root URL
@app.route("/")
def home():
    return render_template("index.html", response='')

# Route for the chatbot interaction
@app.route('/chat', methods=['GET','POST'])
def chat():
    # try:
    #     user_input = request.json.get("What is AdventureWorks?")
    #     print('Try worked:',user_input)
    # except:
    #     user_input = "What is AdventureWorks?"
    #     print("Try didn't work")

    user_input = request.form.get('input')
    print(f"User input: {user_input}")

    # Define collection name
    collection_name = get_collection_name_based_on_input(user_input)

    # Retrieve context from the vector database
    context = retrieve_context(user_input)

    # Check if context is empty.
    if context is None:
        return jsonify({"response": "Context not found."})
    
    # Generate a response based on user input and context
    response = generate_response(user_input, context)
    
    # save_interaction(user_input, response)  # Save interaction to a file
    return jsonify({"response":response})

def get_collection_name_based_on_input(user_input):
    """Map user input to a corresponding collection name based on keywords."""
    
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

# Serve the favicon
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ =="__main__":
    app.run(debug=True)