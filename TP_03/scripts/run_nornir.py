from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command, netmiko_save_config, netmiko_commit
import os
from pathlib import Path
import json
from jinja2 import Template, Environment,  FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


def load_json_data_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{file_path}' est introuvable.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erreur : le fichier '{file_path}' n'est pas un JSON valide : {e}")
        return None
    pass

def render_network_config(template_name, data):
    template = env.get_template(template_name)
    return template.render(**data)
    pass

def save_built_config(file_name, data):
    out_dir = Path()
    out_path = out_dir / file_name
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"Configuration sauvegardée dans {out_path}")
    pass


def question_13(nr):
    print("\n------ QUESTION 13 -----")
    print(nr.__dict__)
    pass

def question_14(nr):
    print("\n------ QUESTION 14 -----")
    print(nr.inventory.hosts)
    pass

def question_15(nr):
    print("\n------ QUESTION 15 -----")
    first = list(nr.inventory.hosts.values())[0]
    print(first)
    print(type(first))
    pass

def question_16(nr):
    print("\n------ QUESTION 16 -----")
    host = list(nr.inventory.hosts.values())[0]
    print(dir(host))
    print(host.hostname)   
    print(host.username)
    print(host.password)


    pass

def question_17(nr):
    print("\n------ QUESTION 17 -----")
    host = list(nr.inventory.hosts.values())[0]
    print(dir(host))
    pass

def question_18(nr):
    print("\n------ QUESTION 18 -----")
    host = list(nr.inventory.hosts.values())[0] 
    print(host.data.get("room"))
    pass

def question_19(nr):
    print("\n------ QUESTION 19 -----")
    print(nr.inventory.groups)
    pass

def question_20(nr):
    print("\n------ QUESTION 20 -----")
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups)
    pass

def question_21(nr):
    print("\n------ QUESTION 21 -----")
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups[0].keys())
    pass

def question_22(nr):
    print("\n------ QUESTION 22 -----")
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups[0].data.get("vendor"))
    pass
def question_23(nr):
    print("\n------ QUESTION 23 -----")
    for name, host in nr.inventory.hosts.items():
        print({host.hostname})
    pass

def question_24(nr):
    print("\n------ QUESTION 24 -----")
    print(print(nr.filter(device_type="router").inventory.hosts.keys()))
    pass

def question_25(nr):
    print("\n------ QUESTION 25 -----")
    print(print(nr.filter(device_type="router_switch").inventory.hosts.keys()))
    pass

def question_26(nr):
    print("\n------ QUESTION 26 -----")
    def hello_world(task: Task) -> Result:
        return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
        )
    result = nr.run(task=hello_world)
    print(result)
    pass

def question_27(nr):
    print("\n------ QUESTION 27 -----")
    def hello_world(task: Task) -> Result:
        return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
        )
    result = nr.run(task=hello_world)
    print(type(result))

    pass

def question_28(nr):
    print("\n------ QUESTION 28 -----")
    def hello_world(task: Task) -> Result:
        return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
        )
    result = nr.run(task=hello_world)
    print_result(result)
    pass

def question_29(nr):
    pass


def question_30(nr):
    print("\n------ QUESTION 30 -----")
    def hello_world(task: Task) -> Result:
        return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
        )
    router_switch = nr.filter(device_type="router_switch")
    result = router_switch.run(task=hello_world)
    print_result(result)
    pass

def question_32(nr):
    print("\n------ QUESTION 32 -----")
    routers = nr.filter(device_type="router")
    result = routers.run(
        task=napalm_cli,
        commands=["show ip interface brief"]
    )
    print_result(result)
    pass
 
def question_33(nr):
    print("\n------ QUESTION 33 -----")
    router_switch = nr.filter(device_type="router_switch")
    result = router_switch.run(
        task=napalm_get,
        getters=["get_arp_table"]
    )
    print_result(result)
    pass

def question_34(nr):
    print("\n------ QUESTION 34 -----")

    r1 = nr.filter(name="R1-CPE-BAT-A")
    result = r1.run(
        task=napalm_configure,
        configuration=(
            "interface Loopback1\n"
            " description Q34 R1\n"
            " ip address 1.1.1.1 255.255.255.255\n"
            " no shutdown\n"
        ),
        name="Create Loopback1 on R1"
    )
    print_result(result)

    r2 = nr.filter(name="R2-CPE-BAT-A")
    result = r2.run(
        task=napalm_configure,
        configuration=(
            "interface Loopback1\n"
            " description Q34 R2\n"
            " ip address 2.2.2.2 255.255.255.255\n"
            " no shutdown\n"
        ),
        name="Create Loopback1 on R2"
    )
    print_result(result)
    
def question_35(nr):
    print("\n------ QUESTION 35 -----")
    result = nr.run(task=napalm_cli, commands=["write memory"])
    print_result(result)

    pass

def question_36(nr):
    print("\n------ QUESTION 36 -----")
    routers = nr.filter(device_type="router")
    result = routers.run(task=netmiko_send_command, command_string="show ip interface brief")
    print_result(result)
    pass

