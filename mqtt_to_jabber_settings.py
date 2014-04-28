#!/usr/bin/python

# (C) 2014 by folkert van heusden
# mail@vanheusden.com

# you might want to adjust the following parameters

xmpp_user_from = 'sender@host.bla'
xmpp_user_password = '****PASSWORD****'
xmpp_connect_interval = 0.5
xmpp_user_to = 'youraccount@somehost.com'
# shows a counter in the xmpp-status
xmpp_heartbeat = False

mqtt_server = 'test.mosquitto.org' # point this to your local mqtt server
mqtt_connect_interval = 0.5
mqtt_topic = [ '#' ] # topic(s) to listen to
mqtt_topic_qos = 0

verbose = True

# it works like this:
# - IF one of the topics matches
# - AND
# - IF one of the payloads matches
# - THEN send via jabber
xmpp_mqtt_topic_regexp_patterns = [ 'text.*bla', 'sms[0-9]*' ] # regexps to look for
xmpp_mqtt_payload_regexp_patterns = [ '.*' ] # regexps to look for
