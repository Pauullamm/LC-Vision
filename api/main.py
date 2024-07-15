import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import base64
import os
from openai import OpenAI

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
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

@app.route('/upload', methods=['POST'], strict_slashes=False)
def upload_image():
    try:
        files = request.files.getlist('images')
        cache = []
        base64_images = []
        for file in files:
            image_data = file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            base64_images.append(base64_image)
        with open("output_image.jpg", "wb") as f:
            f.write(base64_images[0])
        cache.append(base64_images[0])
        outcome = "Image processed successfully!"
        print(outcome)
        params =[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe these pills in as much detail as possible. Give information on the shape, any markings, the colour, any score lines, the finishes",
                            }
                        ]
                    }
                ]
        for image_data in cache:
            a = {
                "type": "image",
                "image": image_data
            }
            params[0]["content"].append(a)
        response = client.chat.completions.create(model="gpt-4o", messages=params, max_tokens=300)
        img_info = response["choices"][0]["message"]["content"]
        print(img_info)
        # # Save image data and outcome to database
        # c.execute('''INSERT INTO images (image_data, outcome) 
        #           VALUES (?, ?)''', 
        #           (decoded_image, outcome))
        # conn.commit()

        return jsonify({'message': outcome})
    except Exception as e:
        print(f"Error processing images: {e}")
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
