import json
import requests
import sys

if len(sys.argv) != 2:
    sys.exit()

response = requests.get("https://itunes.apple.com/search?enitity=song&limit=1&term=" + sys.argv[1])
print(json.dumps(response.json(), indent =2))

