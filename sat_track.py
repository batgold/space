#!/usr/bin/python
import sys
import pickle
from datetime import datetime
import tle2teme as t2t
import teme2lla as t2g

def main():
    with open('geo.tle', 'rb') as f:
        tle_list = pickle.load(f)

    start_epoch = datetime.utcnow()
    #start_epoch = datetime(1995,11,18,12,46,0)

    #for n in range(0, len(tle_list), 3):
        #tle = tle_list[n:n+3]
        #pos, name, epoch = t2t.sgp4(tle, start_epoch)
    for n, item in enumerate(tle_list[0::3]):
        if target_name in item:
            tle = tle_list[n*3:n*3+3]
            pos, name, epoch = t2t.sgp4(tle, start_epoch)
            #p, n, t = t2t.sgp4(tle, start_epoch)

    llh = t2g.teme2lla(pos, epoch)
    #llh = t2g.teme2llh(p, v, t)
    print(tle)
    print('pos: ', pos)
    print('llh: ', llh)

if __name__ == '__main__':
    target_name = sys.argv[1]

    main()

