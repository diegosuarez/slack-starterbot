#!/usr/bin/python
import os
import time
import re
from slackclient import SlackClient


# instantiate Slack client
#token = os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            print event["text"], event['channel']
            issue = parse_direct_mention(event["text"])
            if issue:
                return issue, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(r"#(\d+)", message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1)) if matches else None

def handle_command(issue, channel):
    response = "Hola, aqui tienes la issue: https://soporte.transparentcdn.com/issues/"+issue

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            try:
                command, channel = parse_bot_commands(slack_client.rtm_read())
                if command:
                     handle_command(command, channel)
                     time.sleep(RTM_READ_DELAY)
            except UnicodeEncodeError:
                pass
    else:
        print("Connection failed. Exception traceback printed above.")
