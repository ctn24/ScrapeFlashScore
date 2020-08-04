# import json library
import urllib.request
import json
# request url
urlreq = 'https://groceries.asda.com/api/items/search?keyword=yogurt'
# get response
response = urllib.request.urlopen(urlreq)
# load as json
jresponse = json.load(response)
# write to file as pretty print
with open('asdaresp.json', 'w') as outfile:
    json.dump(jresponse, outfile, sort_keys=True, indent=4)
print(jresponse)