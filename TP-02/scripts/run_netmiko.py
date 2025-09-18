import json
from netmiko import ConnectHandler
from pathlib import Path


def question_9(net_connect):
    print ('---Question 9---')
    print(net_connect)
    print(net_connect.__dict__)
    print("\ndevice type :", net_connect.device_type, "| ip :", net_connect.host)



def question_10(net_connect):
    print ('---Question 10---')
    command = "show ip int brief"
    with ConnectHandler(**r01) as net_connect:
        output = net_connect.send_command(command)
    print()
    print(output)
    print()
    net_connect.disconnect()


def question_11(net_connect):
    print ('---Question 11---')
    command = "show ip int brief"
    with ConnectHandler(**r01) as net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
    print()
    print(output)
    print()
    net_connect.disconnect()



def question_12(net_connect):
    pass

def question_13(net_connect):
    print ('---Question 13---')
    command = "show ip route"
    with ConnectHandler(**r01) as net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
    print()
    print(output)
    print()
    net_connect.disconnect()


def question_14(net_connect):
    print ('---Question 14---')
    command_interfaces = "show ip route"
    command_conf= "show running-config interface"
    interfaces = net_connect.send_command("show ip interface brief", use_textfsm=True)
    for row in interfaces:
        name   = row.get("interface")        
        print(f"{name}")
        command_conf = net_connect.send_command(f"show running-config interface {name}")
        print(f"\n=== {name} ===\n{command_conf}\n")
   

def question_15(net_connect):
    print ('---Question 15---')
    command = [
    "interface Loopback1",
    "ip address 192.168.1.1 255.255.255.255",
    'description "loopback interface from netmiko"',
    ]

    output = net_connect.send_config_set(command)
    print(output)
    print("\n--- Verif conf de l'interface loopback ---")
    check = net_connect.send_command("show run interface Loopback1")
    print(check)
    print("\n--- Sauvegarde de la config ---")
    save = net_connect.save_config()   
    print(save)

def question_16(net_connect):
    print ('---Question 16---')
    remove_command = [
    "no interface Loopback1"
    ]

    print("\n--- Suppression de Loopback1 ---")
    remove = net_connect.send_config_set(remove_command)
    print(remove)


def question_17(net_connect):
    file = "config/loopback_R01.conf"
    output = net_connect.send_config_from_file(file)
    print (output)
    output += net_connect.save_config()



def get_inventory(file="inventory/hosts.json"):
    with open(file, "r") as f:
        inventory = json.load(f)
    return inventory


def question_20(file="inventory/hosts.json"):
    with open(file, "r") as f:
        inventory = json.load(f)
    return inventory


def question_21(file="inventory/hosts.json"):
    with open(file) as f:
        hosts = json.load(f)

    for dev in hosts:
        if dev["hostname"].startswith("R"):
            print(f"\n--- {dev['hostname']} ({dev['ip']}) ---")
            with ConnectHandler(
                device_type=dev["device_type"],
                host=dev["ip"],
                username=dev["username"],
                password=dev["password"]
            ) as conn:
                print(conn.send_command("show running-config interface GigabitEthernet0/0.99"))

    print("\n--- Fin ---")

def question_22(inventory="inventory/hosts.json"):
    targets = {"R2", "R3", "ESW2", "ESW3"}

    with open(inventory) as f:
        hosts = {h["hostname"]: h for h in json.load(f)}

    print("\n=== Déploiement R2, R3, ESW2, ESW3 ===\n")

    for hn in targets:
        dev = hosts.get(hn)
        if not dev:
            print(f"[SKIP] {hn} absent de l'inventory")
            continue

        conf_file = f"config/vlan_{hn}.conf"
        if not Path(conf_file).exists():
            print(f"[ERREUR] {hn} : fichier introuvable -> {conf_file}")
            continue

        print(f"\n--- {hn} ({dev['ip']}) ---")
        with ConnectHandler(**{
            "device_type": dev["device_type"],
            "host": dev["ip"],
            "username": dev["username"],
            "password": dev["password"],
        }) as conn:
            try:
                conn.enable()
            except Exception:
                pass
            print(conn.send_config_from_file(conf_file))
            print(conn.save_config())

    print("\n=== Fin du déploiement ===\n")

if __name__ == "__main__":    
    r01 = {
        'device_type': 'cisco_ios',
        'host':   '172.16.100.126',
        'username': 'cisco',
        'password': 'cisco'
    }
    
    net_connect = ConnectHandler(**r01)




    #question_9(net_connect)
    #question_10(net_connect)
    #question_11(net_connect)
    #question_12(net_connect)
    #question_13(net_connect)
    #question_14(net_connect)
    #question_15(net_connect)
    #question_16(net_connect)
    #question_17(net_connect)
    #hosts = get_inventory()
    # print(hosts)
    #question_20()
    #question_21()
    question_22()