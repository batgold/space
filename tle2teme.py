#!/usr/bin/python
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs84

def sgp4(tle, epoch):
    #extract from TLE: pos, vel in TEME frame

    line0 = tle[0]
    line1 = tle[1]
    line2 = tle[2]
    satrec = twoline2rv(line1, line2, wgs84)

    # if epoch is not set, grab from TLE
    if not epoch:
        epoch = satrec.epoch

    pos, __ = satrec.propagate(
            epoch.year, epoch.month, epoch.day, epoch.hour, epoch.minute, epoch.second)

    return pos, line0, epoch

def _target_tle(tle_set, target):
    # specify a single satellite for tle
    line0 = tle_set[0::3]
    for n, name in enumerate(line0):
        if name == '0 ' + target:
            tle = tle_set[n*3:n*3 + 3]
            return tle

