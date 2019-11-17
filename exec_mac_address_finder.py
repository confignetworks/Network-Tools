import sys
from mac_address_table_interface import *
from CRC_Finded import *
#mac regex
regex_cisco_mac='([a-fA-F0-9]{4}[:|\-.]?){3}'
list_of_macs=[]
for arg in sys.argv:
	ip=re.compile(regex_cisco_mac).search(arg)
	if ip:
		list_of_macs.append(arg)

result_list=get_mac_interface(list_of_macs)
if len(result_list)>0:
	for result in result_list:
		print(result)
		crc_input=result.split("-->")
		print(crc_finded(crc_input[0],crc_input[1],crc_input[3]))
else:
	print("mac ",list_of_macs," does not exist on the network")
	
