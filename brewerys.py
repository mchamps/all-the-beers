import requests
import json

r_brewerys = requests.get("http://api.brewerydb.com/v2/locations?key=API_KEY_HERE&p=1").json()
num_pages = r_brewerys['numberOfPages']
current_page = r_brewerys['currentPage']

data = r_brewerys['data']
numberOfItems = r_brewerys['totalResults']

#uncomment the next line for testing purposes
#for current_page in range(1, 4):
for current_page in range(1, num_pages): 
    r_brewerys = requests.get("http://api.brewerydb.com/v2/locations?key=API_KEY_HERE&p=" + str(current_page)).json()
    print current_page

data.append(r_brewerys['data'])

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
