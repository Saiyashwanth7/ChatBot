from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('view.html')


# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    
    try:
        # Send the message to OpenAI's API and receive the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        # Extract the response content
        response_message = response['choices'][0]['message']['content']
        return jsonify({"response": response_message})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Failed to generate response!"}), 500


if __name__ == '__main__':
    app.run(debug=True)
