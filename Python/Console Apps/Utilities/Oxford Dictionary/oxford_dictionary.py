import requests
import json
app_id = "<your_app_id>"
app_key = "<your_app_key>"
language = "en-gb"
word_id = input("Enter search word: ")
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
print("code {}\n".format(r.status_code))
print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
