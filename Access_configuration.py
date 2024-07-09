from netmiko import ConnectHandler

access1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.191",
    "username": "admin",
    "password": "cisco",
    "fast_cli": True,
    'session_log': 'session_log_access-1.txt',
    'secret': 'cisco',
    "conn_timeout": 10,
}

access2 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.192",
    "username": "admin",
    "password": "cisco",
    "fast_cli": True,
    'session_log': 'session_log_access-2.txt',
    'secret': 'cisco',
    "conn_timeout": 10
}



configurations_access1 = [
        'hostname SW-ACCESS-1',
        'vtp domain cisco123', # set vtp domain-name
        'vlan 10',
        'name NhanVien',
        'interface e0/0',
        'switchport mode access',
        'switchport access vlan 10', # create VLAN
        'int range e0/1-2',
        'switchport trunk encap dot1q',
        'switchport mode trunk',
        # 'sw trunk allow vlan 10,20', # encapsulation and allow vlan
        'spanning-tree mode rapid', # spanning tree config
        'int e0/0',
        'spanning-tree portfast',
        'spanning-tree bpduguard enable',

    ]

configurations_access2 = [
        'hostname SW-ACCESS-2',
        'vtp domain cisco123', # set vtp domain-name
        'vlan 20',
        'name IT',
        'interface e0/0',
        'switchport mode access',
        'switchport access vlan 20', # create VLAN
        'int range e0/1-2',
        'switchport trunk encap dot1q',
        'switchport mode trunk',
        # 'sw trunk allow vlan 10,20', # trunk encapsulation and allow vlan
        'spanning-tree mode rapid', # spanning-tree config
        'int e0/0',
        'spanning-tree portfast',
        'spanning-tree bpduguard enable', # enable bpduguard
    ]

def configure_device(device, commands):
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    output = net_connect.send_config_set(commands)
    # save_config = net_connect.save_config()
    print(output)
    # print('Saving configuration')
    # print(save_config)
    net_connect.disconnect()

configure_device(access1, configurations_access1)
configure_device(access2, configurations_access2)

print ('Config successfully !')

