import galspy.FileTypes.BigFile as bf
import os

def main(env):
    path = os.path.join(env["PWD"],"header")
    header = bf.Header(path).Read()

    for key in header:
        print(key.ljust(6+4),":",header[key])