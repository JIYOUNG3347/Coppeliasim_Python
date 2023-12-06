import time
import sys
import os

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))
sys.path.append("/home/user/cable_casting_4.4.0/VREP_4.4.0/programming/zmqRemoteApi/clients/python")
import numpy as np
from zmqRemoteApi import RemoteAPIClient


print('Program started')

client = RemoteAPIClient()
sim = client.getObject('sim')

client.setStepping(True)

sim.startSimulation()
while (t := sim.getSimulationTime()) < 25:
    s = f'Simulation time: {t:.2f} [s]'
    print(s)
    client.step()
sim.stopSimulation()
