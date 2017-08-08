import requests
import json

r_beers = requests.get("http://api.brewerydb.com/v2/beers?key=API_KEY_HERE&withBreweries=Y&withIngredients=Y").json()
num_pages = r_beers['numberOfPages']

data = r_beers['data']
numberOfItems = r_beers['totalResults']

for page in range(2, num_pages+1):
#for page in range(2, 4):
    r_beers = requests.get("http://api.brewerydb.com/v2/beers?key=API_KEY_HERE&withBreweries=Y&withIngredients=Y", params={'currentPage': page}).json()
    data.append(r_beers['data'])

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)