#!/usr/bin/python

import mosquitto
import re
import sys
import time
import traceback
import xmpp

xmpp_user = 'domotica@jabber.vanheusden.com'
xmpp_password = 'jochie'
xmpp_connect_interval = 0.5
xmpp_target = 'folkert@jabber.vanheusden.com'

mqtt_server = 'mauer'
mqtt_connect_interval = 0.5
mqtt_topic = [ '#' ]
mqtt_topic_qos = 0

verbose = True

xmpp_mqtt_topic_regexp_pattern = 'temp'
xmpp_mqtt_payload_regexp_pattern = '.*'

jid = xmpp.JID(xmpp_user)
cnx = xmpp.Client(jid.getDomain(), debug=[])

xmpp_mqtt_topic_regexp = re.compile(xmpp_mqtt_topic_regexp_pattern)
xmpp_mqtt_payload_regexp = re.compile(xmpp_mqtt_payload_regexp_pattern)

mqtt_client = mosquitto.Mosquitto('mqtt-to-jabber')
mqtt_connected = False

# mqtt
def on_message(mosq, obj, msg):
	global cnx
	global xmpp
	global verbose

	if verbose:
		print("Message received on topic " + msg.topic + " with QoS " + str(msg.qos) + " and payload " + msg.payload)

	if re.match(xmpp_mqtt_payload_regexp, msg.payload) and re.match(xmpp_mqtt_topic_regexp, msg.topic):
		if verbose:
			print 'Sending %s to XMPP (Jabber)' % msg.payload

		cnx.send(xmpp.Message(xmpp_target, msg.topic + ' ' + msg.payload))

	else:
		if verbose:
			print '...ignored'

# jabber
def presenceCB(conn, event):
	global verbose

        if event.getType() == 'subscribe':
                who = event.getFrom()

		if verbose:
			print 'Subscribe reqest from %s (XMPP/Jabber)' % who

                conn.send(xmpp.Presence(to = who, typ = 'subscribed'))
                conn.send(xmpp.Presence(to = who, typ = 'subscribe'))

connected_cnt = 0
pres = xmpp.Presence()

while True:
	while mqtt_connected == False:
		try:
			mqtt_client.connect(mqtt_server)
			mqtt_client.on_message = on_message

			for topic in mqtt_topic:
				mqtt_client.subscribe(topic, mqtt_topic_qos)

			mqtt_connected = True

			if verbose:
				print 'Connected to mosquitto'

		except:
			if verbose:
				print 'Failed connecting to mosquitto %s' % mqtt_server
				traceback.print_exc(file = sys.stdout)

		if mqtt_connected == False:
			time.sleep(mqtt_connect_interval)

	while not cnx.isConnected():
		connected_cnt = 0

		if verbose:
			print 'Connecting to XMPP (Jabber)...'

		try:
			cnx.connect()
			cnx.auth(jid.getNode(), xmpp_password, 'mqtt-to-jabber')

			cnx.sendInitPresence()

			cnx.RegisterHandler('presence', presenceCB)

			if cnx.isConnected():
				if verbose:
					print 'Connected to XMPP (Jabber)'

					cnx.send(xmpp.Message(xmpp_target, 'Connected!'))
			else:
				time.sleep(xmpp_connect_interval)

		except:
			if verbose:
				print 'Exception during XMPP (Jabber) connect'
				traceback.print_exc(file = sys.stdout)

	if mqtt_client.loop(5000) != 0:
		if verbose:
			print 'Disconnected from mosquitto'

		mqtt_connected = False

		try:
			mqtt_client.disconnect()
		except:
			if verbose:
				print 'mosquitto disconnect failed'
				traceback.print_exc(file = sys.stdout)
			pass

	cnx.Process(1)

	if cnx.isConnected():
		connected_cnt += 1

		statstr = 'Connected %d' % connected_cnt
		pres.setStatus(statstr)
		cnx.send(pres)
