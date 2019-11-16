from netmiko import ConnectHandler
import re
import sys
import time

def get_mac_from_ip(wantedip):
	
	#IP address regex
	regex_ip = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

	# Mac address Regex
	regex_mac='([a-fA-F0-9]{2}[:|\-]?){6}'
	regex_cisco_mac='([a-fA-F0-9]{4}[:|\-.]?){3}'

	# Interface Regex
	regex_int='^(TenGigabitEthernet|GigabitEthernet|Port-Channel|ethernet|Ethernet|Tunnel|Null|Vlan|Serial|Bundle-Ether)\d+[/]?[\d+]?[/]?[\d+]?[\.]?[\d+]?[/]?[\d+]?[/]?[\d+]?[:]?[\d+]?$'
	
	#Define SSH parameters
	ssh_port="22"
	username="admin"
	password="admin"
	device_ty="cisco_ios"

	# Define IP and mac list     
	ip_and_mac_list=[]

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
			device_hostname=ch.send_command("sh run | s hostname")
		# show ip arp
			arp_table=ch.send_command("show ip arp")
		
		hostname=device_hostname.split(" ")
		hostname.remove("hostname")
		ip_and_mac_list.append(hostname[0])
				
                                    
			
		
		
		# Remove \n to keep interface
		arp_table=arp_table.replace('\n',' ')
			
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
	
		#search for interface
			int=re.compile(regex_int).search(result)
		#Create ip, mac and int list
			if ip:
				ip_and_mac_list.append(result)
			if mac:
				ip_and_mac_list.append(result)
			if mac_cisco:
				ip_and_mac_list.append(result)
			if int:
				ip_and_mac_list.append(result)
	
	# work and IP and MAC list to find the mac address of IP address
	position=0
	for ip_in_list in ip_and_mac_list:
		position=position+1
		# Find hostname
		ip=re.compile(regex_ip).search(ip_in_list)
		mac=re.compile(regex_cisco_mac).search(ip_in_list)
		int=re.compile(regex_int).search(ip_in_list)
		if not ip and not mac and not int:
			hostname=ip_in_list
		# if IP in the list
		if ip_in_list==wantedip:
			#print("mac address table for IP ", "is : ",ip_and_mac_list[position])
			return hostname+"-"+ip_and_mac_list[position]+"-"+ip_and_mac_list[position+1]
	# Script did not find the wanted IP"
	return "0"
if __name__ == "__main__":
	#pop what is in args
	for arg in sys.argv:
		provided_ip=arg
		print("mac address table for IP ",provided_ip," is : ",get_mac_from_ip(provided_ip))