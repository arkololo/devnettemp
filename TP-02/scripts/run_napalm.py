import json
from napalm import get_network_driver
import os
from jinja2 import Environment, FileSystemLoader
from napalm import get_network_driver



def get_inventory(path="inventory/hosts.json"):
    with open(path, "r") as f:
        return json.load(f)
    pass



def get_json_data_from_file(file):
    if file.lower().endswith(".json"):
        with open(file) as f:
            return json.load(f)
    elif file.lower().endswith((".yml", ".yaml")):
        try:
            import yaml
        except ImportError:
            raise RuntimeError("PyYAML n'est pas installé: pip install pyyaml")
        with open(file) as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Format de fichier non supporté (utilise .json, .yml ou .yaml)")
    pass

def question_26(device):
    print('--- Question 26 ---')

    r01 = {
        'hostname':'172.16.100.126',
        'username': "cisco",
        'password': "cisco"
    }

    driver = get_network_driver('ios')
    device = driver(**r01)
    device.open()
    pass


def question_27(device):
    print('--- Question 27 ---')
    out = device.cli(["show ip interface brief"])
    print(out)
    pass


def question_28(device):
    pass

def question_29(device):
    print('--- Question 29 ---')
    arp_table = device.get_arp_table()
    print(arp_table)


def question_30(device):
    pass


def question_31():
    cfg_path = "config/R01.conf"
    print("--- Question 31 ---")

    try:
        # Charger le fichier de config
        device.load_merge_candidate(filename=cfg_path)

        # Afficher les changements
        diff = device.compare_config()
        if diff:
            print("=== CHANGEMENTS À APPLIQUER ===")
            print(diff)
            device.commit_config()
            print("[OK] Commit effectué.")
        else:
            print("Aucun changement détecté.")
            device.discard_config()

    except Exception as e:
        print(f"[ERREUR] {e}")
        try:
            device.discard_config()
        except Exception:
            pass


def question_32():
    print("--- Question 32 ---")

    template_dir = "templates"
    template_name = "ospf.j2"

    data = get_json_data_from_file("data/ospf.yaml")

    # Préparer Jinja2
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    tpl = env.get_template(template_name)

    os.makedirs("config", exist_ok=True)

    # Rendu pour chaque routeur
    routers = data.get("routers", [])
    if not routers:
        raise ValueError("Aucune entrée 'routers' dans le fichier de données.")

    print("\n--- Génération des configurations OSPF ---\n")
    for r in routers:
        rendered = tpl.render(**r)
        out_file = f"config/ospf_{r['hostname'].lower()}.conf"
        with open(out_file, "w") as f:
            f.write(rendered)
        print(f"-> {out_file}")

    print("\n--- Terminé ---\n")
    pass


def question_33():
    print("--- Question 33 ---")

    for hn, ip in [("R1", "172.16.100.126"), ("R2", "172.16.100.190"), ("R3", "172.16.100.254")]:
        driver = get_network_driver("ios")
        device = driver(hostname=ip, username="cisco", password="cisco")
        device.open()
        device.load_merge_candidate(filename=f"config/ospf_{hn.lower()}.conf")
        print(device.compare_config())
        device.commit_config()
        device.close()
    pass

def question_35(inventory_path="inventory/hosts.json"):
    os.makedirs("config/backup", exist_ok=True)
    hosts = get_inventory(inventory_path)

    print("\n=== Backups NAPALM ===\n")
    for dev in hosts:
        hn, ip, user, pwd = dev["hostname"], dev["ip"], dev["username"], dev["password"]

        driver = get_network_driver("ios")
        device = driver(hostname=ip, username=user, password=pwd)

        try:
            device.open()
            cfg = device.get_config()          
            running = cfg.get("running", "")
            out_path = f"config/backup/{hn}.bak"
            with open(out_path, "w") as f:
                f.write(running)
            print(f"[OK] {hn} -> {out_path}")
        except Exception as e:
            print(f"[ERREUR] {hn}: {e}")
        finally:
            try:
                device.close()
            except Exception:
                pass

    print("\n=== Fin des backups ===\n")
    pass

def test_co_esw1() :
    esw1 = {
        "hostname": "172.16.100.125",
        "username": "cisco",
        "password": "cisco"
    }

    driver = get_network_driver("ios")
    device = driver(**esw1)
    device.open()

if __name__ == "__main__":
    r01 = {
        'hostname':'172.16.100.126',
        'username': "cisco",
        'password': "cisco"
    }

    driver = get_network_driver('ios')
    device = driver(**r01)
    device.open()

    
    
    question_26(device)
    question_27(device)
    question_28(device)
    question_29(device)
    question_30(device)
    question_31()
    question_32()
    question_33()
    question_35()
    #test_co_esw1()
