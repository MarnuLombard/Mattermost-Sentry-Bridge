import re, json
from flask import Flask, request
from requests import request as curl_request
from urllib.parse import quote, urlencode, quote_plus
from config import *


def new_error_send(data):
    debug(message=data)
    debug(message="-------------")

    event = data.get("event")
    message = data.get("message")
    project = data.get("project_name")

    if len(message) < 1:
        message=event.get("title")

    if data and project and message:
        sentry_url = data.get("url", "#")
        level = data.get("level", "error").title()
        title = "New {} in {}".format(level, project)
        culprit = data.get("culprit", event.get("culprit"))
        user = event.get("user", {}).get("username", False)
        level = data.get("level")

        if not user:
            user = "Unknown"
        
        """ Match everyting between the production.ERROR and the stacktrace """
        header = re.findall(r'] .*.ERROR: (.+?)(?=[\[{\n])', message)
        
        if not header or len(header) < 1:
            """ Simples way to extract everything until the (optional) stacktrace in the string """
            header = re.split(r'(.+?)(?=[\[{\n])', message)
            """ Filter out empty values """
            header = [x for x in header if x]

        if not header or len(header) < 1:
            header = ["Mattermost Sentry Bridge Error Parsing header"]
        
        header = "[{}]({})".format(header[0], sentry_url)

        text = u"""**{}**
##### {}  
 | Key          | Value        |
 | -----------: | :----------- |
 | culprit      | {}           |
 | user         | {}           |
 | level        | {}           |
""".format(title, header, culprit, user, level)

        debug(message=text)

        return post_to_mattermost(text=text)
    else:
        print("Project name and Message Missing!")
        print(data)

def post_to_mattermost(text, channel=CHANNEL, username=USER_NAME, icon_url=USER_ICON):
    payload={
        'channel':channel,
        'text':text,
        'username':username,
        'icon_url':icon_url
    }
    payload = json.dumps(payload)
    debug(message=payload)
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    response = curl_request("POST", MM_URL+"hooks/"+HOOK_ID, data=payload, headers=headers)
    result = response.text
    debug(message="---hook response---")
    debug(message=result)
    return result

def debug(message):
    if DEBUG:
        print(message)

""" Start flask app """

app = Flask(__name__)

@app.route('/hooks/<token>', methods=['POST', 'GET'])
def mattermost_sentry(token):
    if token == HOOK_ID:
        try:
            data = request.json
        except Exception as ex:
            return str(ex)
        
        new_error_send(data = data)
    else:
        print("Wrong hook.")

    return token

if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = PORT, debug = DEBUG)
