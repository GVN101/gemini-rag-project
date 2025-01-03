# import os
from flask import Flask, jsonify, request
from gemini_functions import process_query
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# List college JSON data paths 
colleges = [
    'college_json_data/cec.json', 
    'college_json_data/aec.json', 
    'college_json_data/mec.json',
    ]

@app.route("/get_data", methods=["POST"])
def get_response():
    try:
        # Expect JSON payload with 'question' key
        data = request.get_json()
        print(data) # for debugging purpose only
        
        user_question = data['question']
        # college = data.get('college',None)  To get the college from the frontend 
        response = process_query(user_question)
        print(response)
        
        return jsonify({
            "output": response.get('output_text', 'No response generated'),
            "image_urls": response.get('image_urls', "No Images"),
            "status": "success"
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route("/", methods=["GET"])
def  home_page():
    return "go to /get_data to get response"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)