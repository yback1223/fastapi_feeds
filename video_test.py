import requests



# Define multiple files as a list of tuples
files = [
	('image', open("./1.png", "rb")),
	('image', open("./2.png", "rb")),
	('image', open("./3.png", "rb")),
	('image', open("./4.png", "rb")),
	('image', open("./5.png", "rb"))
]

response = requests.post(
	"https://api.stability.ai/v2beta/image-to-video",
	headers={
		"authorization": f"Bearer sk-hMqsP8aVsPnTfGag8vYXUo2yF6bgJMq8Rxvpf3RpSVCjjNc3"
	},
	files=files,
	data={
		"seed": 0,
		"cfg_scale": 1.8,
		"motion_bucket_id": 127
	},
)

print("Generation ID:", response.json().get('id'))
print(response.json())
