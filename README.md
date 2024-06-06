```
pip install slackclient python-dotenv Flask slackeventsapi
```

Put the following in a .env file in the root of the project

SLACK_TOKEN is received after adding oauth scope

SIGNING_SECRET is received after adding the app to the workspace from Basic Information section

Need to add the ```chat:write``` oauth scope

Need to subscribe to ```message.im``` event in the Event Subscriptions section

```
SLACK_TOKEN=<slack_token>
SIGNING_SECRET=<signing_secret>
```