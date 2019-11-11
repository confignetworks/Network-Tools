from netmiko import ConnectHandler


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
        show_interface_config_temp = "show running-config interface {}"

    # Create desired CLI command and send to device
        command = show_interface_config_temp.format("gi3")
        interface = ch.send_command(command)
        arp=ch.send_command("show ip arp")

    # Print the raw command output to the screen
        print(interface)				
        print (arp)
				
