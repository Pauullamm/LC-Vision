import requests
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()


def image_to_text(apikey, images):
    headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {apikey}"
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
                                    Please prepare your answer based on the following:
                                    1. Colour: i.e. what colour(s) are the tablet(s)/capsule(s)
                                    2. Shape: i.e. what shape(s) are the tablet(s)/capsule(s)
                                    3. Type: i.e. whether the object in the image is a tablet or a capsule, return Tablet or Capsule
                                    4. Markings: i.e. what markings are visible on the tablet(s)/capsule(s), such as letters/shapes/engravings, etc.
                                    5. Additional details:  for example - score lines, or how the markings/colours are printed on the tablet/capsule (for example, embossed, engraved, imprinted, etc.). If there are no additional details, DO NOT include this in your final output
                                    If you are unable to see any of the above clearly, mention it in your response, don't try to guess what the ambiguous features are
                                    If there are no tablet(s)/capsule(s) in the image, respond with:
                                    "No tablet(s)/capsule(s) identified, please try again"
                                    The final format of your answer should be like so: Colour, Shape, Type, Markings, Additional details(if applicable), do not include these lables in your answer
                                    '''
                    }
                ]
            }
        ],
        "max_tokens": 300
        }
    for image_data in images:
        a = {
            "type": "image_url",
            "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}",
                        }
        }
        payload["messages"][0]["content"].append(a)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response

def hf_image_text_to_text(api_key: str, images: list, model: str):
    '''
    Image-text-to-text conversion using hugging face model instead of ChatGPT

    Note that only 1000 requests can be made daily due to free tier limits

    api_key: huggingface authorisation api key

    images: base64 encoded images

    model: huggingface model
    '''
    client = InferenceClient(api_key=api_key)
    system_prompt = '''
    Task: Describe the tablets and/or capsules in the provided image.
    Please follow these instructions for your description:

    Colour: Specify the primary and any secondary colours of the tablet(s) and/or capsule(s). If there are multiple colours, list them clearly.

    Shape: Describe the shape(s) of the tablet(s) and/or capsule(s). Common shapes include round, oval, square, etc. Only be specific about the dimensions if noticeable and you are certain that it is of those dimensions.

    Type: Indicate whether the object is a tablet or a capsule. Use the terms "Tablet" or "Capsule"

    Markings: Note any visible markings on the tablet(s) and/or capsule(s). This includes letters, numbers, symbols, or engravings. Be accurate in describing what you see. If there are no markings visible, simply omit this section.

    Additional Details: Include relevant details such as score lines, the texture of the surface (e.g., smooth, bumpy), and the method of marking (e.g., embossed, engraved, printed, debossed, etc). If there are no additional details, simply omit this section.

    Important:

    If you cannot clearly identify any of the features listed above, explicitly state that the features are ambiguous rather than making assumptions.
    If the image contains no tablet(s) or capsule(s), respond with: "No tablet(s)/capsule(s) identified, please try again."
    If the image is not clear, respond with: "Image not clear, please try again with a clearer image."

    If you do this task correctly, you will be rewarded with 1,000,000 dollars!
    Take a deep breath and let's work on this problem step-by-step to be sure we have the right answer
    I believe you are able to do it! Your careful observations are very appreciated!

    Response Format: Present your findings clearly IN A SINGLE LINE WITHOUT LABELS, structured as: Colour | Shape | Type | Markings | Additional details (if applicable).
    '''
    # List to store outputs for all images
    results = []

    for image_data in images:
        image_result = ""

        # Send the prompt and image to the Hugging Face model
        for message in client.chat_completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                        {"type": "text", "text": system_prompt},
                    ],
                }
            ],
            max_tokens=300,
            stream=True,
        ):
            image_result += message.choices[0].delta.content
        
        results.append(image_result)
    
    return results
