import requests

print("=" * 60)
print("EXPERIMENTING 1: INVALID URL")
print("=" * 60 )
try:
    r = requests.get("https://api.agify.io/WRONGPATH")
    print(f"Status : {r.status_code}")
    print(f"Body : {r.text}")
except Exception as e:
    print(f"An error occurred: {e}")


print("\n" + "=" * 60)
print("EXPERIMENTING 2: INVALID PARAMS")
print("=" * 60)
try:
    r = requests.get("https://api.agify.io/?name=")
    print(f"Status : {r.status_code}")
    print(f"Body : {r.json()}")
except Exception as e:
    print(f"An error occurred: {e}")


print("\n" + "=" * 60)
print("EXPERIMENTING 3:  COMPLETELY FAKE DOMAIN")
print("=" * 60)
try:
    r = requests.get("https://this-does-not-exist-xyz.com")
    print(f"Status : {r.status_code}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error caught!")
    print(f"Message : {e}")


print("\n" + "=" * 60)
print("EXPERIMENTING 4:  TIMEOUT (simulating no internet connection)")
print("=" * 60)
try:
    r = requests.get("https://api.agify.io/?name=alice", timeout=0.001)
    print(f"Status : {r.status_code}")
except requests.exceptions.Timeout :
    print("Timeout error caught! The request took too long to complete.")


"""
EXPERIMENT 1: What status code do you get? 404? 400? 500? 200?
EXPERIMENT 2: Does API return error in JSON or plain text? Does it return any error at all?
EXPERIMENT 3: What type of error fires? connection refused?
EXPERIMENT 4: What is the difference between a timeout error and a connection error?
"""
