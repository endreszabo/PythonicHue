#!/usr/bin/env python
from hue import *
from bridge import Bridge
import pythonichue
bridge = Bridge(
	api_key="CFGGnjZ8RXt7XPHlafpD-VDjed83SiqsccVgtqAp",
	## Read-write attributes
	name = 'hue-hubud1-test',
	zigbeechannel = 25,
	dhcp = True,
	ipaddress = '44.128.7.181',
	netmask = '255.255.255.240',
	gateway = '44.128.7.177',
	proxyaddress = 'none',
	proxyport = 0,
	timezone = 'Europe/Budapest',
	portalservices = False,
	## Read-only attributes
	bridgeid = '001788FFFE4F71FC',
	## Lamp serial numbers (optional)
	lamp_serials=[]
)

#################
# light objects #
#################

bridge.add_light(Light(
	## Read-write attributes
	name='Hue color lamp 1',
	serial='fixme',
	## Read-only attributes
))

#################
# group objects #
#################

bridge.add_group(Group(
	## Read-write attributes
	name='teszt',
	lights=[
		"Hue color lamp 1"
	],
	hue_type='Room',
	hue_class='Living room',
	## Read-only attributes
))

##################
# sensor objects #
##################

bridge.add_sensor(Sensor(
	## Read-write attributes
	name='Daylight',
	config={'on': True, 'configured': False, 'sunriseoffset': 30, 'sunsetoffset': -30},
	## Read-only attributes
	type='Daylight',
	modelid='PHDL00',
	manufacturername='Philips',
))

bridge.commit()
