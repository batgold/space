#!/usr/bin/python3
import numpy as nmp
from datetime import datetime
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs84

pi = nmp.pi

def sgp4(tle1, tle2, epoch):
    # extract from TLE: pos, vel in TEME frame
    # return TLE epoch to gauge pos/vel errors
    satrec = twoline2rv(tle1, tle2, wgs84)
    pos, vel = satrec.propagate(
            epoch.year, epoch.month, epoch.day, epoch.hour, epoch.minute, epoch.second)
    return pos, vel, satrec.epoch

def teme2lla(pos_teme, epoch):
    epoch_jd = _julian_date(epoch)
    gmst = _gmst(epoch_jd)
    rot = [nmp.cos(gmst), nmp.sin(gmst), 0, -nmp.sin(gmst), nmp.cos(gmst), 0, 0, 0, 1]
    rot = nmp.reshape(rot, (3, 3))
    pos_ecef = nmp.matmul(rot, pos_teme)
    lat, lon, alt, x, y, z= _ecef2lla(pos_ecef)
    return lat, lon, alt, x, y, z

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

def _gmst(jd):
    # Calculate Greenwich Mean Sidereal Time
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

    if gmst < 0:
        gmst += 2*pi

    return gmst

def _ecef2lla(pos):
    # Convert from ECEF to Lat, Lon, Alt

    x, y, z = pos
    # earth radius
    a = 6378.137
    # earth eccentricity
    e = 0.081819190842622
    small = 1e-10
    n = 0

    # + is east, - is west
    lon = nmp.arctan2(y, x)

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
    lon *= 180/pi

    return lat, lon, alt, x, y, z

def lla2ecef(lat, lon, alt):

    # earth radius
    a = 6378.137
    # earth eccentricity
    e = 0.081819190842622

    lat = lat*pi/180
    lon = lon*pi/180

    rn = a / nmp.sqrt(1- e*e*nmp.sin(lat)*nmp.sin(lat))

    x = (rn + alt) * nmp.cos(lat)*nmp.cos(lon)
    y = (rn + alt) * nmp.cos(lat)*nmp.sin(lon)
    z = ((1-e*e)*rn + alt) * nmp.sin(lat)

    return x, y, z
