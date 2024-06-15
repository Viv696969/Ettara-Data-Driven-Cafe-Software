
'''
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
'''

import requests

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = int(query({
	"inputs": "the place was not the best but was good"
})[0][0]['label'].split()[0])
print(output)

