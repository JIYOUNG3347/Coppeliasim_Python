import sys
import os
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from pytransform3d.plot_utils import make_3d_axis
from pytransform3d.transformations import random_transform
from pytransform3d.transform_manager import TransformManager
from pytransform3d.plot_utils import Frame

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



def draw_3d_plot(ax, time,objPosition, objMatrix):
    ax = ax
    time = str(time) + 's'
    # 그래프 초기화
    ax.clear()

    # objPosition 그리기
    ax.plot(objPosition[:, 0], objPosition[:, 1], objPosition[:, 2], label=time, c='gray')

    tm = TransformManager()
    for i in range(8):
        tm.add_transform(str(i), "Robot Base", objMatrix[i])
    ax = tm.plot_frames_in("Robot Base", ax=ax, alpha=0.7, s=0.05)


    end_effector = np.array(sim.getObjectMatrix(sim.getObjectHandle("Tip"), -1))
    end_effector = end_effector.reshape(3, 4)
    end_effector = np.append(end_effector, [np.array([0, 0, 0, 1])], axis=0)
    frame = Frame(end_effector, label="Tip", s=0.3)
    frame.add_frame(ax)

    ax.set_xlim([-0.1, 0.9])
    ax.set_ylim([-0.5, 0.5])
    ax.set_zlim([0.0, 1.0])

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    ax.view_init(15, 90)
    title_font = {
            'fontsize': 16,
            'fontweight': 'bold'
    }

    plt.title('Cable Joint Position & Orientation', fontdict=title_font, loc='center', pad=20)

    # 범례 표시
    ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

    # 그래프 업데이트 및 1초 딜레이
    plt.draw()
    plt.pause(0.01)


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
objHandleList = objHandle("Cylinder", 8)


# Simulation Time
t = sim.getSimulationTime()
while t < 5.0:
    print(sim.getSimulationTime())
    objPosition, objMatrix = objM(objHandleList, 8)
    draw_3d_plot(ax, t, objPosition, objMatrix)
    t = sim.getSimulationTime()

sim.stopSimulation()
print('Program stopped')
