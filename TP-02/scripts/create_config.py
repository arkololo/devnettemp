from pathlib import Path
import json
from jinja2 import Template, Environment,  FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader("templates"))

#Je ne sais pas si rename cette fonction peut poser problème pour la notation
#mais ma fonction load_json, en réalité load un yaml
def load_json_data_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{file_path}' est introuvable.")
        return None
    except yaml.YAMLError as e:
        print(f"Erreur : le fichier '{file_path}' n'est pas un YAML valide : {e}")
        return None

def render_network_config(template_name, data):
    template = env.get_template(template_name)
    return template.render(**data)


def save_built_config(file_name, data):
    
    out_dir = Path()
    out_path = out_dir / file_name
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"Configuration sauvegardée dans {out_path}")


def create_vlan_config_cpe_marseille():
    esw2_data = load_json_data_from_file("data/vlan_ESW2.yaml")
    esw2_conf = render_network_config("vlan_switch.j2", esw2_data)

    r02_data = load_json_data_from_file("data/vlan_R02.yaml")
    r02_conf = render_network_config("vlan_router.j2", r02_data)
    

    return r02_conf, esw2_conf


def create_vlan_config_cpe_paris():
    esw3_data = load_json_data_from_file("data/vlan_ESW3.yaml")
    esw3_conf = render_network_config("vlan_switch.j2", esw3_data)

    r03_data = load_json_data_from_file("data/vlan_R03.yaml")
    r03_conf = render_network_config("vlan_router.j2", r03_data)

    return r03_conf, esw3_conf


if __name__ == "__main__":
    """
        process question 1 to 5:
    """
    # r02_config, esw2_config = create_vlan_config_cpe_marseille()
    # save_built_config('config/vlan_R02.conf', r02_config)
    # save_built_config('config/vlan_ESW2.conf', esw2_config)
    
    # r03_config, esw3_config = create_vlan_config_cpe_paris()
    # save_built_config('config/vlan_R03.conf', r03_config)
    # save_built_config('config/vlan_ESW3.conf', esw3_config)
    

    # Print dans le terminal avant de sauvegarder
    
    r02_config, esw2_config = create_vlan_config_cpe_marseille()
    print("\n===== CONFIG R02 (Marseille) =====\n")
    print(r02_config)
    print("\n===== CONFIG ESW2 (Marseille) =====\n")
    print(esw2_config)

    save_built_config('config/vlan_R2.conf', r02_config)
    save_built_config('config/vlan_ESW2.conf', esw2_config)


    r03_config, esw3_config = create_vlan_config_cpe_paris()
    print("\n===== CONFIG R03 (Paris) =====\n")
    print(r03_config)
    print("\n===== CONFIG ESW3 (Paris) =====\n")
    print(esw3_config)

    save_built_config('config/vlan_R3.conf', r03_config)
    save_built_config('config/vlan_ESW3.conf', esw3_config)
