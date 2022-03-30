# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import json

import requests

from credentials import app_id, app_key

language = 'en'
word_id = 'euphoria'
url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower()
# url Normalized frequency
urlFR = 'https://od-api.oxforddictionaries.com:443/api/v2/stats/frequency/word/' + language + '/?corpus=nmc&lemma=' + word_id.lower()
r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
print("code {}\n".format(r.status_code))
print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
