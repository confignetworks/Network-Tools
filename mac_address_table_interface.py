from netmiko import ConnectHandler
import re
import sys
import time
def get_mac_interface(wantedmac):
	#IP address regex
	regex_ip = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
	# Mac address Regex
	regex_mac='([a-fA-F0-9]{2}[:|\-]?){6}'
	regex_cisco_mac='([a-fA-F0-9]{4}[:|\-.]?){3}'
	# Interface Regex
	regex_int='^(TenGigabitEthernet|GigabitEthernet|Port-Channel|ethernet|Ethernet|Tunnel|Null|Vlan|Serial|Bundle-Ether|Et|Gi|Ten)\d+[/]?[\d+]?[/]?[\d+]?[\.]?[\d+]?[/]?[\d+]?[/]?[\d+]?[:]?[\d+]?$'
	#Define SSH parameters
	ssh_port="22"
	username="admin"
	password="admin"
	device_ty="cisco_ios"
	# Define mac list     
	mac_list=[]
	#Bring device IP addresses from IP file 
	with open('ip.txt','r') as ip:
	   chaine=ip.read()
	   device_list=chaine.split("\n")
	# Loop for all devices
	
	for device in device_list:
		# Open CLI connection to device
		with ConnectHandler(device,
							device_type=device_ty,
							port = ssh_port,
							username = username,
							password = password) as ch:
		# Get device hostname
			ch.send_command("terminal length 0")
			device_hostname=ch.send_command("sh run | s hostname")
		# show mac address-table
			mac_table=ch.send_command("sh mac address-table")
		#put hostname and ip address in list
		hostname=device_hostname.split(" ")
		hostname.remove("hostname")
		mac_list.append(hostname[0])
		mac_list.append(device)
		# Remove \n to keep interface
		mac_table=mac_table.replace('\n',' ')
			
		# Create arp table list    
		mac_list_temp=mac_table.split(" ")
	
		#search IPs and MAC and put them in a list
		
		for result in mac_list_temp:
		#search for mac
			mac=re.compile(regex_mac).search(result)
		
		#search for cisco mac
			mac_cisco=re.compile(regex_cisco_mac).search(result)
	
		#search for interface
			int=re.compile(regex_int).search(result)
			
		#Create mac and int list
			if mac:
				mac_list.append(result)
			if mac_cisco:
				mac_list.append(result)
			if int:
				mac_list.append(result)
	# work on MAC list to find the mac address of IP address
	position=0
	final_result=[]
	for mac_in_list in mac_list:
		#position=position+1
		# Find hostname
		mac=re.compile(regex_cisco_mac).search(mac_in_list)
		int=re.compile(regex_int).search(mac_in_list)
		ip=re.compile(regex_ip).search(mac_in_list)
		if not mac and not int and not ip:
			hostname=mac_in_list
		# if mac in the list
		for macs in wantedmac:
			if mac_in_list==macs:
				final_result.append(hostname+" --> "+mac_list[position-1]+" --> "+mac_list[position]+" --> "+mac_list[position+1])
		position=position+1
	return final_result
	 
	# Script did not find the wanted IP"
	
if __name__ == "__main__":
	#pop what is in args
	for arg in sys.argv:
		provided_mac=arg
		print("mac address ",provided_mac," is : ",get_mac_interface(provided_mac))