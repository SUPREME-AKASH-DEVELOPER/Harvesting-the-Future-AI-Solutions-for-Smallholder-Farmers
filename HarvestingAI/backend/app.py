from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    query_en = GoogleTranslator(source='auto', target='en').translate(user_query)

    response = model.generate_content(f"Farmer's query: {query_en}. Provide simple agricultural solution:")
    answer_en = response.text
    answer_hi = GoogleTranslator(source='en', target='hi').translate(answer_en)

    return jsonify({"english": answer_en, "hindi": answer_hi})

if __name__ == '__main__':
    app.run(debug=True)
