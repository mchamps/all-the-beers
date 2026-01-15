#!/usr/bin/env python3
"""
Fetch all brewery locations from BreweryDB API.

This script retrieves all brewery location data from the BreweryDB API
and saves it to a JSON file.

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
DEFAULT_OUTPUT_FILE = "brewerys.json"
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


def fetch_locations(api_key, output_file):
    """
    Fetch all brewery locations from BreweryDB API.

    Args:
        api_key: BreweryDB API key
        output_file: Path to output JSON file
    """
    session = create_session()

    # Build query parameters
    params = {
        "key": api_key,
        "p": 1,
    }

    # Make initial request to get metadata
    print("Connecting to BreweryDB API...")
    try:
        response = session.get(
            f"{API_BASE_URL}/locations",
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

    print(f"Found {total_results} brewery locations across {num_pages} pages")

    # Collect all data
    all_locations = result.get("data", [])

    # Fetch remaining pages
    for page in range(2, num_pages + 1):
        params["p"] = page

        try:
            time.sleep(REQUEST_DELAY)  # Rate limiting
            response = session.get(
                f"{API_BASE_URL}/locations",
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()

            page_data = result.get("data", [])
            all_locations.extend(page_data)  # Flatten data into single list

            print(f"Fetched page {page}/{num_pages} ({len(all_locations)} locations collected)")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            print("Saving partial data...")
            break

    # Save to file
    print(f"\nSaving {len(all_locations)} locations to {output_file}...")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_locations, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved data to {output_file}")
    except IOError as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

    return len(all_locations)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch all brewery locations from BreweryDB API"
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output JSON file (default: {DEFAULT_OUTPUT_FILE})"
    )

    args = parser.parse_args()

    api_key = get_api_key()

    count = fetch_locations(
        api_key=api_key,
        output_file=args.output
    )

    print(f"\nDone! Fetched {count} brewery locations.")


if __name__ == "__main__":
    main()
