import requests

resp = requests.get("https://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145")
print(resp.headers)