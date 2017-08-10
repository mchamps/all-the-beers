import requests
import json

r_beers = requests.get("http://api.brewerydb.com/v2/beers?key=API_KEY_HERE&withBreweries=Y&p=").json()
num_pages = r_beers['numberOfPages']
current_page = r_beers['currentPage']

data = r_beers['data']
numberOfItems = r_beers['totalResults']

#uncomment the next line for testing purposes
#for current_page in range(1, 10 + 1):
for current_page in range(1, num_pages + 1): 
    r_beers = requests.get("http://api.brewerydb.com/v2/beers?key=API_KEY_HERE&withBreweries=Y&p=" + str(current_page)).json()
    data.append(r_beers['data'])
    print str(current_page) + " of " + str(num_pages) 

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)