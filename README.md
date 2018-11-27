## iptables parser

### 用途
用于解析iptables规则，将每一个iptables文件转化成一个Iptables对象实例。而每一个Iptables对象实例的rules属性是一个Rule对象实例的列表。

有了Rule实例，我们就可以对每一条iptables规则进行判断分析。

### Rule规则说明
``` python
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
```
这里将iptables规则中的具体的"参数"和其"含义"进行了一一映射，而后面的"含义"就是Rule对象的属性名称。
> 除了此处映射的属性名称外，`-m`和`--match`拥有特殊的对待，它们使用其match的名称来当做其属性名称，例如：`-m set --match-set es-node src`的属性名称为`set`

> 特殊modules，`MODULE_NO_EXT = ["tcp"]`，因为`-m tcp`并不一定强制需要。以下规则都是正确的，所以需要跳过这个module的判断。
- `-p tcp -m tcp --dport 80`
- `-p tcp --dport 80`


### 使用范例
例如，我们可以通过以下逻辑来实现判断
``` python
if __name__ == '__main__':
    iptables = Iptables.parse_iptables("/vagrant/iptables-parser/iptables-template", file=True)
    for i in iptables.rules:
        if (not hasattr(i, "set")
            and i.type is "rule"
            and not hasattr(i, "reject-with")):
            print i.raw
```
这里我们需要筛选出满足以下条件的规则
- 使用了ipset
- 规则类型为rule
- 非reject-with类型的rule

同理可以根据Rule中的属性来灵活组合出不同的逻辑，方便后面整理或者二次处理。