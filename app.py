from flask import Flask, request, jsonify, render_template
from chatbot.llm import generate_response
from chatbot.retriever import retrieve_context
from chatbot.database import save_interaction  # Import from database.py

app = Flask(__name__)

# Route for the root URL
@app.route("/")
def home():
    return render_template("index.html")

# Route for the chatbot interaction
@app.route('/chat', methods=['GET','POST'])
def chat():
    try:
        user_input = request.json.get("What is AdventureWorks?")
        print('Try worked:',user_input)
    except:
        user_input = "What is AdventureWorks?"
        print("Try didn't work")
    context = retrieve_context(user_input)
    response = generate_response(user_input, context)
    # save_interaction(user_input, response)  # Save interaction to a file
    return jsonify({"response":response})

# Serve the favicon
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

if __name__ =="__main__":
    app.run(debug=True)