from netmiko import ConnectHandler
import re
import sys
import time
def crc_finded(device_name,device_ip,interface):
	# Interface Regex
	regex_int='^(TenGigabitEthernet|GigabitEthernet|Port-Channel|ethernet|Ethernet|Tunnel|Null|Vlan|Serial|Bundle-Ether)\d+[/]?[\d+]?[/]?[\d+]?[\.]?[\d+]?[/]?[\d+]?[/]?[\d+]?[:]?[\d+]?$'
	#Define SSH parameters
	ssh_port="22"
	username="admin"
	password="admin"
	device_ty="cisco_ios"
	#CRC list
	crc_list=[]
	# Open CLI connection to device
	with ConnectHandler(device_ip,
						device_type=device_ty,
						port = ssh_port,
						username = username,
						password = password) as ch:
	# CRC lookup on interface
		ch.send_command("terminal length 0")
		crc=ch.send_command("sh int "+interface+" | include CRC")
	crc_list=crc.split(", ")
	#CRC list
	return "CRC on interface "+interface+" on device "+device_name+" is "+crc_list[1] 