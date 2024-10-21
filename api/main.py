import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests
import os
from dotenv import load_dotenv
import redis
import logging
from utils import embed, query, retriever

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PWD'), decode_responses=True)
app.config.from_object(__name__)


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

#api key and session processing
@app.route('/key', methods=['POST'])
def upload_key():
    try:
        api_key = request.form.get("input")  # Safer way to get input
        if not api_key:
            return jsonify({"message": "Please input an OpenAI API key"}), 400

        session_id = request.form.get("sessionID")
        if session_id:
            # Set session to last for 1 hour
            redis_client.set(name=session_id, ex=3600, value=api_key)

            # Retrieve the API key from Redis
            stored_api_key = redis_client.get(session_id)
            
            # Check if stored_api_key is None
            if stored_api_key is None:
                return jsonify({"message": "API key could not be retrieved from Redis"}), 500

            return jsonify({"message": "API key received", 'text': stored_api_key}), 200  # Decode if necessary
        else:
            return jsonify({"message": "Session ID is missing"}), 400

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(request.form)
        return jsonify({'error': 'Internal server error: ' + str(e), 'text': redis_client.get(session_id)}), 500
#image processing

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        session_id = request.form['sessionID']
        api_key = redis_client.get(session_id) # obtain api_key which has been stored as a key value pair in redis (sessionID: api key)
        if api_key is None:
            return jsonify({"message": "Session expired or not found"}), 404
        logging.debug(f"retrieved API key: {api_key}")
        if "images" in request.files:
            files = request.files.getlist('images')
            base64_images = []
            for file in files:
                image_data = file.read() # read file as bytes
                base64_image = base64.b64encode(image_data).decode('utf-8') # convert bytes to base64 string
                base64_images.append(base64_image)
            outcome = "Image(s) received!"
            print(outcome)
        else:
            return jsonify({"message": "Please upload an image"})
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
                            "text": '''Describe the tablet(s) and/or capsule(s) in this image, and only the tablet(s) and/or capsule(s).
                                        Please format your answer based on the following:
                                        1. Colour: i.e. what colour(s) are the tablet(s)/capsule(s)
                                        2. Shape: i.e. what shape(s) are the tablet(s)/capsule(s)
                                        3. Markings: i.e. what markings are visible on the tablet(s)/capsule(s)
                                        4. Additional details:  for example - score lines, or how the markings/colours are printed on the tablet/capsule. If there are no additional details, answer with "NIL"
                                        5. Visibility: i.e. How well you are able to see the details on the tablet/capsule (respond with a float number between 0 to 10)
                                        If you are unable to see any of the above clearly, mention it in your response, don't try to guess what the ambiguous features are
                                        If there are no tablet(s)/capsule(s) in the image, respond with:
                                        "No tablet(s)/capsule(s) identified, please try again"
                                        '''
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

        # # Save image data and outcome to database
        # c.execute('''INSERT INTO images (image_data, outcome) 
        #           VALUES (?, ?)''', 
        #           (decoded_image, outcome))
        # conn.commit()
        res = response.json()
        print(res)
        initial_query = res['choices'][0]['message']['content']
        vectorised_query = embed.embed_query(initial_query, api_key, "text-embedding-3-large")
        pinecone_res = query.query_db(vectorised_query) # query pinecone vectorstore
        interpretation = retriever.generate_augmented_query(pinecone_res)
        redis_client.flushall() # clear session data upon successful image processing
        return jsonify({ 'message': response.json(), 'interpretation': interpretation })
    except Exception as e:
        print(f"Error processing images: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
