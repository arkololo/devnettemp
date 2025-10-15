from flask import Flask, jsonify, request, abort, make_response, send_file
from werkzeug.exceptions import HTTPException
import json
from nornir import InitNornir
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)

ALLOWED_EXTENSIONS = {'conf'}
UPLOAD_FOLDER = 'fastprod/upload_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def init_nornir():
    app.config['nr'] = InitNornir(config_file="fastprod/inventory/config.yaml")

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



init_nornir()


from services.devices import (get_inventory, add_device, get_device_by_name, delete_device, get_device_interfaces, get_device_interfaces_ip, get_device_facts)
from services.config import (get_config_by_device)
from services.tasks import (run_show_commands_by_device, run_config_commands_by_device, run_config_from_file_by_device)
from services.snapshots import (create_snapshot_by_device, get_snapshots_by_device, get_snapshot_by_name)


@app.route("/")
def hello_world():
    return jsonify({
        "env": "DEV",
        "name": "fastprod_backend",
        "version": 1.0
    })

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
    "code": e.code,
    "name": e.name,
    "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/devices", methods=['GET', 'POST'])
def devices():
    if request.method == 'GET':
        devices = get_inventory()
        return jsonify(devices = devices, total_count=len(devices))
    
    if request.method == 'POST':
        data = request.get_json()
        new_device = add_device(data)
        return jsonify(device=new_device)


@app.route("/devices/<device_name>", methods=['GET', 'DELETE'])
def device_by_name(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        return jsonify(device=device)
    if request.method == 'DELETE':
        device = get_device_by_name(device_name)
        delete_device(device)
        return jsonify(message="Device deleted")


@app.route("/devices/<device_name>/interfaces", methods=['GET'])
def get_interfaces(device_name):
    device = get_device_by_name(device_name)
    interfaces = get_device_interfaces(device)
    return jsonify(interfaces=interfaces)

@app.route("/devices/<device_name>/interfaces/ip", methods=['GET'])
def get_interfaces_ip(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        interfaces_ip = get_device_interfaces_ip(device)
        return jsonify(interfaces_ip=interfaces_ip)

@app.route("/devices/<device_name>/facts", methods=['GET'])
def get_facts(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        facts = get_device_facts(device)
        return jsonify(facts=facts)

@app.route("/devices/<device_name>/config", methods=['GET', 'POST'])
def get_config(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        config = get_config_by_device(device)
        return jsonify(config=config)
    if request.method == 'POST':
        device = get_device_by_name(device_name)             
        if request.files.to_dict(flat=False).get('config_file'):
            file = request.files.get('config_file')
            if allowed_file(file.filename) is False:
                abort(make_response(jsonify(message="file extension not allowed"), 403)) 
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = run_config_from_file_by_device(device,file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(result=result)
        if request.get_json().get('mode') == 'enable':
            commands = request.get_json().get('commands')
            result = run_show_commands_by_device(device, commands=commands)
            return jsonify(result=result)
        if request.get_json().get('mode') == 'config':
            commands = request.get_json().get('commands')
            result = run_config_commands_by_device(device, commands=commands)
            return jsonify(result=result, commands=commands)

    

    
@app.route("/devices/<device_name>/snapshots", methods=['POST', 'GET'])
def snapshots(device_name):
    if request.method == 'POST':
        device = get_device_by_name(device_name)
        snap = create_snapshot_by_device(device)
        return jsonify(snap=snap)
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        snap = get_snapshots_by_device(device)
        return jsonify(snap=snap)

@app.route("/snapshots/<path:filename>", methods=['GET'])
def snapshot_by_name(filename):
    if request.method == 'GET':
        try:
            return send_file('snapshots/'+filename)
        except FileNotFoundError:
            abort(make_response(jsonify(message="snapshot not found"), 404))
