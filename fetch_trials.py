import argparse
import json
import requests

def fetch_trials(search_term, output_file, statuses=None, countries=None):
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"format": "json", "pageSize": 1000}
    query_parts = [search_term]
    if countries:
        country_filters = []
        for c in countries:
            if ' ' in c:
                c = f'"{c}"'
            country_filters.append(f"AREA[LocationCountry]{c}")
        country_filter = " (" + " OR ".join(country_filters) + ")"
        query_parts.append(country_filter)
    params["query.term"] = " AND ".join(query_parts)
    if statuses:
        params["filter.overallStatus"] = ",".join(statuses)
    studies = []
    while True:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        studies.extend(data.get("studies", []))
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
        params["pageToken"] = next_page_token
    with open(output_file, 'w') as f:
        json.dump(studies, f, indent=4)
    print(f"Saved {len(studies)} trials to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch clinical trials from ClinicalTrials.gov API and save to JSON.")
    parser.add_argument("search_term", help="The search term to query for clinical trials (e.g., 'cancer').")
    parser.add_argument("-o", "--output", default="trials.json", help="The output JSON file path (default: trials.json).")
    parser.add_argument("--status", action="append", help="Filter by overall status (e.g., RECRUITING). Can be used multiple times. Allowed values: ACTIVE_NOT_RECRUITING, COMPLETED, ENROLLING_BY_INVITATION, NOT_YET_RECRUITING, RECRUITING, SUSPENDED, TERMINATED, WITHDRAWN, AVAILABLE, NO_LONGER_AVAILABLE, TEMPORARILY_NOT_AVAILABLE, APPROVED_FOR_MARKETING, WITHHELD, UNKNOWN")
    parser.add_argument("--country", action="append", help="Filter by country where facilities are located (e.g., Sweden). Can be used multiple times. Uses advanced query syntax.")
    args = parser.parse_args()
    fetch_trials(args.search_term, args.output, args.status, args.country) 