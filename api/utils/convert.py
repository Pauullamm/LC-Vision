import requests

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