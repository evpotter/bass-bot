import os
import time
from slackclient import SlackClient
import spotipy
from random import randint


# bass-bot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
BASS_COMMAND = "drop the bass"

# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
spotify = spotipy.Spotify()


def bass_command(command, slack_channel):
    response = "Not sure what you mean. Use the *" + BASS_COMMAND
    if command.startswith(BASS_COMMAND):
        try:
            q = 'artist:bassnectar'
            print q
            result = spotify.search(q, 25, 0, 'track')
            if result and 'tracks' in result and 'items' in result['tracks'] and len(result['tracks']['items']) > 0:
                rand_num = randint(0, len(result['tracks']['items']))
                response = result['tracks']['items'][rand_num]['external_urls']['spotify']
            else:
                response = "The spotify search returned no results"
        except:
            print "an error occurred that wasn't handled"
    slack_client.api_call("chat.postMessage", channel=slack_channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'], output['channel']
    return None, None


def find_music(message_text, slack_channel):
    try:
        text_detail = message_text.split('$[')[1].strip().lower()
        song_name = text_detail.split('-')[0]
        artist_name = text_detail.split('-')[1].split(']')[0]
        q = 'artist:' + artist_name + ' track:' + song_name
        print q
        result = spotify.search(q, 1, 0, 'track')
        if result and 'tracks' in result and 'items' in result['tracks'] and len(result['tracks']['items']) > 0:
            response = result['tracks']['items'][0]['external_urls']['spotify']
        else:
            response = "The spotify search returned no results"
        slack_client.api_call("chat.postMessage", channel=slack_channel, text=response, as_user=True)
    except:
        print "an error occurred that wasn't handled"

if __name__ == "__main__":
    READ_DELAY = 1  # 1 second delay between reading from fire hose
    if slack_client.rtm_connect():
        print("Bass-bot connected and running!")
        while True:
            text, channel = parse_slack_output(slack_client.rtm_read())
            if text and channel:
                if AT_BOT in text:
                    command_text = text.split(AT_BOT)[1].strip().lower()
                    bass_command(command_text, channel)
                if '$[' in text:
                    find_music(text, channel)
            time.sleep(READ_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
