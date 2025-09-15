from pathlib import Path
import json
from jinja2 import Template, Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("templates"))
import yaml



def load_json_data_from_file(file_path):
    """
        A compléter ....
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"erreur le fichier '{file_path}' est introuvable.")
        return None
    except json.JSONDecodeError as e:
        print(f"erreur le fichier '{file_path}' n'est pas un JSON valide : {e}")
        return None
    pass


def load_yaml_data_from_file(file_path):
    """
        A compléter ....
    """
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
    """
        A compléter ....
    """
    template = env.get_template(template_name)
    return template.render(**data)
    


def save_built_config(file_name, data):
    """
        A compléter ....
    """
    out_dir = Path("config")
    out_dir.mkdir(parents=True, exist_ok=True)   # crée le dossier s'il n'existe pas

    out_path = out_dir / file_name
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"Configuration sauvegardée dans {out_path}")
    pass


if __name__ == "__main__":

    #process R2
    # r2_data = load_json_data_from_file(file_path='data/R2.json')
    # r2_config = render_network_config(template_name='R2.j2', data=r2_data)
    # save_built_config('config/R2.conf', r2_config)

    #process ESW2
    # esw2_data = load_json_data_from_file(file_path='data/ESW2.json')
    # esw2_config = render_network_config(template_name='ESW2.j2', data=esw2_data)
    # save_built_config('config/ESW2.conf', esw2_config)

    #json
    esw2_data = load_json_data_from_file("data/ESW2.json")
    esw2_config = render_network_config("ESW2.j2", esw2_data)
    save_built_config("ESW2.conf", esw2_config)
    
    r2_data = load_json_data_from_file("data/R2.json")
    r2_config = render_network_config("R2.j2", r2_data)
    save_built_config("R2.conf", r2_config)

    

    #yaml
    r2_data = load_yaml_data_from_file("data/R2.yaml")
    r2_config = render_network_config("R2.j2", r2_data)
    save_built_config("R2_from_yaml.conf", r2_config)

    esw2_data = load_yaml_data_from_file("data/ESW4.yaml")  
    esw2_config = render_network_config("ESW2.j2", esw2_data)
    save_built_config("ESW4_from_yaml.conf", esw2_config)

    
    