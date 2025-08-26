import requests

url = "http://localhost:5000/signup"
data = {
    "email": "<script>alert('XSS')</script>",
    "password": "test",
    "phone": ""
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
