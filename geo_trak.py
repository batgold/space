#!/usr/bin/python
import argparse
import sys
import pickle
import graph as grf
from satellite import Satellite
from satellite import GraphFrame
import coord_trans
import space_track_api as api
from datetime import datetime, timedelta
import numpy as nmp
from tqdm import tqdm

#TODO: check out pyorbital

def main():
    inputs = read_input()
    x = calc_orbits(inputs)
    output(inputs, x)

def read_input():
    inputs = {}

    #  ------------------ parse input arguments --------------------

    parser = argparse.ArgumentParser()
    t1_arg = parser.add_mutually_exclusive_group()
    t2_arg = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '-u', '--update', action='store_true', help='update TLE')
    parser.add_argument(
        'lon0', type=float, help='starting longitude')
    parser.add_argument(
        'targ', type=str, help='target satellite name')
    t1_arg.add_argument(
        '-n', '--now', action='store_true', help='start date = now')
    t1_arg.add_argument(
        '-t1', type=_datetime_type, nargs=1, help='start date mm/dd/yy-hh:mm:ss')
    t2_arg.add_argument(
        '-t2', type=_datetime_type, help='stop date mm/dd/yy-hh:mm:ss')
    t2_arg.add_argument(
        '-tr', nargs=1, help='relative time from start, ddd:hh')

    args = parser.parse_args()

    #  --------------- get tle from space_track.org ----------------

    if args.update:
        session = api.login()
        tle_list = api.get_tle(session)
        api.close(session)
    else:
        with open('geo.tle', 'rb') as f:
            tle_list = pickle.load(f)

    inputs['tle_list'] = tle_list

    #  ------------------------ get epochs -------------------------

    # start time, t1
    if args.now:
        epoch1 = datetime.utcnow()
    else:
        epoch1= args.t1

    # end time, t2
    if args.tr:
        d, h = [int(x) for x in args.tr[0].split(':')]

        #datetime.timedelta([d,] [sec,] [microsec,] [msec,] [min,] [hr,] [week])
        epoch2 = epoch1 + timedelta(d,0,0,0,0,h)
    else:
        epoch2 = args.t2

    inputs['epoch1'] = epoch1
    inputs['epoch2'] = epoch2

    #  ---------------------- get locations ------------------------

    inputs['lon0'] = args.lon0
    inputs['target_name'] = args.targ

    return inputs

def calc_orbits(inputs):

    # Epoch 0 is pulled from the TLE; gives the most accurate orbit
    # Epoch 1 is the start time of the simulation
    # Epoch 2 is the end time of the simulation

    tle_list = inputs['tle_list']
    lon0 = inputs['lon0']
    target_name = inputs['target_name']
    epoch1 = inputs['epoch1']
    epoch2 = inputs['epoch2']


    #  ------------------- build satellite list --------------------

    sat_list = [Satellite(epoch1, epoch2) for n in range(0, len(tle_list), 3)]

    for n, sat in enumerate(tqdm(sat_list, desc='Loading Satellites')):
        tle = tle_list[n*3:n*3+3]
        sat.load_tle(tle)

        if target_name in sat.name:
            sat.type = 'target'
            sat_target = sat


    #  --------------- parse out objects in region -----------------

    #TODO: account for sats initially out of region

    # lon0 is the global starting point; defined by user
    # lon1 is the tracked satellite's longitude
    # lon2 is the global ending point; target's longitude

    tmp_list = []
    for n, sat in enumerate(sat_list):
        lon1 = sat.lon[0]
        lon2 = sat_target.lon[0]

        if (lon1 >= lon0 and lon1 <= lon2 and lon2 > lon0) \
        or (lon1 <= lon0 and lon1 >= lon2 and lon2 < lon0):
            tmp_list.append(sat)

    sat_list = tmp_list     # only sats in region of interest


    #  ------------------- calculate all epochs --------------------

    for n, sat in enumerate(tqdm(sat_list, desc='Computing Motion')):
        sat.get_motion()


    #  ----------------------- Add RSV -----------------------
    #rsv = Satellite(epoch1, epoch2)
    #rsv.load_rsv(lon0, sat_target.lon[0])
    sat_list.append(Satellite(epoch1, epoch2, [lon0, sat_target.lon[0]]))
    #rsv = sat_list[-1]
    #rsv.load_rsv(lon0, sat_target.lon[0])

    #  ----------------------- reformat data -----------------------

    frame_cnt = sat_list[0].sim_cnt
    frame_list = [GraphFrame(sat_list) for n in range(frame_cnt)]

    for n, frame in enumerate(tqdm(frame_list, desc='Building Frames')):
        frame.load_data(n)

    return frame_list

def output(inputs, x):

    #  ----------------------- print results -----------------------
    print('\r')
    print('epoch start: ', inputs['epoch1'], '\r')
    print('epoch end: ', inputs['epoch2'], '\n')

    grf.graph(x)

def _datetime_type(arg_datetime):
    return datetime.strptime(arg_datetime, '%x-%X')

if __name__ == '__main__':
    main()
