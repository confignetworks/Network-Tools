from netmiko import ConnectHandler
import re

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

#Bring IP address from IP file 
with open('ip.txt','r') as ip:
   chaine=ip.read()
   liste=chaine.split("\n")
   print(liste)
# Loop for all devices

for ip in liste:
    # Open CLI connection to device
    with ConnectHandler(ip,
                        device_type=device_ty,
                        port = ssh_port,
                        username = username,
                        password = password) as ch:
                                          
    # Create a CLI command template
        #show_interface_config_temp = "show running-config interface {}"

    # Create desired CLI command and send to device
        #command = show_interface_config_temp.format("gi3")
        #interface = ch.send_command(command)
        arp_table=ch.send_command("show ip arp")
        arp_liste=arp_table.split(" ")
        print(arp_liste)
        ip_and_mac_liste=[]
	#search IPs and MAC and put them in a dictionnary 
        for result in arp_liste:
            #search for IP
            ip=re.compile(regex_ip).search(result)
            #search for mac
            mac=re.compile(regex_mac).search(result)
			#search for cisco mac
            mac_cisco=re.compile(regex_cisco_mac).search(result)
            if ip:
                ip_and_mac_liste.append(result[ip.start():ip.end()])
            if mac:
                ip_and_mac_liste.append(result[mac.start():mac.end()])
            if mac_cisco:
                ip_and_mac_liste.append(result[mac_cisco.start():mac_cisco.end()])
			
    # Print the raw command output to the screen
print (ip_and_mac_liste)
				
