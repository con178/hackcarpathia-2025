import requests
import pandas as pd
import json

api_key = "xxx"
address = "parafia królowej jadwigi rzeszów"

url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key})"

response = requests.get(url).json()
data = json.loads(response)
df = pd.json_normalize(data['results'])