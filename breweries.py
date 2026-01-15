#!/usr/bin/env python3
"""
Fetch all breweries from Open Brewery DB API.

This script retrieves all brewery data from the Open Brewery DB API
and saves it to a JSON file.

Open Brewery DB is a free, open-source API that requires no authentication.
https://www.openbrewerydb.org/
"""

import json
import sys
import time
import argparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
DEFAULT_OUTPUT_FILE = "breweries.json"
API_BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
REQUEST_DELAY = 0.2  # Seconds between requests to be respectful
REQUEST_TIMEOUT = 30  # Seconds
PER_PAGE = 200  # Maximum allowed by API


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


def get_total_count(session, params=None):
    """Get total brewery count from metadata endpoint."""
    try:
        response = session.get(
            f"{API_BASE_URL}/meta",
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        meta = response.json()
        return int(meta.get("total", 0))
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"Warning: Could not get total count: {e}")
        return None


def fetch_breweries(output_file, by_country=None, by_state=None, by_city=None, by_type=None):
    """
    Fetch all breweries from Open Brewery DB API.

    Args:
        output_file: Path to output JSON file
        by_country: Filter by country
        by_state: Filter by state/province
        by_city: Filter by city
        by_type: Filter by brewery type
    """
    session = create_session()

    # Build filter parameters
    filter_params = {}
    if by_country:
        filter_params["by_country"] = by_country.replace(" ", "_")
    if by_state:
        filter_params["by_state"] = by_state.replace(" ", "_")
    if by_city:
        filter_params["by_city"] = by_city.replace(" ", "_")
    if by_type:
        filter_params["by_type"] = by_type

    # Get total count for progress reporting
    print("Connecting to Open Brewery DB API...")
    total_count = get_total_count(session, filter_params)
    if total_count:
        print(f"Found {total_count} breweries to fetch")
    else:
        print("Fetching breweries (total count unknown)...")

    # Collect all data
    all_breweries = []
    page = 1

    while True:
        params = {
            "page": page,
            "per_page": PER_PAGE,
            **filter_params
        }

        try:
            if page > 1:
                time.sleep(REQUEST_DELAY)  # Rate limiting

            response = session.get(
                API_BASE_URL,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            page_data = response.json()

            # Empty response means we've fetched all pages
            if not page_data:
                break

            all_breweries.extend(page_data)

            if total_count:
                print(f"Fetched page {page} ({len(all_breweries)}/{total_count} breweries)")
            else:
                print(f"Fetched page {page} ({len(all_breweries)} breweries collected)")

            # If we got fewer than per_page, we're done
            if len(page_data) < PER_PAGE:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            print("Saving partial data...")
            break

    # Save to file
    print(f"\nSaving {len(all_breweries)} breweries to {output_file}...")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_breweries, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved data to {output_file}")
    except IOError as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

    return len(all_breweries)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch all breweries from Open Brewery DB API"
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output JSON file (default: {DEFAULT_OUTPUT_FILE})"
    )
    parser.add_argument(
        "--country",
        help="Filter by country (e.g., 'United States', 'Ireland')"
    )
    parser.add_argument(
        "--state",
        help="Filter by state/province (e.g., 'California', 'New York')"
    )
    parser.add_argument(
        "--city",
        help="Filter by city (e.g., 'San Diego', 'Portland')"
    )
    parser.add_argument(
        "--type",
        choices=["micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprietor", "closed"],
        help="Filter by brewery type"
    )

    args = parser.parse_args()

    count = fetch_breweries(
        output_file=args.output,
        by_country=args.country,
        by_state=args.state,
        by_city=args.city,
        by_type=args.type
    )

    print(f"\nDone! Fetched {count} breweries.")


if __name__ == "__main__":
    main()
