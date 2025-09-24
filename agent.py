import requests
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load necessary environment variables and check their presence
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
EMAIL = os.getenv('EMAIL')
API_TOKEN = os.getenv('API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not all([JIRA_DOMAIN, EMAIL, API_TOKEN, OPENAI_API_KEY]):
    raise ValueError("Please make sure all required environment variables are set in the .env file.")

# Setup for API authentication and headers
auth = (EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

# Generalized Jira API request function
def fetch_issues(jql: str, fields: str = "summary,status,priority") -> str:
    """Fetch issues from Jira based on JQL query."""
    url = f"{JIRA_DOMAIN}/rest/api/3/search"
    params = {"jql": jql, "fields": fields}
    
    try:
        response = requests.get(url, headers=headers, params=params, auth=auth)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        issues = data.get("issues", [])
        
        if not issues:
            return "No issues found."
        
        summary = "\n".join([
            f"- {issue['key']}: {issue['fields']['summary']} (Status: {issue['fields']['status']['name']})"
            for issue in issues
        ])
        return summary
    
    except requests.exceptions.RequestException as e:
        return f"❌ Error while fetching Jira issues: {e}"

# Define Tool functions with JQL queries
def get_all_issues(_: str) -> str:
    """Fetch all Jira issues."""
    return fetch_issues("ORDER BY priority DESC")

def get_current_user_issues(_: str) -> str:
    """Fetch Jira issues assigned to the current user."""
    return fetch_issues("assignee=currentUser() ORDER BY priority DESC")

def get_unassigned_issues(_: str) -> str:
    """Fetch unassigned Jira issues."""
    return fetch_issues("assignee is EMPTY ORDER BY priority DESC")

def get_unresolved_issues(_: str) -> str:
    """Fetch unresolved Jira issues."""
    return fetch_issues("resolution=Unresolved ORDER BY priority DESC")

# Initialize LangChain agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [
    Tool(name="AllIssues", func=get_all_issues, description="Fetch all issues from Jira."),
    Tool(name="CurrentUserJiraIssues", func=get_current_user_issues, description="Fetch Jira issues assigned to the current user."),
    Tool(name="UnassignedIssues", func=get_unassigned_issues, description="Fetch unassigned Jira issues."),
    Tool(name="UnresolvedIssues", func=get_unresolved_issues, description="Fetch unresolved Jira issues."),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Get task from terminal input
if __name__ == "__main__":
    print("🧠 Jira AI Agent is ready. Type your task or type 'exit' to quit.\n")

    while True:
        task = input("\n_______________________________________\n📥 Enter task:\n> ")

        if task.lower() in ["exit", "quit"]:
            print("👋 Exiting. Goodbye!")
            break

        try:
            result = agent.run(task)
            print("\n📤 Agent's Response:")
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
