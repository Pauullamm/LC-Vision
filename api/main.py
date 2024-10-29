from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
from dotenv import load_dotenv
import redis
import logging
from utils import embed, query, convert

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PWD'), decode_responses=True)
app.config.from_object(__name__)

#api key and session processing
@app.route('/key', methods=['POST'])
def upload_key():
    try:
        api_key = request.form.get("input")
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
                image_data = file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8') # convert bytes to base64 string
                base64_images.append(base64_image)
            print("Image(s) received!")
        else:
            return jsonify({"message": "Please upload an image"})

        response = convert.image_to_text(api_key, base64_images)
        res = response.json()
        initial_query = res['choices'][0]['message']['content']
        openai_embed_query = embed.embed_query(query=initial_query, apikey=api_key, embed_model='text-embedding-3-large')
        # hf_query = embed.hf_embed(url=os.getenv('HF_MODEL_URL'), query=initial_query, apikey=os.getenv('HF_API_KEY')) # obtain embeddings using huggingface model + serverless inference api
        # pinecone_res = query.query_db(hf_query)
        pinecone_res = query.query_db(openai_embed_query)
        redis_client.flushall() # clear session data upon successful image processing
        return jsonify({ 'message': response.json(), 'interpretation': pinecone_res })
    except Exception as e:
        print(f"Error processing images: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
