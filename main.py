#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import tweepy
import json
import urllib
from urllib2 import urlopen, URLError
import ConfigParser
import random

class MainHandler(webapp2.RequestHandler):
    def get(self):
        repos = getRepos()
        index = random.randint(0,25)
        description = truncate(repos[index]["description"],75)
        link = repos[index]["title"]["href"]
        message = description + " - " + link
        #post = postStatus("Hello Twitter")
        self.response.write(message)
        #self.response.write(len(repos))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


# Gets list of repositories
def getRepos():
    # get api key from config
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    API_KEY = config.get('Kimono','API_KEY')

    #fetch data from api
    #data = json.load(urllib.urlopen("http://www.kimonolabs.com/api/ci1ld6i6?apikey=" + API_KEY))
    response = urlopen("http://www.kimonolabs.com/api/ci1ld6i6?apikey=" + API_KEY)
    raw_data = response.read()
    data = json.loads(raw_data)
    return data["results"]["repository"]


# posts message to twitter timeline
def postStatus(message):
    # get keys from config
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    # http://dev.twitter.com/apps/myappid
    CONSUMER_KEY = config.get('Twitter OAuth', 'CONSUMER_KEY')
    CONSUMER_SECRET = config.get('Twitter OAuth', 'CONSUMER_SECRET')
    # http://dev.twitter.com/apps/myappid/my_token
    ACCESS_TOKEN_KEY = config.get('Twitter OAuth', 'ACCESS_TOKEN_KEY')
    ACCESS_TOKEN_SECRET = config.get('Twitter OAuth', 'ACCESS_TOKEN_SECRET')

    # tweet
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, secure=True)
    result = api.update_status(message)
    return result

def truncate(message, length):
    return message[:length] + (message[length:] and '..')