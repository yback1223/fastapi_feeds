import requests

response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
    headers={
        "authorization": f"Bearer sk-hMqsP8aVsPnTfGag8vYXUo2yF6bgJMq8Rxvpf3RpSVCjjNc3",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "The woman of glamor.",
        "output_format": "png",
    },
)

if response.status_code == 200:
    with open("./5.png", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))