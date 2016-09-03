import os
from slackclient import SlackClient
"""Use this program and the API Key(SLACK_BOT_TOKEN) to pull the ID for your Slack PyBot
   Once you get the user ID set that up as the BOT_ID
   TODO:
        1. Have this create the BOT_ID in envs vars
"""
BOT_NAME = 'plizzly'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        #retrieve all users so we can find out bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is "+ user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME )