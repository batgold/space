#!/usr/bin/python
import numpy as nmp
import coord_trans
from datetime import timedelta

class Satellite():

    def __init__(self, epoch1, epoch2, lon0=False, dirx=0):
        self.epoch1 = epoch1
        self.epoch2 = epoch2
        self.type = None

        self._calc_simtime()

        self.dt = 10**self.sim_factor
        self.x = nmp.zeros(self.sim_cnt)
        self.y = nmp.zeros(self.sim_cnt)
        self.z = nmp.zeros(self.sim_cnt)
        self.lat = nmp.zeros(self.sim_cnt)
        self.lon = nmp.zeros(self.sim_cnt)
        self.alt = nmp.zeros(self.sim_cnt)
        self.range = nmp.zeros(self.sim_cnt)

        if lon0:
            self.load_rsv(lon0, dirx)

    def load_tle(self, tle):
        """Convert TLE parameters to Lat/Lon"""
        self.name = tle[0]
        self.line1 = tle[1]
        self.line2 = tle[2]

        self.epoch = self.epoch1
        self._get_pos()
        self._get_lla()

        if 'R/B' in self.name:
            self.type = 'RB'

    def get_motion(self):
        """Get Position at each Epoch"""

        for n in range(self.sim_cnt):
            self.epochX = self.epoch1 + timedelta(seconds=n*self.dt)

            self.epoch = self.epochX
            self._get_pos(n)
            self._get_lla(n)

    def get_range(self, rsgs):
        for n in range(self.sim_cnt):
            dx = rsgs.x[n] - self.x[n]
            dy = rsgs.y[n] - self.y[n]
            dz = rsgs.z[n] - self.z[n]
            self.range[n] = nmp.sqrt(dx*dx + dy*dy + dz*dz)
            print(self.name, self.range[n])

    def load_rsv(self, lon0, dirx):
        self.name = '0 RSGS'
        self.type = 'RSGS'
        self.vel = 4/86400                      # deg/second
        time_increment = 10**self.sim_factor    # seconds

        for n in range(self.sim_cnt):
            self.lat[n] = 0
            self.lon[n] = lon0 + dirx * n * self.vel * time_increment
            self.alt[n] = 35800 + 100
            self.x[n], self.y[n], self.z[n] = coord_trans.lla2ecef(self.lat[n], self.lon[n], self.alt[n])

    def _get_pos(self, n=0):
        """Convert TLE to Postion & Velocity"""
        self.pos, \
        self.vel, \
        self.epoch0 = coord_trans.sgp4(self.line1, self.line2, self.epoch)

    def _get_lla(self, n=0):
        """Convert Position/Velocity to Lat/Lon"""
        self.lat[n], \
        self.lon[n], \
        self.alt[n], \
        self.x[n], \
        self.y[n], \
        self.z[n] = coord_trans.teme2lla(self.pos, self.epoch)

    def _calc_simtime(self):
        """Return a reasonable amount of animation frames"""
        epoch_delta = (self.epoch2 - self.epoch1).total_seconds()

        n = 0
        while epoch_delta > 100:      # cut sim_cnt to under 300
            epoch_delta = nmp.floor(epoch_delta / 10)
            n += 1

        self.sim_cnt = int(epoch_delta)
        self.sim_factor = n

class GraphFrame():

    def __init__(self, sat_list):
        self.sat_list = sat_list
        self.dt = self.sat_list[0].dt
        self.lat = []
        self.lon = []
        self.alt = []
        self.size = []
        self.name = []
        self.color = []
        self.marker = []

    def load_data(self, num):
        self.num = num      # Frame Number

        for n, sat in enumerate(self.sat_list):
            self.name.append(sat.name[2:])      # remove leading zero
            self.lat.append(sat.lat[self.num])
            self.lon.append(sat.lon[self.num])
            self.alt.append(sat.alt[self.num])

            if sat.type == 'RB':
                self.size.append(30)
                self.color.append('r')
                self.marker.append('^')
            elif sat.type == 'RSGS':
                self.size.append(60)
                self.color.append('b')
                self.marker.append('s')
            elif sat.type == 'target':
                #self.name[-1] = 'RSO-1'
                self.size.append(40)
                self.color.append('C2')
                self.marker.append('o')
            else:
                self.size.append(16)
                self.color.append('C0')
                self.marker.append('o')

    def get_params(self, n):
        return [self.lat[n],
                self.lon[n],
                self.alt[n],
                self.size[n],
                self.color[n],
                self.marker[n],
                self.name[n]]
