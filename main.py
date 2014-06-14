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
import ConfigParser

class MainHandler(webapp2.RequestHandler):
    def get(self):
        repos = getRepos()
        self.response.write(json.dumps(repos[4]["title"]["text"]))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

def getRepos():
    # get api key from config
    config = ConfigParser.RawConfigParser()
    config.read('settings.cfg')
    API_KEY = config.get('Kimono','API_KEY')

    #fetch data from api
    data = json.load(urllib.urlopen("http://www.kimonolabs.com/api/ci1ld6i6?apikey=" + API_KEY))
    return data["results"]["repository"]