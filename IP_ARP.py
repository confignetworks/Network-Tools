import sys
from get_mac_from_ip_function import *
#IP address regex
regex_ip = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

for arg in sys.argv:
	provided_ip=arg
	ip=re.compile(regex_ip).search(provided_ip)
	if ip:
		result=get_mac_from_ip(provided_ip)
		if result!="0":
			print("mac address table for IP ",provided_ip," is : ",get_mac_from_ip(provided_ip))
		else:
			print("IP ",provided_ip," does not exist on the network")

