import os
import http.client
import urllib
import config

class Message:
  def __init__(self):
    self.pushover_user = config.PUSHOVER_USER
    self.pushover_token = config.PUSHOVER_TOKEN
  def push(self,text):
          """
          Send a Push Notification using the Pushover API
          """
          conn = http.client.HTTPSConnection("api.pushover.net:443")
          conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
              "token": self.pushover_token,
              "user": self.pushover_user,
              "message": text,
              "sound": "cashregister"
            }), { "Content-type": "application/x-www-form-urlencoded" })
          conn.getresponse()