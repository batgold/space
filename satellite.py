#!/usr/bin/python
import numpy as nmp
import coord_trans
from datetime import timedelta

class Satellite():

    def __init__(self, epoch1, epoch2):
        self.epoch1 = epoch1
        self.epoch2 = epoch2
        self.type = None

        self._calc_simtime()

        self.lat = nmp.zeros(self.sim_cnt)
        self.lon = nmp.zeros(self.sim_cnt)
        self.alt = nmp.zeros(self.sim_cnt)

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

        for n in range(0, self.sim_cnt):
            self.epochX = self.epoch1 + timedelta(seconds=n*self.sim_factor*10)

            self.epoch = self.epochX
            self._get_pos()
            self._get_lla(n)

    def _get_pos(self):
        """Convert TLE to Postion & Velocity"""
        self.pos, \
        self.vel, \
        self.epoch0 = coord_trans.sgp4(self.line1, self.line2, self.epoch)

    def _get_lla(self, ndx=0):
        """Convert Position/Velocity to Lat/Lon"""
        self.lat[ndx], \
        self.lon[ndx], \
        self.alt[ndx] = coord_trans.teme2lla(self.pos, self.epoch)

    def _calc_simtime(self):
        """Return a reasonable amount of animation frames"""
        epoch_delta = (self.epoch2 - self.epoch1).total_seconds()

        n = 0
        while epoch_delta > 100:      # cut sim_cnt to under 100
            epoch_delta = nmp.floor(epoch_delta / 10)
            n += 1

        self.sim_cnt = int(epoch_delta)
        self.sim_factor = n

class GraphFrame():

    def __init__(self, sat_list):
        self.sat_list = sat_list
        self.name = []
        self.lat = []
        self.lon = []
        self.alt = []
        self.size = []
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
            else:
                self.size.append(20)
                self.color.append('C0')
                self.marker.append(u'o')

    def get_params(self, n):
        return [self.lat[n],
                self.lon[n],
                self.alt[n],
                self.size[n],
                self.color[n],
                self.marker[n],
                self.name[n]]

