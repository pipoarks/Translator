import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from langchain_community.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize the OpenAI API model and key
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MODEL_API_KEY = os.getenv("OPENAI_MODEL_API_KEY")

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes, allowing only requests from 'https://nihongotranslator.com'
CORS(app, origins=["https://nihongotranslator.com"])

# Initialize the ChatOpenAI model
llm = ChatOpenAI(model_name=OPENAI_MODEL, openai_api_key=OPENAI_MODEL_API_KEY)

@app.route('/translate', methods=['POST'])
def translate():
    # Parse JSON input
    data = request.json
    user_input = data.get('text', '')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Construct the prompt
    prompt = f"Translate the given Romaji '{user_input}' into a single Japanese word. Only provide the Japanese word without any explanations."

    # Get the AI response
    result = llm.invoke(prompt)

    # Extract text content (assuming `result.content` holds the response text)
    if hasattr(result, 'content'):
        response_text = result.content
    else:
        response_text = str(result)  # Fallback in case content attribute does not exist

    # Return the AI response as JSON
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)