## Bridge Between Sentry hosted and Mattermost hosted

**Bridge to parse and format messages between Sentry and Mattermost using webhooks**

### Logic:
Sentry's Slack plugin only points to slack.com,
I couldn't get the deprecated Slack plugin to appear in my Sentry installation
There were very few other options at the time (there are better options out there now)

### Starting up
- Add a (Sentry webhook)[https://docs.sentry.io/product/integrations/integration-platform/webhooks/]
- Add a (Mattermost incoming webhook)[https://docs.mattermost.com/developer/webhooks-incoming.html]
- `$ cp config.py.example config.py`
- Edit values
- Replace text for the port that your bridge container will listen on in `Dockerfile`
  * `EXPOSE <YOUR BRIDGE PORT>` ~> `EXPOSE 8888`
- Build the container `$ docker build -t mattermost-sentry-bridge ./`
- Start the container `$ docker run --rm -d <YOUR BRIDGE PORT>:<YOUR BRIDGE PORT> -v ./config.py:/config.py mattermost-sentry-bridge`
