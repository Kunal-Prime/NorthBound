import requests

url = "https://api.agify.io"
params = {"name": "alice"}

response = requests.get(url, params=params)


print("=" * 50)
print("STATUS CODE:")
print("=" * 50)
print(response.status_code)

print("\n" + "=" * 50)
print("RESPONSE HEADERS:")
print("=" * 50)
for key, value in response.headers.items():
    print(f"{key}: {value}") 
    
print("\n" + "=" *50)
print("RAE JSON BODY")
print("=" * 50)
print(response.json())

print("\n" + "=" * 50)
print("EXTRACTED DATA")
print("=" * 50)
data = response.json()
print(f"Name: {data['name']}")
print(f"Age : {data['age']}")
print(f"Count : {data['count']}people with this name ")