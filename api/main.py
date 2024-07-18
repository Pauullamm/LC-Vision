import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import base64
import os
import requests

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('images.db')
c = conn.cursor()

# Database schema definition (executed only once)
c.execute('''CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_data TEXT,
            outcome TEXT,
            comment TEXT
)''')
conn.commit()


#image processing

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        api_key = request.json["input"]
        if not api_key:
            return jsonify({"message": "Please input an OpenAI API key"})
        files = request.files.getlist('images')
        base64_images = []
        for file in files:
            image_data = file.read() # read file as bytes
            base64_image = base64.b64encode(image_data).decode('utf-8') # convert bytes to base64 string
            base64_images.append(base64_image)
        outcome = "Image(s) received!"
        print(outcome)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
}
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe the tablet(s) in this image, and only the tablets"
                        }
                    ]
                }
            ],
            "max_tokens": 300
            }
        for image_data in base64_images:
            a = {
                "type": "image_url",
                "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                            }
            }
            payload["messages"][0]["content"].append(a)
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
        # img_info = response.json()["data"]["message"]["chioces"][0]["content"]
        # print(img_info)
        # # Save image data and outcome to database
        # c.execute('''INSERT INTO images (image_data, outcome) 
        #           VALUES (?, ?)''', 
        #           (decoded_image, outcome))
        # conn.commit()

        return jsonify({ 'message': response.json()})
    except Exception as e:
        print(f"Error processing images: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
