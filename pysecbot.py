import os
import time
from slackclient import SlackClient

"""
    Todo:
        1. Create Brosec integration
        2. Add Tool web scraping
            a. Top 10
            b. New
                a1. Today
                b2. Week
                c3. Month
        3. Optimize Code
        4. Docker integration
        5.
"""


# pysecbot's ID as an enviornment variable
BOT_ID = os.environ.get("BOT_ID")
system = os.system('uname -a')
# constants
AT_BOT = "<@" + BOT_ID + ">"
COMMANDS = ["do", "bros"]

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    """
    Receives commands directed at the bot and determines if they are valid commands.
    If so, then acts on the commands. If not, returns back what it needs for clarification
    """
    response = "Not sure what you mean. Use the *" + COMMANDS + "* command with numbers, delimited by spaces."

    """
    Creating a command for the bot:
        1. When calling to the bot in Slack the string will be parsed. From there it will look at the first word in the
           string. handle_command will check that and if it matches the EXAMPLE_COMMAND the bot will evaluate the next
           section in the string.
        2. Now if it matches the first section and the next section does not match the conditions programmed it will spit
           out a custom error.
        3. If they bot match it will run the section of the code in the IF statement.

        Example:
            if command.statswith(EXAMPLE_COMMAND):
                # this will move to the nested IF statement
                if command.split()[2] == 'Argument':  # here we are breaking the string you give the bot in to a list
                                                      # and looking at the next section of the string. If true will
                                                      # run the block of code
                    do block of code

    """

    for cmd in COMMANDS:    # Loops through COMMANDS
        if command.startswith(cmd):    # Checks to see if the string sent to the Bot starts with any of the COMMANDS set in the list
            print "Handler " + cmd
            # cupofjoe command
            if command.split()[1] == 'option':
                response = """----------------------
                [1] - cupofjoe
                [2] -
                [3] -
                """



            elif command.split()[1] == 'cupofjoe':
                response = "Kill yourself Joe!"
            elif command.split()[1] == 'system': # not a super safe command to add to you bot, but pretty cool!
                response = os.popen(command.split()[2]).read()
            else:
                # If command doesn't exist return this response
                response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
    The Slack Real Time Messaging API is an envents firehose.
    This parsing function returns None unless a message is directed at the Bot, Based on its ID.
    :param slack_rtm_output:
    :return:
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Pysecbot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")