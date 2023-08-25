import requests

# Replace 'your_access_token' with the actual access token you obtained
access_token = 'your_access_token'

headers = {
    'Authorization': f'Bearer {access_token}'
}

body = {
    
}
response = requests.get('http://localhost:8000/login_sessions', headers=headers)
print(response.json())
