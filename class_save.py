#!/usr/bin/env python3
'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

This is the script to perform the classification of the filtered ODB
and save the results in a simple csv format

The classification is explained in
https://acp.copernicus.org/articles/21/5117/2021/
'''

import sys
import os

#test plotting
import matplotlib.pyplot as pl

#local functions (not everything is necessary)
from odb import *
from geo import *
from dat import *
from utl import *
from clc import *


##################################

###input params
date=sys.argv[1]
window_len=sys.argv[2]
dir_data=sys.argv[3]
dir_save=sys.argv[4]


file_stats=dir_data+"st_bin_"+date+"_w"+str(window_len)+"days.npz"

#############
#make the classification per zone
# fgd_lp, obs_lp, mod_lp and lon,lat are needed




#areas list
list_region=['global']#,'europe','northam','mideast']

for area in list_region:

    cnt_thrsh=3
    cnt,lon,lat,obs,err,fgd,mod,fgd_lp,obs_lp,mod_lp = utl().load_file(file_stats,cnt_thrsh)

    m,milo,malo,mila,mala = geo().base_region(area)

    cnt,lon,lat,obs,err,mod,fgd_lp,obs_lp,mod_lp = geo().cut_geo_multi_list(cnt,lon,lat,obs,err,mod,fgd_lp,obs_lp,mod_lp,milo,malo,mila,mala)

    #test plots
    #bx,by=m(lon,lat)
    #pl.figure(0)
    #m.drawcoastlines(linewidth=1,color='grey')
    #m.drawcountries(linewidth=0.5,color='grey')
    #m.drawstates(linewidth=0.25,color='grey')
    #pl.scatter(bx,by)
    #pl.show()
  

    ths=err
    out_lab = clc().get_filt_ths(fgd_lp,ths)
    #out_lab = clc().get_filt_sig(fgd_lp,3.0)

    fgd_lp=fgd_lp[out_lab==-1]
    obs_lp=obs_lp[out_lab==-1]
    mod_lp=mod_lp[out_lab==-1]
    cnt=cnt[out_lab==-1]
    lat=lat[out_lab==-1]
    lon=lon[out_lab==-1]

    quad=clc().get_class_quadrants(obs_lp,mod_lp)
    #dist_norm=np.sqrt(obs_lp**2+mod_lp**2)
    dist_norm=abs(fgd_lp)
    #make the classification arch in csv
    df = pd.DataFrame({'lon':lon,'lat':lat,'N_occurences':cnt.astype(int),'magnitude':dist_norm,'category':quad}) 
    df.to_csv(dir_save+'CH4detec_'+date+'.csv', index=False,float_format='%.3f')

if not os.path.isfile(dir_save+"README"): utl().gen_rdm()



exit()
