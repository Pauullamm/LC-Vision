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