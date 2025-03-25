import requests
import argparse
import json
import urllib.parse
import re

def parse_jira_url(jira_url):
    """Extracts the JIRA instance URL and JQL query from a JIRA search URL."""
    match = re.match(r"(https://[^/]+).*?[?&]jql=([^&]+)", jira_url)
    if not match:
        raise ValueError("Invalid JIRA search URL format.")
    
    jira_instance = match.group(1)
    jql_query = urllib.parse.unquote(match.group(2))  # Decode URL-encoded JQL
    return jira_instance, jql_query

def get_jira_issues(jira_instance, jql_query, api_token):
    """Fetches JIRA issues using the JQL query."""
    api_url = f"{jira_instance}/rest/api/2/search"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    params = {
        "jql": jql_query.strip(),
        "fields": "customfield_12310243,key,assignee",
        "maxResults": 1000
    }
    
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        response.raise_for_status()

    return response.json()

def calculate_story_points(jira_instance, issues):
    """Calculates total story points and finds issues missing story points."""
    total_points = 0
    issues_without_points = []
    
    for issue in issues.get("issues", []):
        story_points = issue["fields"].get("customfield_12310243")  # Story Points field
        issue_key = issue["key"]
        issue_url = f"{jira_instance}/browse/{issue_key}"

        if isinstance(story_points, (int, float)):
            total_points += story_points
        else:
            issues_without_points.append(issue_url)  # Store only the hyperlink
    
    return total_points, issues_without_points

def main():
    parser = argparse.ArgumentParser(description="Calculate total story points from a JIRA search URL.")
    parser.add_argument("jira_url", help="JIRA search URL with JQL (e.g., https://issues.redhat.com/issues/?jql=...)")
    parser.add_argument("-t", "--token", required=True, help="JIRA API token")
    args = parser.parse_args()

    try:
        jira_instance, jql_query = parse_jira_url(args.jira_url)
        issues = get_jira_issues(jira_instance, jql_query, args.token)
        total_story_points, issues_without_points = calculate_story_points(jira_instance, issues)
        
        print(f"Total Story Points: {total_story_points}")
        if issues_without_points:
            print("\nIssues without story points:")
            for issue_url in issues_without_points:
                print(issue_url)  # Only display hyperlink
    except ValueError as ve:
        print(f"Error parsing JIRA URL: {ve}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JIRA issues: {e}")

if __name__ == "__main__":
    main()
