#!/usr/bin/env python

import ConfigParser
import httplib2
import os
import json
import sys
import urllib

import splunk.mining.dcutils as dcu

def get_splatter_settings():
   settings = ConfigParser.ConfigParser()
   location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
   settings.read(location + '/../../etc/apps/splatter/bin/config.ini')
   # TODO: VALIDATE PRESENCE OF REQUIRED SETTINGS
   return settings
   
def post_chatter_message(msg, settings):
    dcu.getLogger().info("Message: %s" % msg)

    instance_server = settings.get('splatter', 'instance_server')
    access_token = get_chatter_access_token(instance_server, settings)

    dcu.getLogger().info("Access token: %s" % access_token)

    encoded_chatter_message = urllib.quote(msg)
    # Post to configured user's feed
    url = 'https://%s.salesforce.com/services/data/v26.0/chatter/feeds/news/me/feed-items?text=%s' % (instance_server, encoded_chatter_message)
    # Post to group's feed
    #url = 'https://%s.salesforce.com/services/data/v26.0/chatter/feeds/record/SFDC_GROUP_ID/feed-items?text=%s' % (instance_server, encoded_chatter_message)
    # Post to another user's feed (not yet)
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    headers = { 'authorization' : 'Bearer %s' % access_token }

    h.request(url, 'POST', headers=headers)
    # TODO: ERROR CHECKING

def get_chatter_access_token(instance_server, settings):
    post_args = {'grant_type' : 'password'}

    required_keys = ['client_id', 'client_secret', 'username', 'password']
    for k in required_keys:
        if settings.get('splatter', k):
            post_args[k] = settings.get('splatter', k)
    post_body = urllib.urlencode(post_args)

    h = httplib2.Http(disable_ssl_certificate_validation=True)
    instance_url = 'https://%s.salesforce.com/services/oauth2/token' % instance_server
    headers = { 'content-type' : 'application/x-www-form-urlencoded' }

    resp, content = h.request(instance_url, 'POST', body=post_body, headers=headers)
    # TODO: ERROR CHECKING

    parsed_content = json.loads(content)
    access_token = parsed_content['access_token']
    return access_token

# Main
settings = get_splatter_settings()
get_chatter_access_token(settings.get('splatter', 'instance_server'), settings)
msg = ('The saved search "%s" returned %s events, triggering an alert -- %s' % (sys.argv[4], sys.argv[1], sys.argv[6]))
post_chatter_message(msg, settings)