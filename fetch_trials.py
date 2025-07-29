import argparse
import json
import requests

def fetch_trials(search_term, output_file):
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"format": "json", "pageSize": 1000, "query.term": search_term}
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
    args = parser.parse_args()
    fetch_trials(args.search_term, args.output) 