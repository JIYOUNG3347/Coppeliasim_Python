import sys
import os
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from pytransform3d.plot_utils import make_3d_axis
from pytransform3d.transformations import random_transform
from pytransform3d.transform_manager import TransformManager

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))
sys.path.append(".clients/python")
import numpy as np
from zmqRemoteApi import RemoteAPIClient

# ObjectHandle Function

def objHandle(name, n):
    objHandleList = []
    for i in range(n):
        objHandleList.append(sim.getObjectHandle(name + str(i)))
    return objHandleList


def objM(handle, n):
    objPosition = []
    objMatrix = []
    for i in range(n):
        T = np.array(sim.getObjectMatrix(handle[i], -1))
        pos = [T[3], T[7], T[11]]
        objPosition.append(pos)
        T = T.reshape(3, 4)
        T = np.append(T, [np.array([0, 0, 0, 1])], axis=0)
        objMatrix.append(T)
    objPosition = np.array(objPosition)
    objMatrix = np.array(objMatrix)
    return objPosition, objMatrix


# Program Start
print('Program started')
# create client and sim object
client = RemoteAPIClient()
sim = client.getObject('sim')
sim.startSimulation()
client.step()

# Plot
mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111, projection='3d')

# Start Position & Orientation
objHandleList = objHandle("Spherical_joint", 8)
objPosition, objMatrix = objM(objHandleList, 8)
ax.plot(objPosition[:,0], objPosition[:,1], objPosition[:,2], label='0s joint_position', c='black')
tm = TransformManager()
for i in range(8):
    n = str(i)
    tm.add_transform(n, "Robot Base", objMatrix[i])
ax = tm.plot_frames_in("Robot Base", ax=ax, alpha=0.7, s=0.05)


# Simulation Time
while sim.getSimulationTime() < 5.0:
    objPosition, objMatrix = objM(objHandleList, 8)
    print(sim.getSimulationTime())

# End Position & Orientation
objPosition, objMatrix = objM(objHandleList, 8)
print(objMatrix)

# Sim Stop
sim.stopSimulation()
print('Program stopped')

ax.plot(objPosition[:,0], objPosition[:,1], objPosition[:,2], label='5s joint_position', c='gray')

tm = TransformManager()
for i in range(8):
    tm.add_transform(str(i), "Robot Base", objMatrix[i])
ax = tm.plot_frames_in("Robot Base", ax=ax, alpha=0.7, s=0.05)

ax.set_xlim([-0.1, 0.9])
ax.set_ylim([-0.5, 0.5])
ax.set_zlim([0.0, 1.0])
ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
title_font = {
    'fontsize': 16,
    'fontweight': 'bold'
}
# Set the limits of the plot
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
plt.title('Cable Joint Position & Orientation', fontdict=title_font, loc='center', pad = 20)
plt.show()

