import sys
import os
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import math


wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))
sys.path.append("/home/user/cable_casting_4.4.0/VREP_4.4.0/programming/zmqRemoteApi/clients/python")
import numpy as np
from zmqRemoteApi import RemoteAPIClient

# ObjectHandle Function

def objHandle(name, n):
    objHandleList = []
    for i in range(n):
        objHandleList.append(sim.getObjectHandle(name + str(i)))
    return objHandleList


def objA(handle, n):
    arr = []
    for i in range(n):
        pos = sim.getObjectPosition(handle[i], -1)
        vel = sim.getObjectVelocity(handle[i], -1)
        qua = sim.getObjectQuaternion(handle[i], -1)
        arr.append([pos[0], pos[1], pos[2], vel[0][1], vel[0][1], vel[0][2], qua[0], qua[1], qua[2], qua[3], vel[1][0], vel[1][1], vel[1][2]])
    arr = np.array(arr)
    return arr

# Program Start
print('Program started')

# create client and sim object
client = RemoteAPIClient()
sim = client.getObject('sim')
sim.startSimulation()
client.step()

# Start Position & Orientation
objHandleList = objHandle("Cylinder", 8)


# Simulation Time
a = 0
data = []
while a < 101:
    t = sim.getSimulationTime()
    print(t)
    if t < 7.0:
        arr = objA(objHandleList, 8)
        data.append(arr)
        a = a + 1
    else:
        break


data = np.array(data)
print(data.shape)


sim.stopSimulation()
print('Program stopped')
