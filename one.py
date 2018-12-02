#!/usr/bin/python
import pickle
from datetime import datetime
import numpy as nmp
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from skyfield.api import EarthSatellite, load
import json
import requests

session = requests.Session()
base_url = 'https://www.space-track.org/'
query_url = base_url + '/basicspacedata/query/'
re = wgs72.radiusearthkm
ts = load.timescale()
t = ts.now()

def st_login():
    # open seesion & post credentials to spact-track.org
    login_url = base_url + 'ajaxauth/login'
    username = 'batgold@gmail.com'
    password = 'berttracksspaceequipment'
    login_cred = {'identity': username, 'password': password}

    sess = session.post(login_url, data=login_cred)
    print('login response: ', sess.reason)

def st_close():
    # close session with space-track.org
    logout_url = base_url + 'ajaxauth/logout'
    sess = session.get(logout_url)
    print('logout response: ', sess.reason)
    session.close()

def geo_catalog():
    cat_q = query_url + 'class/satcat/PERIOD/1430--1450/CURRENT/Y/DECAY/null-val/format/json'
    cat = session.get(cat_q).json()

def geo_tle():
    #tle_q = query_url + 'class/tle_latest/ORDINAL/1/EPOCH/>now-30/MEAN_MOTION/0.99--1.01/ECCENTRICITY/<0.01/format/3le'
    tle_q = query_url + 'class/tle_latest/ORDINAL/1/MEAN_MOTION/0.99--1.01/ECCENTRICITY/<0.01/format/3le'

    tle = session.get(tle_q).text
    tle = tle.splitlines()
    sat_num = int(len(tle) / 3)
    print('total satellites found: ', sat_num)

    with open('geo_tle', 'wb') as f:
        pickle.dump(tle, f)
    return tle

def target_tle(tle, target):
    line0 = tle[0::3]
    for n, name in enumerate(line0):
        if name == '0 ' + target:
            print('target: ', target, ' #', n*3)
            return n*3


#st_login()
#tle = geo_tle()

with open('geo_tle', 'rb') as f:
    tle = pickle.load(f)


target_name = 'OPTUS D1'
target_n = target_tle(tle, target_name)

tle = tle[target_n:target_n+3]
print(tle)
sat = twoline2rv(tle[1], tle[2], wgs72)
pos, vel = sat.propagate(2018,11,24,0,0,0)

print('pos = ', pos, '\nvel = ', vel)
r = nmp.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)
print('r = ', r - re)


#skyfield
sat = EarthSatellite(tle[1], tle[2])
geo = sat.at(t)
sub = geo.subpoint()
lat = sub.latitude
lon = sub.longitude
elv = sub.elevation

print('lon: ', lon)

def data_process():
    APOGEE = 35786  #km
    new_data = []
    for sat in satcat:
        if float(sat['INCLINATION']) <= 15.0:
            if float(sat['APOGEE']) < (APOGEE + 320.0) and float(sat['APOGEE']) > (APOGEE - 320.0):
                new_data.append(sat)


    #print('new\n',new_data[0])
    for sat in satcat:
        if sat['SATNAME'] == 'INTELSAT 19':
            i19 = sat

    print('\n', i19)

    satellite = twoline2rv(tle[0], tle[1], wgs72)
    print(satellite.satnum)

#st_close()


def julian_date(d, m, y):
    # calculate Julian date
    # quasar.as.utexas.edu/BillInfo/JulianDatesG.html
    if m < 3:
        y = y - 1
        m = m + 12
    a = nmp.trunc(y/100)
    b = nmp.trunc(a/4)
    c = 2 - a + b
    e = nmp.trunc(365.25 * (y + 4716))
    f = nmp.trunc(30.6001 * (m + 1))
    return c + d + e + f - 1524.5

def eci2ecef(jd, t):
    # julian day at 2000
    j2000 = julian_date(1.5,1,2000)
    # julian century
    jcent = 36525
    # julian day
    tu = (jd - j2000) / jcent
    # earth's inertial rotation rate, rad/s
    wi = 7.2921151467e-5
    # rate of precession in right ascension, rad/s
    rpra = 7.086e-12 + 4.3e-15*tu
    # rotation rate in precessing reference frame, rad/s
    wp = wi + rpra

    # greenwich mean sidereal time at 0h UT1 of Julian Ephemeris Date, sec
    gmst = 24110.54841 + 8640184.812866*tu + 0.093104*tu*tu - 6.2e-6*tu*tu*tu
    print('gmst2 = ', gmst)

    dt = jd - j2000
    x = gmst + wp*(t - dt)

    B = [nmp.cos(x), nmp.sin(x), 0, -nmp.sin(x), nmp.cos(x), 0, 0, 0, 1]
    return nmp.reshape(B, (3, 3))

def ecef2llh(p):
    lon = nmp.arctan2(p[1], p[0])*180/nmp.pi
    if lon < 0:
        lon += 360
    return lon

def gmst(jd):
    w,x,y,z = [24110.54841, 8640184.812866, 0.093104, -6.2e-6]

    jd2000 = julian_date(1.5,1,2000)
    du = jd - jd2000
    tu = du / 36525
    gmst = w + x*tu + y*tu**2 + z*tu**3
    gmst = round(gmst, 4)
    print('gmst = ', gmst)
    print(nmp.mod(gmst, 86400))
    print(7.2921151e-5 * 180 / nmp.pi * nmp.mod(gmst,86400))


now = datetime.today()

jd = julian_date(now.day, now.month, now.year)
#jd = julian_date(1, 10, 1995)
print(jd)
gmst(jd)
B = eci2ecef(jd, 0)
p = nmp.matmul(pos, B)
r = nmp.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
print(p, r - re)

lon = ecef2llh(p)
print('lon: ', lon)
#check out:
#pyorbital

