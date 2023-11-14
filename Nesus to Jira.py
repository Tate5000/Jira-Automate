import pandas as pd 
from jira import JIRA

# Step 1: Read Excel Data
nessus_data = pd.read_excel('path_to_nessus_scan_results.xlsx')
relevant_data = nessus_data[['Plugin ID', 'Name', 'Description', 'Solution', 'Plugin Output']]

# Step 3: Connect to Jira
jira_options = {'server': 'https://your_jira_server'}
jira = JIRA(options=jira_options, basic_auth=('username', 'password'))

# Retrieve existing Jira ticket summaries for project 'IA'
jql_query = "project = IA"
existing_issues = jira.search_issues(jql_query, fields="summary,description")

# Create a set to store unique identifiers from existing issues
existing_identifiers = set()
for issue in existing_issues:
    # Adjust the following lines to match how the 'Plugin ID' is stored in your Jira tickets
    if 'Plugin ID' in issue.fields.summary:
        existing_identifiers.add(issue.fields.summary.split('Plugin ID: ')[1].split(')')[0])
    if 'Plugin ID' in issue.fields.description:
        existing_identifiers.add(issue.fields.description.split('Plugin ID: ')[1].split('\n')[0])

# Process and filter Nessus data to only include new issues that need Jira tickets
filtered_data = relevant_data[~relevant_data['Plugin ID'].astype(str).isin(existing_identifiers)]

# Step 4: Map Nessus Data to Jira Fields and Create Tickets
for index, row in filtered_data.iterrows():
    issue_dict = {
        'project': {'key': 'IA'},
        'summary': f"Security Issue: {row['Name']} ({row['Plugin ID']})",
        'description': f"Description: {row['Description']}\n\nSolution: {row['Solution']}\n\nOutput: {row['Plugin Output']}",
        'issuetype': {'name': 'Task'},
        'reporter': {'name': 'reporter_username'},  #
    }
    
    # Create a new jira
    new_issue = jira.create_issue(fields=issue_dict)
    print(f"Created new issue: {new_issue.key}")

