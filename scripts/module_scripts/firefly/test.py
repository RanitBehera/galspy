import numpy as np
from firefly.data_reader import ArrayReader
import time
from firefly.server import spawnFireflyServer,quitAllFireflyServers

coords = np.random.randn( 20000, 3 )
fields = np.random.random(size=coords[:,0].size)


my_arrayReader = ArrayReader(
    coords,
    fields=fields,
    write_to_disk=False)


process = spawnFireflyServer()
my_arrayReader.sendDataViaFlask()

time.sleep(100)
return_code = quitAllFireflyServers()




