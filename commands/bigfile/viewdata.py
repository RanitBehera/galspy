import galspy.IO.BigFile as bf
import os

def main(env):
    path = os.path.join(env["PWD"])
    data = bf.Column(path).Read()
    print(data)