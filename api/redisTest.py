import redis
import os
from dotenv import load_dotenv
load_dotenv()


redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=12256, password=os.getenv("REDIS_PWD"), decode_responses=False)


def get_all_redis_data():
    all_data = {}  # Dictionary to store all data

    # Retrieve all keys in the database
    keys = redis_client.keys('*')  # Use '*' to match all keys
    print(f"Found {len(keys)} keys.")

    # Iterate over each key and fetch its value
    for key in keys:
        if redis_client.exists(key):  # Check if the key exists
            key_type = redis_client.type(key)  # Determine the type of each key
            print(f"Key: {key}, Type: {key_type}")

            if key_type == 'string':
                # Fetch and store string values
                value = redis_client.get(key)
                all_data[key] = value
                print(f"String Value: {value}")

        else:
            print(f"Key does not exist: {key}")

    return all_data

# Fetch all data and print
all_redis_data = get_all_redis_data()

for key, value in all_redis_data.items():
    
    print(f"Key: {key}, Value: {value.decode('latin-1')}")

# redis_client.flushall()
