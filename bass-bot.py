import os
import time
from slackclient import SlackClient


# bass-bot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
BASS_COMMAND = "drop the bass"

# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, spotify_channel):
    response = "Not sure what you mean. Use the *" + BASS_COMMAND
    if command.startswith(BASS_COMMAND):
        response = "https://open.spotify.com/track/67nDjmo4SYiaVgWvFavDCb"
    slack_client.api_call("chat.postMessage", channel=spotify_channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'], output['channel']
    return None, None


if __name__ == "__main__":
    READ_DELAY = 1  # 1 second delay between reading from fire hose
    if slack_client.rtm_connect():
        print("Bass-bot connected and running!")
        while True:
            text, channel = parse_slack_output(slack_client.rtm_read())
            if text and channel:
                if AT_BOT in text:
                    command_text = text.split(AT_BOT)[1].strip().lower()
                    handle_command(command_text, channel)
            time.sleep(READ_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
