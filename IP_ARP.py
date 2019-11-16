import sys
from get_mac_from_ip_function import *
#IP address regex
regex_ip = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
				25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
list_of_ips=[]
for arg in sys.argv:
	ip=re.compile(regex_ip).search(arg)
	if ip:
		list_of_ips.append(arg)

result_list=get_mac_from_ip(list_of_ips)
if len(result_list)>0:
	for result in result_list:
		print(result)
else:
	print("IP ",list_of_ips," does not exist on the network")
