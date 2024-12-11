import numpy as np
x = np.zeros(10)
i = [0,1,2,3,1]
a = [1,1,1,1,2]
np.add.at(x, i, a)
print(x)