from netmiko import ConnectHandler


gateway1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.177",
    "username": "admin",
    "password": "cisco",
    "fast_cli": True,
    'session_log': 'session_log_gateway-1.txt',
    'secret': 'cisco',
    "conn_timeout": 10,
}

gateway2 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.178",
    "username": "admin",
    "password": "cisco",
    "fast_cli": True,
    'session_log': 'session_log_gateway-2.txt',
    'secret': 'cisco',
    "conn_timeout": 10,
}

routers = [gateway1, gateway2]

configurations_gateway1 =  [
        'hostname GATEWAY-1',
        'int e0/0',
        'ip add 172.16.10.1 255.255.255.0',
        'no shut',
        'int e0/1',
        'ip add 172.16.12.2 255.255.255.0',
        'no shut', # config interface
        # 'int e0/0',
        # 'standby 1 ip 172.16.10.10',
        # 'standby 1 priority 120',
        # 'standby 1 preempt',
        # 'int e0/1',
        # 'standby 1 ip 172.16.12.10',
        # 'standby 1 priority 120',
        # 'standby 1 preempt', # HSRP Config
        'router ospf 1',
        'network 172.16.10.0 0.0.0.255 area 0',
        'network 172.16.12.0 0.0.0.255 area 0', # config OSPF 
        'default-information originate', # broadcast IP route using OSPF
        'ip route 0.0.0.0 0.0.0.0 192.168.1.2', # set ip nexthop .2
        'access-list 1 permit any',
        'ip nat inside source list 1 interface e0/2 overload',
        'int e0/2',
        'ip nat outside',
        'int range e0/0-1',
        'ip nat inside',


    ]

configurations_gateway2 =  [
        'hostname GATEWAY-2',
        'int e0/0',
        'ip add 172.16.15.5 255.255.255.0',
        'no shut',
        'int e0/1',
        'ip add 172.16.14.1 255.255.255.0',
        'no shut', # config interface
        # 'int e0/0',
        # 'standby 1 ip 172.16.12.10',
        # 'standby 1 preempt',
        # 'int e0/1',
        # 'standby 1 ip 172.16.10.10',
        # 'standby 1 preempt',
        'router ospf 1',
        'network 172.16.14.0 0.0.0.255 area 0',
        'network 172.16.15.0 0.0.0.255 area 0', 
        'default-information originate', # broadcast IP route using OSPF
        'ip route 0.0.0.0 0.0.0.0 192.168.1.2', # set ip nexthop .2
        'access-list 1 permit any',
        'ip nat inside source list 1 interface e0/2 overload',
        'int e0/2',
        'ip nat outside',
        'int e0/0',
        'ip nat inside',
        'int e0/1',
        'ip nat inside', # config NAT

    ]

def configure_device(device, commands):
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    output = net_connect.send_config_set(commands)
    # save_config = net_connect.save_config()
    # print('Saving configuration')
    # print(save_config)
    print(output)
    net_connect.disconnect()


configure_device(gateway1, configurations_gateway1)
configure_device(gateway2, configurations_gateway2)

print ('Config successfully !')






