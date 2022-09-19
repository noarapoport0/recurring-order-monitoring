from dotenv import load_dotenv
from datetime import date, timedelta
import time
import gspread
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import re

slack_token = os.environ["SLACK_BOT_TOKEN"] # connects to slack
client = WebClient(token=slack_token)

# ID of channel that the message exists in
conversation_id = "conversation ID not shown"  #  channel ID


today = date.today() # function that find's today's date
yesterday = today - timedelta(days=1)
todays_date = today.strftime("%Y-%m-%d")
yesterday_date_unix = time.mktime(yesterday.timetuple()) # slack function needs timestamp in form of unix to recognize time


def read_slack_message(conversation_id, number, date):  # function to read the slack message
    # date parameter can be changed to any date, default is just today's date
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization    
        result = client.conversations_history( # finding the slack message
            channel=conversation_id,
            inclusive=True,
            oldest=date
        )
        message = result["messages"][number] 
        # Print message text
        message = message["text"]
        return(message)

    except SlackApiError as e: # returns error message if there is an issue with the slack api function
        print(f"Error: {e}")

def is_message_will_be_retried(message, date): # is the message in the format of will be retried
    if re.search(date, message) == False:  
        return("This is not today's date")
    will = re.search('will be retried', message)
    if will:
        return(True)

def is_message_were_retried(message, date): # is the message in the format of were retried
    if re.search(date, message) == False:  
        return("This is not today's date")
    were = re.search('were retried', message)
    if were:
        return(True)

messages = [] # stores the messages found in slack
values = [] # stores the number of subscriptions retried
count = 0 # track if you found both messages
for i in range(0,100):
    messages.append(read_slack_message(conversation_id, number = i, date = yesterday_date_unix))
    if is_message_will_be_retried(messages[i], todays_date) == True:
        values.append(messages[i].split()[0])
        count += 1
    elif is_message_were_retried(messages[i], todays_date) == True:
        values.append(messages[i].split()[0])
        count += 1
    if count == 2: 
        percent_difference = ((int(values[1])-int(values[0]))/int(values[0]))*100
        if percent_difference > 3:
            text = "<> There was a greater than 3 percent difference in retries on " + today.strftime("%m/%d/%Y") + ". The percent difference was " + str(round(percent_difference, 2)) + '%.'
        else:
            text = "flag"
            break
        break
    else:
        text = "The script ran, but data is missing."

if text != 'flag':
    client.chat_postMessage(channel='#channel id not shown', 
        blocks= [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ] 
    )