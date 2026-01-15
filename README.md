# all-the-beers

Python scripts to bulk download beer and brewery data from the [BreweryDB](https://www.brewerydb.com/) API.

## Requirements

- Python 3.7+
- BreweryDB premium account API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/all-the-beers.git
   cd all-the-beers
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your BreweryDB API key as an environment variable:
   ```bash
   # Linux/Mac
   export BREWERYDB_API_KEY='your_api_key_here'

   # Windows (Command Prompt)
   set BREWERYDB_API_KEY=your_api_key_here

   # Windows (PowerShell)
   $env:BREWERYDB_API_KEY='your_api_key_here'
   ```

## Usage

### Fetch all beers

```bash
python beers.py
```

This downloads all beers from BreweryDB including brewery and ingredient data.

**Options:**
- `-o, --output FILE` - Specify output file (default: `beers.json`)
- `--no-breweries` - Exclude brewery data
- `--no-ingredients` - Exclude ingredient data

**Examples:**
```bash
# Save to custom file
python beers.py -o my_beers.json

# Fetch beers without ingredient data
python beers.py --no-ingredients
```

### Fetch all brewery locations

```bash
python brewerys.py
```

This downloads all brewery location data from BreweryDB.

**Options:**
- `-o, --output FILE` - Specify output file (default: `brewerys.json`)

**Examples:**
```bash
# Save to custom file
python brewerys.py -o locations.json
```

## Output Format

Both scripts output a flat JSON array. Example beer object:

```json
[
  {
    "id": "abc123",
    "name": "Example IPA",
    "description": "A hoppy India Pale Ale",
    "abv": "6.5",
    "ibu": "65",
    "breweries": [...],
    "ingredients": [...]
  },
  ...
]
```

## Features

- **Rate limiting** - Built-in delays between requests to respect API limits
- **Automatic retry** - Failed requests are retried up to 3 times with exponential backoff
- **Error handling** - Network errors are caught gracefully with partial data saved
- **Progress reporting** - Real-time progress displayed during download
- **Secure configuration** - API key read from environment variable (not hardcoded)

## API Documentation

For more information about the BreweryDB API endpoints and data formats, visit:
https://www.brewerydb.com/developers/docs

## License

MIT
