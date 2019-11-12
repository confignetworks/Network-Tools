from netmiko import ConnectHandler
import re
import sys

def get_mac_from_ip(ip):
	#pop what is in args
	#for arg in sys.argv:
	#	provided_ip=arg

	#IP address regex
	regex_ip = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

	# Mac address Regex
	regex_mac='([a-fA-F0-9]{2}[:|\-]?){6}'
	regex_cisco_mac='([a-fA-F0-9]{4}[:|\-.]?){3}'

	#Define SSH parameters
	ssh_port="22"
	username="admin"
	password="admin"
	device_ty="cisco_ios"

	# Define IP and mac list     
	ip_and_mac_list=[]

	#Bring IP address from IP file 
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
		# show ip arp                                    
			arp_table=ch.send_command("show ip arp")
		# Create arp table list    
			arp_list=arp_table.split(" ")
		#search IPs and MAC and put them in a dictionnary 
			for result in arp_list:
		#search for IP
				ip=re.compile(regex_ip).search(result)
		#search for mac
				mac=re.compile(regex_mac).search(result)
		#search for cisco mac
				mac_cisco=re.compile(regex_cisco_mac).search(result)
		#Create ip and mac list
				if ip:
					ip_and_mac_list.append(result)
				if mac:
					ip_and_mac_list.append(result)
				if mac_cisco:
					ip_and_mac_list.append(result)

					
	# work and IP and MAC list to find the mac address of IP address
	position=0
	for ip_in_list in ip_and_mac_list:
		position=position+1
		if ip_in_list==provided_ip:
			print("mac address table for IP ", "is : ",ip_and_mac_list[position])
			return ip_and_mac_list[position]