import galspy.IO.BigFile as bf
import os

def main(env,args):
    path = os.path.join(env["PWD"],"attr-v2")
    attr_v2 = bf.Attribute(path).Read()

    keys = attr_v2.keys()
    klen = [len(key) for key in keys]
    maxlen = max(klen)

    for key in attr_v2:
        print(key.ljust(maxlen+4)," : ",end="")
        val=attr_v2[key]
        if key=="MassTable":val = [round(mt,7) for mt in val]
        print(val)