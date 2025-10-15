from flask import current_app as app               
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result


def get_config_by_device(device):
    nr = app.config.get('nr')
    result = nr.filter(device_name=device.get('name')).run(task=napalm_get, getters=["get_config"])
    return result[device.get('name')][0].result.get('get_config')

