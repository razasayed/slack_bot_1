import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/slack/events", app)

client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
BOT_ID = client.api_call("auth.test")["user_id"]


@slack_event_adapter.on("message")
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

@app.route("/confluence", methods=["POST"])
def confluence():
    data = request.form
    question = data["text"]
    if question == "what is ensemble":
        return Response(f"Arkose Ensemble is a framework described as a substrate for developing advanced modular components for detecting telltales and managing traffic pressure. It enables multiple components to integrate seamlessly across a platform and allows for greater transparency in data transfers between components. It is part of the Arkose Labs system that focuses on automation, migration work, new feature development, bug fixing, performance optimization, and reliability.
", mimetype="text/plain"), 200
    elif question == "what are telltales":
        return Response(f"Telltales are repeated patterns within traffic that are used to identify 'bad' actors. They are created either by systems (AI/computer-generated) or by a SOC team manually to identify malicious traffic and take action against it. Telltales are rules-based systems that leverage information on a session to validate whether a client matches any existing rules and then take actions based on that information.", mimetype="text/plain"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
