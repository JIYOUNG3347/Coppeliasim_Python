import sys
import os
import time

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))
sys.path.append("/home/user/cable_casting_4.4.0/VREP_4.4.0/programming/zmqRemoteApi/clients/python")
import numpy as np
from zmqRemoteApi import RemoteAPIClient


print('Program started')

# create client and sim object
client = RemoteAPIClient()
sim = client.getObject('sim')
sim.startSimulation()
client.step()
while sim.getSimulationTime() < 5.0:
    print(sim.getSimulationTime())
sim.stopSimulation()
print('Program stopped')