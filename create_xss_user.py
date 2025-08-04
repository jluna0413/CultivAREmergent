import requests

url = "http://localhost:4200/signup"
data = {
    "email": "<script>alert('XSS')</script>",
    "password": "test",
    "phone": ""
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
