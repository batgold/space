#!/usr/bin/python
import requests
import pickle

base_url = 'https://www.space-track.org/'
query_url = base_url + '/basicspacedata/query/'

def login():
    # open seesion & post credentials to spact-track.org
    session = requests.Session()
    login_url = base_url + 'ajaxauth/login'
    username = 'batgold@gmail.com'
    password = 'berttracksspaceequipment'
    login_cred = {'identity': username, 'password': password}

    sess = session.post(login_url, data=login_cred)
    print('login response: ', sess.reason)
    return session

def close(session):
    # close session with space-track.org
    logout_url = base_url + 'ajaxauth/logout'
    sess = session.get(logout_url)
    print('logout response: ', sess.reason)
    session.close()

def get_tle(session):
    #tle_q = query_url + 'class/tle_latest/ORDINAL/1/EPOCH/>now-30/MEAN_MOTION/0.99--1.01/ECCENTRICITY/<0.01/format/3le'
    tle_q = query_url + 'class/tle_latest/ORDINAL/1/MEAN_MOTION/0.99--1.01/ECCENTRICITY/<0.01/format/3le'

    tle = session.get(tle_q).text
    tle = tle.splitlines()

    sat_num = int(len(tle) / 3)

    with open('geo.tle', 'wb') as f:
        pickle.dump(tle, f)

    return tle

def __geo_catalog():
    cat_q = query_url + 'class/satcat/PERIOD/1430--1450/CURRENT/Y/DECAY/null-val/format/json'
    cat = session.get(cat_q).json()

