# coding: utf-8



class Iptables(object):
    """
    Iptables.rules中包含了所有rules，每一条rules有如下结构：

    type=comment,policy,rule
    raw=string of iptables rule
    seq=line NO.

    chain=input,prerouting,forward,output,postrouting
    method=add,insert
    source=source_ip
    destination=dest_ip
    protocol=tcp,udp,icmp
    dport=ports
    modules={module_name: {setting_name: value}, ...}
    target=DROP,ACCEPT,REJECT,LOG
    """
    def __init__(self):
        rules = []

    def load_iptables(iptables, file=False):
        """
        load iptables and return a list of eachline of iptables
        """
        if not file:
            if type(iptables) is list:
                result_list = iptables
        else:
            try:
                with open(iptables, "r") as f:
                    result_list = f.readlines()
            except Exception as e:
                print("iptables file: %s open failed. \nError: %s\n", % (iptable, e))
                result_list = []

        return result_list

    def parse_iptables(iptables_list):
        result_obj = Iptables()

        return result_obj