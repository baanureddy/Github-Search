from github import Github
import time

# Authentication token for accessing GitHub API
ACCESS_TOKEN = '<GITHIB_ACCESS_TOKEN>'

# Initialize the GitHub instance
github = Github(ACCESS_TOKEN)

# Organization name
ORG_NAME = '<ORG-NAME>'

# String to search for
SEARCH_STRING = '. fetch_config'

# Output file name
OUTPUT_FILE = 'search_results.txt'

# Rate limit variables
REQUESTS_LIMIT = 30  # Limit requests to 30 per minute
REQUESTS_RESET_TIME = 60  # Reset rate limit every 60 seconds

# Function to perform API calls with rate limiting and retry
def perform_api_call(func):
    while True:
        remaining_requests, _ = github.rate_limiting
        if remaining_requests <= REQUESTS_LIMIT:
            reset_time = github.rate_limiting_resettime
            wait_time = max(0, reset_time - time.time() + 1)
            if wait_time > 0:
                print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                break
        else:
            break
    return func()
        
def search_repo(repo):
    results = github.search_code(query=f'{SEARCH_STRING} repo:{repo.full_name}')
    if results.totalCount > 0:
        print(f"Found in {repo.full_name}")
        for result in results:
            content = result.decoded_content.decode("utf-8")
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if SEARCH_STRING in line:
                    with open(OUTPUT_FILE, 'a') as file:  # Open the file in append mode
                        print(f"\tFile: {result.path}, Line: {i + 1}, Content: {line.strip()}", file=file)

# Open the output file in write mode (clear the content)
with open(OUTPUT_FILE, 'w') as file:
    file.write('')

# Search across all repositories in the organization
for repo in github.search_repositories(query=f'org:{ORG_NAME}'):
    # Call the search_repo function with the current repository
    #search_repo(repo)
    perform_api_call(lambda: search_repo(repo))
