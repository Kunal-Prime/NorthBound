import requests

url = "https://api.exchangerate-api.com/v4/latest/INR"

response = requests.get(url)

print(f"status code : {response.status_code}")
print(f"headers : {dict(response.headers)}")

data = response.json()
print(f'\n ALL keys in response: {list(data.keys())}')


print(f"\nBase Currency : {data['base']}")  
print(f"Last Updated : {data['date']}")
print(f"total currencies : {len (data['rates'])}")

curriencies_i_want = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "THB", "SGD"]

print("\n INR Conversion Rates:")
print("-" * 30)
for currency in curriencies_i_want:
    rate = data["rates"][currency]
    print(f"1 INR = {rate:.6f} {currency}")