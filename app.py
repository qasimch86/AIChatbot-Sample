from flask import Flask, request, render_template
from chatbot.llm.llm import generate_response_llm
from chatbot.retrieval.retriever import retrieve_context
from data.load_csv import load_schema_from_csv
from functions import fill_missing_fields, get_collection_name_based_on_input
from chatbot.config import Config

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# Route to serve the chat UI page (chatui.html)
@app.route("/chat") # Set the route for the chat UI page
def chatui():
    return render_template('chatui.html')

# Combined route for handling both GET and POST requests
@app.route("/", methods=['GET', 'POST'])
def chat():
    user_input = ''
    response_llm = ''
    final_sql_results = []
    if request.method == 'POST':
        user_input = request.form.get('input')
        Config.llm_provider = request.form.get('llm_provider')  # Get the selected LLM provider
        print(f"User input: {user_input}")
        print(f"LLM Provider: {Config.llm_provider}")
        # Define collection name
        collection_name = get_collection_name_based_on_input(user_input)

        # Load schema (assuming CSV or other schema source)
        schema = load_schema_from_csv('./data/schema_testdb3.csv')
        # Retrieve context from the vector database
        sql_results = retrieve_context(user_input, schema)

        # Fill missing values with N/A
        final_sql_results = fill_missing_fields(sql_results)
        print(f"\n\n\n\n This is final_sql_results\n\n{final_sql_results}\n\n\n\n")

        # Check if context is empty
        if final_sql_results is None or len(final_sql_results) == 0:
            response_llm = "Query not found.\nMake sure you have previledge to retrieve data from this table."
        else:
            # Generate a response based on user input and context
            response_llm = generate_response_llm(user_input, final_sql_results, schema)

    # Render the template, passing the variables to the HTML
    return render_template("index.html", user_input=user_input, response_llm=response_llm, final_sql_results=final_sql_results)

# Serve the favicon
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