def question_37(nr):
    print("\n------ QUESTION 37 -----")
    r1 = nr.filter(name="R1-CPE-BAT-A")
    result = r1.run(task=netmiko_send_config, config_commands=[
            "interface Loopback2",
            "ip address 11.11.11.11 255.255.255.255",
            "description Loopback2 depuis Netmiko",
            "no shutdown"
        ]
    )
    print_result(result)

    r2 = nr.filter(name="R2-CPE-BAT-A")
    result = r2.run(task=netmiko_send_config, config_commands=[
            "interface Loopback2",
            "ip address 22.22.22.22 255.255.255.255",
            "description Loopback2 depuis Netmiko",
            "no shutdown"
        ]
    )
    print_result(result)
    pass

def question_38(nr):
    print("\n------ QUESTION 38 -----")
    targets = nr.filter(name__in=["R1-CPE-BAT-A", "R2-CPE-BAT-A"])
    result = targets.run(task=netmiko_save_config)
    print_result(result)
    
    pass

def question_39(nr):
    files = {
        "R1-CPE-BAT-A":  "config/R1_CPE_LYON_BAT_A.conf",
        "R1-CPE-BAT-B":  "config/R1_CPE_LYON_BAT_B.conf",
        "R2-CPE-BAT-A":  "config/R2_CPE_LYON_BAT_A.conf",
        "R2-CPE-BAT-B":  "config/R2_CPE_LYON_BAT_B.conf",
        "ESW1-CPE-BAT-A":"config/ESW1_CPE_LYON_BAT_A.conf",
        "ESW1-CPE-BAT-B":"config/ESW1_CPE_LYON_BAT_B.conf",
    }

    print("\n=== Déploiement des configurations (A & B) ===\n")

    # déploiement + sauvegarde host par host (pas de fonction imbriquée)
    for host, path in files.items():
        if not os.path.exists(path):
            print(f"[SKIP] {host}: fichier absent -> {path}")
            continue

        print(f"\n--- {host}  <-  {path} ---")
        # push de la config depuis fichier
        res_push = nr.filter(name=host).run(task=netmiko_send_config,config_file=path)
        print_result(res_push)

        # sauvegarde (write memory / équivalent)
        res_save = nr.filter(name=host).run(task=netmiko_save_config)
        print_result(res_save)

    print("\n=== Fin du déploiement ===\n")
    pass

def question_39_d(nr):
    pairs = {
        "BAT-A": ("R1-CPE-BAT-A", "R2-CPE-BAT-A"),
        "BAT-B": ("R1-CPE-BAT-B", "R2-CPE-BAT-B"),
    }

    print("\n=== TEST VRRP SIMPLE ===\n")

    for bldg, (h1, h2) in pairs.items():
        out = {}
        for host in (h1, h2):
            res = nr.filter(name=host).run(
                task=netmiko_send_command,
                command_string="show vrrp brief"
            )
            out[host] = res[host][0].result if host in res else ""
            print(f"\n--- {host} :: show vrrp brief ---\n{out[host]}\n")

        # vérif très basique
        text_all = out[h1] + out[h2]
        if "Master" in text_all and "Backup" in text_all:
            print(f"[{bldg}] VRRP HA OK (Master/Backup présents)")
        else:
            print(f"[{bldg}] VRRP HA NON CONFORME")

    print("\n=== FIN TEST VRRP ===\n")
    pass

def question_40(nr):
    data = load_json_data_from_file("data/ospf.json")
    if not data or "routers" not in data:
        print("[ERREUR] data/ospf.json manquant ou invalide (clé 'routers').")
        return

    Path("config").mkdir(exist_ok=True)
    host_to_file = {}
    for r in data["routers"]:
        cfg = render_network_config("ospf.j2", r)
        out_path = f"config/ospf_{r['hostname']}.conf"
        save_built_config(out_path, cfg)
        host_to_file[r["hostname"]] = out_path

    for host, cfg_file in host_to_file.items():
        if not Path(cfg_file).exists():
            print(f"[SKIP] {host}: fichier introuvable -> {cfg_file}")
            continue

        print(f"\n--- Déploiement OSPF {host}  <-  {cfg_file} ---")
        res_push = nr.filter(name=host).run(task=netmiko_send_config,config_file=cfg_file,cmd_verify=False,delay_factor=2,)      
        print_result(res_push)

        res_save = nr.filter(name=host).run(task=netmiko_save_config)
        print_result(res_save)

    print("\n=== Question 40 : génération + déploiement OSPF terminés ===\n")
    pass
    


if __name__ == "__main__":
    nr = InitNornir(config_file="inventory/config.yaml")

    question_13(nr)
    question_14(nr)
    question_15(nr)
    question_16(nr)
    question_17(nr)
    question_18(nr)
    question_19(nr)
    question_20(nr)
    question_21(nr)
    question_22(nr)
    question_23(nr)
    question_24(nr)
    question_25(nr)
    question_26(nr)
    question_27(nr)
    question_28(nr)
    question_29(nr)
    question_30(nr)

    question_32(nr)
    question_33(nr)
    question_34(nr)
    question_35(nr)
    question_36(nr)
    question_37(nr)
    question_38(nr)
    question_39(nr)
    question_39_d(nr)

    question_40(nr)
    pass
