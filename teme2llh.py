#!/usr/bin/python
import numpy as nmp
from datetime import datetime
from sgp4.earth_gravity import wgs84

pi = nmp.pi

def _julian_date(epoch):
    # calculate Julian day, from 4713 bc
    # quasar.as.utexas.edu/BillInfo/JulianDatesG.html
    y = epoch.year
    m = epoch.month
    d = epoch.day
    s = (epoch.hour + (epoch.minute + epoch.second/60)/60)/24

    if m < 3:
        y = y - 1
        m = m + 12
    x0 = nmp.trunc(y/100)
    x1 = nmp.trunc(x0/4)
    x2 = 2 - x0 + x1
    x3 = nmp.trunc(365.25 * (y + 4716))
    x4 = nmp.trunc(30.6001 * (m + 1))

    jd =  d + x2 + x3 + x4 - 1524.5 + s
    return jd

def teme2llh(pos, epoch):

    jdut1 = _julian_date(epoch)

    gmst = _gstime(jdut1)

    rot = [nmp.cos(gmst), nmp.sin(gmst), 0, -nmp.sin(gmst), nmp.cos(gmst), 0, 0, 0, 1]
    rot = nmp.reshape(rot, (3, 3))
    r_ecef = nmp.matmul(rot,pos)

    lat, lon, alt = _ecef2lla(r_ecef)

    return lat, lon, alt

def _gstime(jd):
    # julian data at 2000: 2451545.0
    # this is the reference date for the conversion equation below.
    jd2000 = _julian_date(datetime(2000,1,1,12))

    # julian centuries from 2000; for conversion equation below
    T = (jd - jd2000)/36525

    # conversion factor from teme to ecef, sec
    gmst0 = 67310.54841 + (876600*3600 + 8640184.812866)*T + 0.093104*T*T - 6.2e-6*T*T*T

    # angle between vernal equinox and Greenwich meridian, rad eastward
    gmst_rad = gmst0 * 2*pi / 86400

    # bring back to [0:2pi]
    gmst = nmp.mod(gmst_rad, 2*pi)

    #if gmst < 0:
        #gmst += 2*pi
    return gmst

def _ecef2lla(p):
    x, y, z = p
    # earth radius
    a = wgs84.radiusearthkm
    # earth eccentricity
    e = 0.081819190842622
    small = 1e-10
    n = 0

    lon = nmp.arctan2(y, x)*180/pi
    # + is east, - is west
    if lon > 180:
        lon -= 180

    lat_delta = 100
    lat = nmp.arctan2(z, nmp.sqrt(x*x + y*y))
    while lat_delta > small and n < 20:
        lat0 = lat
        c = a*e*e*nmp.sin(lat0) / nmp.sqrt(1 - e*e*nmp.sin(lat0)*nmp.sin(lat0))
        lat = nmp.arctan2(z + c, nmp.sqrt(x*x + y*y))
        n += 1
        lat_delta = nmp.abs(lat0 - lat)

    if n > 15:
        print('latitude calculation did not converge.\n')

    alt = nmp.sqrt(x*x + y*y)/nmp.cos(lat) - a/nmp.sqrt(1 - e*e*nmp.sin(lat)**2)

    lat *= 180/pi
    return lat, lon, alt


