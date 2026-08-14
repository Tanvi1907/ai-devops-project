from flask import Flask, jsonify, request
from google import genai
import os
import logging
import time
from dotenv import load_dotenv

# Configure logging - saves logs to a file called app.log
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load API key from .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "AI DevOps project is running!"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/greet/<name>')
def greet(name):
    if not name.strip():
        return jsonify({"error": "Name cannot be empty"}), 400
    return jsonify({"message": f"Hello, {name}! Welcome to the DevOps project."}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "This route does not exist"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Something went wrong on the server"}), 500

# Helper function: calls Gemini AI with automatic retry on failure
def call_ai_with_retry(prompt, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text
        except Exception as e:
            logging.warning(f"AI call attempt {attempt} failed: {str(e)}")
            if attempt < max_retries:
                time.sleep(2)  # wait 2 seconds before retrying
            else:
                raise e  # if all retries fail, raise the error

# Route to analyze error logs using AI
@app.route('/analyze-error', methods=['POST'])
def analyze_error():
    data = request.get_json()

    if not data or 'error_log' not in data:
        logging.warning("Request received without error_log")
        return jsonify({"error": "Please provide 'error_log' in request body"}), 400

    error_log = data['error_log']
    logging.info(f"Analyzing error: {error_log}")

    try:
        prompt = f"You are a DevOps expert. Analyze this error log and explain the likely cause and a fix in 3-4 short sentences:\n\n{error_log}"
        ai_result = call_ai_with_retry(prompt)

        logging.info("AI analysis successful")
        return jsonify({
            "original_error": error_log,
            "ai_analysis": ai_result
        }), 200

    except Exception as e:
        logging.error(f"AI analysis failed after retries: {str(e)}")
        return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)