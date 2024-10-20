from flask import Flask, render_template, request, jsonify
import cohere
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load your Cohere API key from the environment variable
co = cohere.Client(os.getenv("COHERE_API_KEY"))

@app.route('/')
def home():
    return render_template('view.html')

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    
    try:
        # Send the message to Cohere's API and receive the response
        response = co.chat(
        message=message,
        model="command",
        temperature=0.3
    )

        # Extract the response content
        response_message = response.text
        return jsonify({"response": response_message})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Failed to generate response!"}), 500


if __name__ == '__main__':
    app.run(debug=True)
