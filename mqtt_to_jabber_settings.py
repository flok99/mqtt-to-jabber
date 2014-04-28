#!/usr/bin/python

# (C) 2014 by folkert van heusden
# mail@vanheusden.com

xmpp_user_from = 'domotica@jabber.vanheusden.com'
xmpp_user_password = 'jochie'
xmpp_connect_interval = 0.5
xmpp_user_to = 'folkert@jabber.vanheusden.com'
xmpp_heartbeat = False

mqtt_server = 'test.mosquitto.org'
mqtt_connect_interval = 0.5
mqtt_topic = [ '#' ]
mqtt_topic_qos = 0

verbose = True

xmpp_mqtt_topic_regexp_patterns = [ 'text', 'sms' ]
xmpp_mqtt_payload_regexp_patterns = [ '.*' ]
