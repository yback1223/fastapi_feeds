import requests

def get_video_pid(files: list):
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
	print(response.json())
	return response.json().get('id')


def fetch_video_result(pid: str):

	response = requests.request(
		"GET",
		f"https://api.stability.ai/v2beta/image-to-video/result/{pid}",
		headers={
			'accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
			'authorization': f"Bearer sk-hMqsP8aVsPnTfGag8vYXUo2yF6bgJMq8Rxvpf3RpSVCjjNc3"
		},
	)

	if response.status_code == 202:
		print("Generation in-progress, try again in 10 seconds.")
	elif response.status_code == 200:
		print("Generation complete!")
		with open("video.mp4", 'wb') as file:
			file.write(response.content)
	else:
		raise Exception(str(response.json()))