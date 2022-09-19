# Data Monitoring Script

This is a python script that runs daily and checks the #data-monitoring slack channel. When the script is run, it first checks to see if the payment-bot uploaded the number of subscriptions retried on the current date, then calculates the difference, and if the difference is greater than 3%, it sends a message in slack to notify the data science team. 

## Setup

Set the following environment variables in a `.env` file. 

```
SLACK_BOT_TOKEN=
```

- [Slack Bot Token](https://api.slack.com/apps/A01K7ESN4AW/oauth?) - Oauth & Permissions section of the slack bot being used
    - If there's no existing slack bot [create one](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace)

## Libraries
Use the package manager to install [pip](https://pip.pypa.io/en/stable/) to install [slack_sdk](https://github.com/slackapi/python-slack-sdk). Install any other missing libraries. 

```bash
pip3 install slack_sdk
```

## File Specific Changes
Copy data-monitoring-script.py to a directory and make the changes to the file:

```python
# Update the file path to .env in line 9
load_dotenv('dot env path')

# Set the conversation ID (slack channel key) in line 15 (if necessary)
conversation_id = ""

# Set the slack user that you want to notify in line 69, or keep default
'<@>'

# Set the slack channel where the user should be notified in line 76
channel='#'
```

## Schedule
Test that it runs locally. 

```bash
# Local test run
python3 data-monitoring-script
```
## Example Run
<img width="837" alt="Screen Shot 2022-08-23 at 12 34 29 PM" src="https://user-images.githubusercontent.com/108364344/186250276-02a243aa-846f-4e5f-95b0-754f0afbec41.png">
