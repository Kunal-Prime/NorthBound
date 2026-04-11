import requests

url = "https://official-joke-api.appspot.com/random_joke"

response = requests.get(url)

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers['Content-Type']}")
print(f"Raw JSON : {response.json()}")


joke = response.json()

print("\n" + "🎭" * 20)
print(f"Type : {joke['type']}")
print(f"Setup : {joke['setup']}")
print(f"Punchline : {joke['punchline']}")
print("🎭" * 20)
