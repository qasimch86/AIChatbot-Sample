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
    context = retrieve_context(collection_name,user_input)

    # Check if context is empty.
    if context is None:
        return jsonify({"response": "Context not found."})
    
    # Generate a response based on user input and context
    response = generate_response(user_input, context)
    
    # save_interaction(user_input, response)  # Save interaction to a file
    return jsonify({"response":response})

def get_collection_name_based_on_input(user_input):
    """Map user input to a corresponding collection name."""
    # Example mapping (this could be based on keywords, etc.)
    if "product" in user_input.lower():
        return "adventureworks_products"
    elif "sales" in user_input.lower():
        return "adventureworks_sales"
    else:
        return "default_collection"

# Serve the favicon
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ =="__main__":
    app.run(debug=True)