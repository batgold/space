#!/usr/bin/python
import numpy as nmp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def graph(frame_list, lon0, lon2):

    fig = plt.figure()
    fig.set_size_inches(10, 8, True)
    ax = fig.add_subplot(111, projection='3d')

    frame_cnt = len(frame_list)

    ani = animation.FuncAnimation(fig, update_graph, frame_cnt,
            fargs=(frame_list, ax, frame_cnt, lon0, lon2), interval=600)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.tight_layout(pad=0)
    plt.show()
    #ani.save('orb3.gif', writer='imagemagick', fps=10, dpi=128)

def update_graph(f, frame_list, ax, cnt, lon0, lon2):

    ax.clear()
    f = nmp.mod(f, cnt)
    frame = frame_list[f]
    dt = frame.dt/3600

    for n in range(len(frame.marker)):
        x, y, z, s, c, m, name = frame.get_params(n)

        center = (lon2+lon0)/2
        #WORKING
        ax.scatter(x, y, z, s=s, c=c, marker=m)
        ax.text(x+0.1, y+0.1, z+0.1, '%s'%(name), size=5, zorder=1)
        ax.text(0,center,36250,'Mission Time: %.2f hr'%(f*dt), size=20)
        #ax.text(0,155,36000,'%s / %s'%(f, cnt-1), size=20)

        ax.set_xlabel('Latitude, deg')
        ax.set_ylabel('Longitude, $\circ$E')
        ax.set_zlabel('Altitude, km')

        ax.set_xlim3d(-15,15)
        ax.set_zlim3d(35600,36100)
        if lon2 > lon0:
            ax.set_ylim3d(lon0-5, lon2+5)
        else:
            ax.set_ylim3d(lon0+5, lon2-5)
