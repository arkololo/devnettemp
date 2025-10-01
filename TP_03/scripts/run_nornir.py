from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command, netmiko_save_config, netmiko_commit




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
    print("\n------ R1 A et B -----")

    r1 = nr.filter(name__in=["R1-CPE-BAT-A", "R1-CPE-BAT-B"])
    result = r1.run(
        task=napalm_configure,
        configuration="""
    interface Loopback1
    ip address 1.1.1.1 255.255.255.255
    no shutdown
    """
    )
    print_result(result)

    print("\n------ R2 A et B -----")

    r2 = nr.filter(name__in=["R2-CPE-BAT-A", "R2-CPE-BAT-B"])
    result = r2.run(
        task=napalm_configure,
        configuration="""
    interface Loopback1
    ip address 2.2.2.2 255.255.255.255
    no shutdown
    """,     
        dry_run=False          
    )
    print_result(result)

def question_35(nr):
    pass

def question_36(nr):
    pass

def question_37(nr):
    pass

def question_38(nr):
    pass

def question_39(nr):
    pass

def question_39_d(nr):
    pass

def question_40(nr):
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
    #question_39_d(nr)

    #question_40(nr)
    pass
