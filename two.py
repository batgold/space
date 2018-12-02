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
now = datetime.today()

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


target_name = 'INTELSAT 21'
target_n = target_tle(tle, target_name)

tle = tle[target_n:target_n+3]
print(tle)
sat = twoline2rv(tle[1], tle[2], wgs72)
pos, vel = sat.propagate(now.year,now.month,now.day,0,0,0)

print('pos = ', pos, '\nvel = ', vel)
r = nmp.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)
print('r = ', r - re)


#skyfield
sat = EarthSatellite(tle[1], tle[2])
geo = sat.at(t)
sub = geo.subpoint()
lon = sub.longitude

print('lon: ', lon)
print('\r')

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
    # julian day at 2000 UT1
    j2000 = julian_date(1.5,1,2000)
    # days per julian century
    dpc = 36525
    # julian centuries from epoch 2000 UT1
    jce = (jd - j2000) / dpc
    # earth's inertial rotation rate, rad/s
    wi = 7.2921151467e-5
    # rate of precession in right ascension, rad/s
    rpra = 7.086e-12 + 4.3e-15*jce
    # rotation rate in precessing reference frame, rad/s
    wp = wi + rpra

    # greenwich mean sidereal time at 0h UT1 of Julian Ephemeris Date, sec
    g0 = 24110.54841 + 8640184.812866*jce + 0.093104*jce*jce - 6.2e-6*jce*jce*jce
    print('jd', jd)
    print('g0', g0)
    print('g0 mod', nmp.mod(g0, 86400))
    print('g0 deg', nmp.mod(g0, 86400)*360/84600)
    print('\r')

    t = t * 3600 * 1.002737909350795
    gmst = g0 + t #what about wp?
    x = nmp.mod(gmst, 86400) * 2*nmp.pi / 86400
    print('gmst', gmst)
    print('gmst mod', nmp.mod(gmst, 86400))
    print('gmst deg', nmp.mod(gmst, 86400)*360/86400)
    print('gmst rad', x)

    B = [nmp.cos(x), nmp.sin(x), 0, -nmp.sin(x), nmp.cos(x), 0, 0, 0, 1]
    return nmp.reshape(B, (3, 3))

def ecef2llh(p):
    lon = nmp.arctan2(p[1], p[0])*180/nmp.pi
    if lon < 0:
        lon += 360
    return lon

def gstime(t):
    jdut1 = t
    jd2000 = julian_date(1.5,1,2000)
    dpc = 36525
    tut1 = (jdut1 - jd2000)/dpc
    temp = -6.2e-6*tut1*tut1*tut1 + 0.093104*tut1*tut1 + (876600*3600 + 8640184.812866)*tut1 + 67310.54841
    #temp = 24110.54841 + 8640184.812866*tut1 + 0.093104*tut1*tut1 - 6.2e-6*tut1*tut1*tut1
    temp = nmp.mod(temp*nmp.pi/180/240,2*nmp.pi)
    if temp < 0:
        temp += 2*nmp.pi
    print('gmst',180/nmp.pi*temp)
    return temp

def teme(pos,jdut1,lod):
    gmst = gstime(jdut1)
    st = [nmp.cos(gmst), nmp.sin(gmst), 0, -nmp.sin(gmst), nmp.cos(gmst), 0, 0, 0, 1]
    st = nmp.reshape(st, (3, 3))
    rpef = nmp.matmul(st,pos)
    return rpef

jd = julian_date(now.day, now.month, now.year)
#jd = julian_date(1, 10, 1995)

lod = 0.839*86400
p = teme(pos, jd, lod)
lon = ecef2llh(p)
if lon > 180: lon -= 360
print('lon: ', lon)
print('\r')


hr = 0.839*24
#hr = 9
B = eci2ecef(jd, hr)
p = nmp.matmul(B, pos)
print('xyz = ', p)

lon = ecef2llh(p) # minus gmst deg + g0 deg
# if lon > 180; lon =- 360
print('lon: ', lon)
print('\r')

#check out:
#pyorbital

