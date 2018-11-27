# coding: utf-8



class ParsedIptables(object):
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
    def __init__(self, iptables, file=False):
        rules = []
        self.iptables_raw_lines = self._load_iptables(iptables, file=file)

    def _load_iptables(self, iptables, file=False):
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

    def _parse_iptables(iptables_list):
        return parsed_iptables


if __name__ == '__main__':