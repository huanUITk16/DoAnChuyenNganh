from netmiko import ConnectHandler


core1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.189",
    "username": "admin",
    "password": "cisco",
    "fast_cli": True,
    'session_log': 'session_log_core-1.txt',
    'secret': 'cisco',
    "conn_timeout": 10,
}

core2 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.190",
    "username": "admin",
    "password": "cisco",
    "fast_cli": True,
    'session_log': 'session_log_core-2.txt',
    'secret': 'cisco',
    "conn_timeout": 10,
}

cores = [core1, core2]

configurations = [
    [
        'hostname SW-CORE-1',
        'vlan 10',
        'name NhanVien',
        'vlan 20',
        'name IT', # create VLAN
        'ip routing',
        'no ip cef',
        'interface range e0/0-1',
        'sw trunk encap dot1q',
        'sw mode trunk',
        # 'sw trunk allow vlan 10,20', # config trunk
        'spanning-tree mode rapid',
        'spanning-tree vlan 10 root primary',
        'spanning-tree vlan 20 root primary', # config RSTP (CORE 1 is primary) 
        'int e0/2',
        'no switchport',
        'ip add 172.16.10.2 255.255.255.0',
        'no shut',
        'int e0/3',
        'no switchport',
        'ip add 172.16.14.2 255.255.255.0',
        'no shut',
        'int vlan 10',
        'ip add 192.168.10.5 255.255.255.0',
        'no shut',
        'int vlan 20',
        'ip add 192.168.20.5 255.255.255.0',
        'no shut', # config interface
        'ip dhcp pool vlan10',
        'network 192.168.10.0 255.255.255.0',
        'default-router 192.168.10.1',
        'dns 8.8.8.8',
        'exit',
        'ip dhcp exclude 192.168.10.1 192.168.10.5',
        'ip dhcp pool vlan20',
        'network 192.168.20.0 255.255.255.0',
        'default-router 192.168.20.1',
        'dns 8.8.8.8',
        'exit',
        'ip dhcp exclude 192.168.20.1 192.168.20.5', # DHCP for vlan 10 and vlan 20
        'int vlan 10',
        'standby 1 ip 192.168.10.1',
        'standby 1 priority 105',
        'standby 1 preempt',
        'int vlan 20',
        'standby 1 ip 192.168.20.1',
        'standby 1 priority 105',
        'standby 1 preempt', # Config HSRP,
        # 'int vlan 10',
        # 'standby 1 track e0/2',
        # 'int vlan 20',
        # 'standby 1 track e0/2', # Track interface for backup when interface CORE1-GW1 down
        'router ospf 1',
        'network 172.16.14.0 0.0.0.255 area 0',
        'network 172.16.10.0 0.0.0.255 area 0',
        'network 192.168.10.0 0.0.0.255 area 0',
        'network 192.168.20.0 0.0.0.255 area 0', # config OSPF

    ],

    [
        'hostname SW-CORE-2',
        'vlan 10',
        'name NhanVien',
        'vlan 20',
        'name IT', # create VLAN
        'ip routing',
        'no ip cef',
        'interface range e0/0-1',
        'sw trunk encap dot1q',
        'sw mode trunk',
        # 'sw trunk allow vlan 10,20', # config trunk
        'spanning-tree mode rapid',
        'spanning-tree vlan 10 root secondary',
        'spanning-tree vlan 20 root secondary', # config RSTP (CORE 2 is secondary) 
        'int e0/2',
        'no switchport',
        'ip add 172.16.15.6 255.255.255.0',
        'no shut',
        'int e0/3',
        'no switchport',
        'ip add 172.16.12.1 255.255.255.0',
        'no shut',
        'int vlan 10',
        'ip add 192.168.10.6 255.255.255.0',
        'no shut',
        'int vlan 20',
        'ip add 192.168.20.6 255.255.255.0',
        'no shut', # config interface
        'int vlan 10',
        'standby 1 ip 192.168.10.1',
        'standby 1 preempt',
        'int vlan 20',
        'standby 1 ip 192.168.20.1',
        'standby 1 preempt', # Config HSRP,
        'router ospf 1',
        'network 172.16.12.0 0.0.0.255 area 0',
        'network 172.16.15.0 0.0.0.255 area 0',
        'network 192.168.10.0 0.0.0.255 area 0',
        'network 192.168.20.0 0.0.0.255 area 0', # config OSPF
    ]
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

for core, config in zip(cores, configurations):
    configure_device(core, config)

print ('Config successfully !')
