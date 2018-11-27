# coding: utf-8


RULE_OPTIONS = {
    "-A": "method",
    "-I": "method",
    "-D": "method",
    "-p": "protocol",
    "--protocol": "protocol",
    "-s": "source",
    "--source": "source",
    "-d": "destination",
    "--destination": "destination",
    "--dport": "ports",
    "-i": "in-interface",
    "--in-interface": "in-interface",
    "-o": "out-interface",
    "--out-interface": "out-interface",
    "-j": "target",
    "--jump": "target",
    "--reject-with": "reject-with",
}

MODULE_NO_EXT = ["tcp"]


class Rule(object):
    """
    每一条rule有如下属性：

    type=table_name,comment,policy,rule,end
    raw=string of iptables rule
    seq=line NO.

    chain=INPUT,PREROUTING,FORWARD,OUTPUT,POSTROUTING
    method=ADD,INSERT
    source=source_ip
    destination=dest_ip
    protocol=tcp,udp,icmp
    dport=ports
    modules={module_name: {setting_name: value}, ...}
    target=DROP,ACCEPT,REJECT,LOG
    """
    def __init__(self, rule):
        # 判断类型
        # # 开头是comment
        # * 开头是table-name
        # : 开头是policy
        # - 开头是rule
        # COMMIT 开头是end
        rule = rule.strip()
        self.raw = rule
        self.error = False

        if rule.startswith("#"):
            self.type = "comment"
        elif rule.startswith("*"):
            self.type = "table_name"
            self._parse_rule_table_name()
        elif rule.startswith(":"):
            self.type = "policy"
            self._parse_rule_policy()
        elif rule.startswith("-"):
            self.type = "rule"
            self._parse_rule()
        elif rule == "COMMIT":
            self.type = "end"
        else:
            self.error = "ERROR: format error: [%s]" % rule
            print(self.error)

    def _parse_rule_table_name(self):
        table_name = self.raw.split("*")
        if len(table_name) is not 2:
            self.error = "ERROR: table's name [%s] is wrong" % self.raw
        else:
            self.table_name = table_name[1]

    def _parse_rule_policy(self):
        policy = self.raw.split(":")[1].split()
        if len(policy) is not 3:
            self.error = "ERROR: policy [%s] is wrong" % self.raw
        else:
            self.table = policy[0]
            self.policy = policy[1]

    def _parse_rule(self):
        rule = self.raw.split()
        match_rule = {}
        match=False
        skip_loop=0
        for i in range(len(rule)):

            if skip_loop > 0:
                skip_loop -= 1
                continue

            if match:
                if rule[i] not in MODULE_NO_EXT:
                    for j in range(len(rule)-i):
                        if not (rule[i+j].startswith("-") and not rule[i+j].startswith("--")):
                            match_rule.setdefault(rule[i], []).append(rule[i+j])
                        else:
                            break
                    skip_loop = len(match_rule[rule[i]])-1
                    setattr(self, rule[i], match_rule)
                match = False
            elif rule[i].startswith("-m"):
                match=True
            else:
                #self.__dict__[RULE_OPTIONS[rule[i]]] = rule[i+1]
                setattr(self, RULE_OPTIONS[rule[i]], rule[i+1])
                skip_loop=1



class Iptables(object):
    def __init__(self, iptables, file=False):
        self.rules = []
        self.iptables_raw_lines = self._load_iptables(iptables, file=file)
        self._parse_iptables()

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
                print("iptables file: %s open failed. \nError: %s\n" % (iptables, e))
                result_list = []

        return result_list

    def _parse_iptables(self):
        for rule in self.iptables_raw_lines:
            self.rules.append(Rule(rule))

    @staticmethod
    def parse_iptables(iptables, file=False):
        iptables = Iptables(iptables, file=file)
        return iptables



if __name__ == '__main__':
    iptables = Iptables.parse_iptables("/vagrant/iptables-parser/iptables-template", file=True)
    for i in iptables.rules:
        if (not hasattr(i, "set")
            and i.type is "rule"
            and not hasattr(i, "reject-with")):
            print i.raw