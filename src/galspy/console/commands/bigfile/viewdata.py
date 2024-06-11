import galspy.IO.bigfile as bf
import os

def main(args,env):
    path = os.path.join(env["PWD"])
    data = bf.Column(path).Read()
    print(data)