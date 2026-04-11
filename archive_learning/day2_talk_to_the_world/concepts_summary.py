import requests

# CONCEPT 1 : params vs manually building url
# bad (fragile):
url_bad = "https://api.agify.io?name=alice&extra=123"

# good (requests handle encoding for you, less error prone):
url_good = "https://api.agify.io"
params = {"name": "alice", "extra": "123"}
r = requests.get(url_good, params=params)
print(r.url)  # see how requests builds the url for you

# CONCEPT 2 : reponse.text vs response.json()
r = requests.get("https://api.agify.io?name=alice")
print(type(r.text))  # <class 'str'> raw string response
print(type(r.json()))  # <class 'dict'> python dict

# CONCEPT 3 : eaise_for_status
# instead of checking status code manually:
if r.status_code != 200:
    print("ERROR")

# USE THIS (cleaner):
try:
    r.raise_for_status()
    #only  runs if 200-299
except requests.exceptions.HTTPError as e:
    print(f"HTTP ERROR: {e}")   

# CONCEPT 4 : EXCEPTION HIRARCHY
"""
requests.exceptions.RequestException   ← catches ALL below
    ├── ConnectionError                 ← no internet, DNS fail
    ├── Timeout                         ← server too slow
    ├── HTTPError                       ← 4xx, 5xx status codes
    └── TooManyRedirects                ← redirect loop
"""