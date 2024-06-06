import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], '/slack/events', app)

client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
BOT_ID = client.api_call("auth.test")["user_id"]


@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    if user_id != BOT_ID:
        client.chat_postMessage(text=f"You said {text}", channel=channel_id)


# /weather is a slash command created in the bot. It can be used as /weather pune for example.
@app.route("/weather", methods=["POST"])
def weather():
    data = request.form
    location = data["text"]
    return Response(f"The current weather in {location} is 24 degrees", mimetype="text/plain"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
