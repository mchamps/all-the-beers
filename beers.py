#!/usr/bin/env python3
"""
Fetch all beers from BreweryDB API.

This script retrieves all beer data including brewery and ingredient information
from the BreweryDB API and saves it to a JSON file.

Requires a BreweryDB premium account API key.
"""

import json
import os
import sys
import time
import argparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
DEFAULT_OUTPUT_FILE = "beers.json"
API_BASE_URL = "https://api.brewerydb.com/v2"
REQUEST_DELAY = 0.5  # Seconds between requests to avoid rate limiting
REQUEST_TIMEOUT = 30  # Seconds


def create_session():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_api_key():
    """Get API key from environment variable."""
    api_key = os.environ.get("BREWERYDB_API_KEY")
    if not api_key:
        print("Error: BREWERYDB_API_KEY environment variable is not set.")
        print("Please set it with your BreweryDB API key:")
        print("  export BREWERYDB_API_KEY='your_api_key_here'  # Linux/Mac")
        print("  set BREWERYDB_API_KEY=your_api_key_here       # Windows")
        sys.exit(1)
    return api_key


def fetch_beers(api_key, output_file, include_breweries=True, include_ingredients=True):
    """
    Fetch all beers from BreweryDB API.

    Args:
        api_key: BreweryDB API key
        output_file: Path to output JSON file
        include_breweries: Include brewery data for each beer
        include_ingredients: Include ingredient data for each beer
    """
    session = create_session()

    # Build query parameters
    params = {
        "key": api_key,
        "p": 1,
    }
    if include_breweries:
        params["withBreweries"] = "Y"
    if include_ingredients:
        params["withIngredients"] = "Y"

    # Make initial request to get metadata
    print("Connecting to BreweryDB API...")
    try:
        response = session.get(
            f"{API_BASE_URL}/beers",
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        sys.exit(1)

    # Check for API errors
    if result.get("status") == "failure":
        print(f"API Error: {result.get('errorMessage', 'Unknown error')}")
        sys.exit(1)

    # Extract metadata
    num_pages = result.get("numberOfPages", 1)
    total_results = result.get("totalResults", 0)

    print(f"Found {total_results} beers across {num_pages} pages")

    # Collect all data
    all_beers = result.get("data", [])

    # Fetch remaining pages
    for page in range(2, num_pages + 1):
        params["p"] = page

        try:
            time.sleep(REQUEST_DELAY)  # Rate limiting
            response = session.get(
                f"{API_BASE_URL}/beers",
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()

            page_data = result.get("data", [])
            all_beers.extend(page_data)  # Flatten data into single list

            print(f"Fetched page {page}/{num_pages} ({len(all_beers)} beers collected)")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            print("Saving partial data...")
            break

    # Save to file
    print(f"\nSaving {len(all_beers)} beers to {output_file}...")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_beers, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved data to {output_file}")
    except IOError as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

    return len(all_beers)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch all beers from BreweryDB API"
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output JSON file (default: {DEFAULT_OUTPUT_FILE})"
    )
    parser.add_argument(
        "--no-breweries",
        action="store_true",
        help="Exclude brewery data"
    )
    parser.add_argument(
        "--no-ingredients",
        action="store_true",
        help="Exclude ingredient data"
    )

    args = parser.parse_args()

    api_key = get_api_key()

    count = fetch_beers(
        api_key=api_key,
        output_file=args.output,
        include_breweries=not args.no_breweries,
        include_ingredients=not args.no_ingredients
    )

    print(f"\nDone! Fetched {count} beers.")


if __name__ == "__main__":
    main()
