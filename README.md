# all-the-beers

Python script to bulk download brewery data from the [Open Brewery DB](https://www.openbrewerydb.org/) API.

## About Open Brewery DB

Open Brewery DB is a free, open-source dataset and API with public information on breweries, cideries, brewpubs, and bottleshops worldwide. No API key or authentication required.

## Requirements

- Python 3.7+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mchamps/all-the-beers.git
   cd all-the-beers
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Fetch all breweries

```bash
python breweries.py
```

This downloads all breweries from Open Brewery DB.

**Options:**
- `-o, --output FILE` - Specify output file (default: `breweries.json`)
- `--country COUNTRY` - Filter by country (e.g., "United States", "Ireland")
- `--state STATE` - Filter by state/province (e.g., "California", "New York")
- `--city CITY` - Filter by city (e.g., "San Diego", "Portland")
- `--type TYPE` - Filter by brewery type

**Brewery Types:**
- `micro` - Most craft breweries
- `nano` - Extremely small breweries
- `regional` - Regional location of an expanded brewery
- `brewpub` - Brewery with restaurant/bar on-premise
- `large` - Large national/international breweries
- `planning` - Brewery in planning (not yet opened)
- `bar` - Bar without brewing equipment
- `contract` - Brews under contract for another brewery
- `proprietor` - Similar to brewpub but focuses on a restaurant
- `closed` - Closed locations

**Examples:**
```bash
# Fetch all breweries worldwide
python breweries.py

# Fetch only US breweries
python breweries.py --country "United States"

# Fetch California breweries only
python breweries.py --country "United States" --state "California"

# Fetch only microbreweries in Portland
python breweries.py --city "Portland" --type micro

# Save to custom file
python breweries.py -o us_breweries.json --country "United States"
```

## Output Format

The script outputs a flat JSON array. Example brewery object:

```json
[
  {
    "id": "5128df48-79fc-4f0f-8b52-d06be54d0cec",
    "name": "10-56 Brewing Company",
    "brewery_type": "micro",
    "address_1": "400 Brown Cir",
    "address_2": null,
    "address_3": null,
    "city": "Knox",
    "state_province": "Indiana",
    "postal_code": "46534",
    "country": "United States",
    "longitude": "-86.627954",
    "latitude": "41.289715",
    "phone": "6308165790",
    "website_url": null,
    "state": "Indiana",
    "street": "400 Brown Cir"
  }
]
```

## Features

- **No API key required** - Open Brewery DB is free and open
- **Rate limiting** - Built-in delays between requests to be respectful
- **Automatic retry** - Failed requests are retried up to 3 times with exponential backoff
- **Error handling** - Network errors are caught gracefully with partial data saved
- **Progress reporting** - Real-time progress displayed during download
- **Flexible filtering** - Filter by country, state, city, or brewery type

## API Documentation

For more information about the Open Brewery DB API:
- Website: https://www.openbrewerydb.org/
- Documentation: https://www.openbrewerydb.org/documentation
- GitHub: https://github.com/openbrewerydb

## License

MIT
