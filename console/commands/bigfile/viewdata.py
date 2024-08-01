import galspy.IO.BigFile as bf
import os
import numpy
numpy.set_printoptions(suppress=True)

def main(env):
    path = os.path.join(env["PWD"])
    data = bf.Column(path).Read()
    print(data)