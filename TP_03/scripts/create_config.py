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


def create_config_cpe_lyon_batA():
    r1_data = load_json_data_from_file("data/R1_CPE_LYON_BAT_A.json")
    r1_conf = render_network_config("vlan_router.j2", r1_data)
    r1_conf += render_network_config("vrrp_router.j2", r1_data)
    print("------- CONFIG R1 BAT B -------", r1_conf)
    r2_data = load_json_data_from_file("data/R2_CPE_LYON_BAT_A.json")
    r2_conf = render_network_config("vlan_router.j2", r2_data)
    r2_conf += render_network_config("vrrp_router.j2", r2_data)
    print("------- CONFIG R2 BAT B -------", r2_conf)

    esw1_data = load_json_data_from_file("data/ESW1_CPE_LYON_BAT_A.json")
    esw1_conf = render_network_config("vlan_switch.j2", esw1_data)
    print("------- CONFIG ESW1 BAT B -------", esw1_conf)

    return {
        "r1": r1_conf,
        "r2": r2_conf,
        "esw1": esw1_conf
    }
    pass


def create_config_cpe_lyon_batB(): 
    r1_data = load_json_data_from_file("data/R1_CPE_LYON_BAT_B.json")
    r1_conf = render_network_config("vlan_router.j2", r1_data)
    r1_conf += render_network_config("vrrp_router.j2", r1_data)
    print("------- CONFIG R1 BAT B -------", r1_conf)
    r2_data = load_json_data_from_file("data/R2_CPE_LYON_BAT_B.json")
    r2_conf = render_network_config("vlan_router.j2", r2_data)
    r2_conf += render_network_config("vrrp_router.j2", r2_data)
    print("------- CONFIG R2 BAT B -------", r2_conf)

    esw1_data = load_json_data_from_file("data/ESW1_CPE_LYON_BAT_B.json")
    esw1_conf = render_network_config("vlan_switch.j2", esw1_data)
    print("------- CONFIG ESW1 BAT B-------", esw1_conf)

    return {
        "r1": r1_conf,
        "r2": r2_conf,
        "esw1": esw1_conf
    }
    pass
    
if __name__ == "__main__":
    """
        process question 3 to 5:
    """
    #question 3:
    config = create_config_cpe_lyon_batA()


    #question 4:
    save_built_config('config/R1_CPE_LYON_BAT_A.conf', config.get('r1'))
    save_built_config('config/R2_CPE_LYON_BAT_A.conf', config.get('r2'))
    save_built_config('config/ESW1_CPE_LYON_BAT_A.conf', config.get('esw1'))

    #question 5:
    config = create_config_cpe_lyon_batB()
    save_built_config('config/R1_CPE_LYON_BAT_B.conf', config.get('r1'))
    save_built_config('config/R2_CPE_LYON_BAT_B.conf', config.get('r2'))
    save_built_config('config/ESW1_CPE_LYON_BAT_B.conf', config.get('esw1'))
    