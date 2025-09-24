# Jira AI Agent using LangChain and OpenAI

This PoC allows you to interact with your Jira account using an AI-powered agent. The agent can fetch and interact with various Jira issues based on different JQL queries (e.g., all issues, issues assigned to the current user, unassigned issues, unresolved issues). The agent is powered by OpenAI's GPT-3.5 and integrates with Jira via their REST API.

## Requirements

- Python 3.8 or above
- OpenAI API key
- Jira API token

## Setup Instructions

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/jira-ai-agent.git
cd jira-ai-agent
````

### 2. Set Up Your Environment Variables

Create a `.env` file in the project root by copying from the provided `.env.back`:

```bash
cp .env.back .env
```

Then, update the `.env` file with your own values:

```env
# .env

JIRA_DOMAIN=https://your-domain.atlassian.net
EMAIL=your-email@example.com
API_TOKEN=your-jira-api-token
OPENAI_API_KEY=your-openai-api-key
```

> ⚠️ Do **not** commit the `.env` file. It contains sensitive credentials.

### 3. Install the required dependencies

Create a virtual environment and install the required dependencies by running the following commands:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

### 4. Run the Jira AI Agent

After setting up the environment and installing the dependencies, you can start the agent. Run the following command:

```bash
python agent.py
```

This will launch the agent, and you'll be able to interact with it via the terminal. 

You can type in tasks like:
* "All issues"
* "All issues assigned to me"
* "Completed issues"
* "My completed issues"
* "Unresolved issues"
* "My unresolved issues"
* "Unassigned issues"

To exit the program, simply type `exit` or `quit`.

### 5. Example Interaction

Once the agent is running, you can type tasks to interact with Jira, for example:

```
🧠 Jira AI Agent is ready. Type your task or type 'exit' to quit.

_______________________________________
📥 Enter task:
> All issues

📤 Agent's Response:
- KAN-1: This is a test task (Status: In Progress)
- KAN-2: This is another test (Status: Done)

_______________________________________
📥 Enter task:
> Unresolved Issues

📤 Agent's Response:
- KAN-1: This is a test task (Status: In Progress)

_______________________________________
📥 Enter task:
> exit
👋 Exiting. Goodbye!
```

## Dependencies

The project requires the following Python libraries:

* `requests`: For making HTTP requests to the Jira API.
* `langchain`: For building and interacting with the language model.
* `langchain_community`: Community extensions for LangChain.
* `openai`: For OpenAI API integration.
* `python-dotenv`: For loading environment variables from the `.env` file.

You can find the full list of dependencies in the `requirements.txt` file.

## Troubleshooting

* **Error: Missing Environment Variables**: Make sure your `.env` file is set up correctly with all the necessary values (e.g., `JIRA_DOMAIN`, `EMAIL`, `API_TOKEN`, `OPENAI_API_KEY`).
* **Error: Connection Issues**: Check your internet connection and ensure that Jira and OpenAI are accessible.
* **Rate Limits**: Be mindful of rate limits imposed by Jira and OpenAI. If you exceed the rate limit, you may receive errors or slow responses.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vitthalsynerzip/jira-ai-agent/blob/main/LICENSE) file for details.