import pytest
import requests
import json
import base64

BASE_URL = "http://localhost:7071/api"

@pytest.fixture(scope="module")
def base64_image():
	with open("tests/data/example_essay.jpg", "rb") as image_file:
		return base64.b64encode(image_file.read()).decode('utf-8')

def test_analyze_images_post(base64_image):
	url = f"{BASE_URL}/analyzeImages"
	headers = {"Content-Type": "application/json"}
	payload = json.dumps({"images": [f"data:image/jpeg;base64,{base64_image}"]})
	response = requests.post(url, headers=headers, data=payload)
	assert response.status_code == 200


	