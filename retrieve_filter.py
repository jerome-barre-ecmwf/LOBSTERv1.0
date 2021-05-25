#!/usr/bin/env python3
'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

This is the main script to perform retrieval and filtering of the ODB

Filtering is a convoluiton filter on obd spapce explained in
https://acp.copernicus.org/articles/21/5117/2021/
'''

import sys
import os
import numpy as np

#local functions (not everything is necessary)
from odb import *
from geo import *
from dat import *
from utl import *
from clc import *



##################################

###input params
date=sys.argv[1]
window_len=int(sys.argv[2])
EXPVER=sys.argv[3]
WORKDIR=sys.argv[4]

###internal params (could be passed at input above if need be)
sat=64
var=188
stream='lwda'
report='35014'
#WORKDIR="work/"
#EXPVER="hblp"
#window_len=30
#size of the bin in degrees
bin_size=0.1
#sig is the smoothing size in number of bins, 
#so sig*bin_size in degrees  
sig=20.0

prefix=WORKDIR+EXPVER+"_tropOMI_odb_"

win_date=dat().single_date_window(sys.argv[1],window_len)

print('1 ',win_date)  

win_files=utl().make_file_list(prefix,win_date)

print('2 ',win_files)

outfile="work/st_bin_"+win_date[0]+"_w"+str(window_len)+"days"
print('3 ',outfile,os.path.isfile(outfile+'.npz'))

if not os.path.isfile(outfile+'.npz'):

 odb().get_odb(win_date,win_files,EXPVER,'ofb',stream,report,False) 
 
 df=odb().concat_db(win_files,sat,var)
 lat=np.array(df['latitude'])
 lon=np.array(df['longitude'])
 obs=np.array(df['obsval'])
 err=np.array(df['obserr']) 
 fgd=np.array(df['departure'])
 mod=obs-fgd
 
 count,lons,lats=clc().make_bin_stat(lat,lon,obs,bin_size,'count') 
 b_obs_m,lons,lats=clc().make_bin_stat(lat,lon,obs,bin_size,'mean')
 b_err_m,lons,lats=clc().make_bin_stat(lat,lon,err,bin_size,'mean')
 b_fgd_m,lons,lats=clc().make_bin_stat(lat,lon,fgd,bin_size,'mean')
 b_mod_m,lons,lats=clc().make_bin_stat(lat,lon,mod,bin_size,'mean')
     
 fgd_lp=clc().high_pass(lat,lon,fgd,sig,bin_size)
 obs_lp=clc().high_pass(lat,lon,obs,sig,bin_size)
 mod_lp=clc().high_pass(lat,lon,mod,sig,bin_size)
 
 b_fgd_lp_m,lons,lats=clc().make_bin_stat(lat,lon,fgd_lp,bin_size,'mean')
 b_obs_lp_m,lons,lats=clc().make_bin_stat(lat,lon,obs_lp,bin_size,'mean')
 b_mod_lp_m,lons,lats=clc().make_bin_stat(lat,lon,mod_lp,bin_size,'mean')

 llat=lats[0:len(lats)-1]+abs(lats[1]-lats[0])/2
 llon=lons[0:len(lons)-1]+abs(lons[1]-lons[0])/2
 lonss, latss = np.meshgrid(llon,llat)
 nlat=np.shape(latss)[0]
 nlon=np.shape(lonss)[1]
 
 count=np.reshape(count,(nlat*nlon))
 latss=np.reshape(latss,(nlat*nlon))
 lonss=np.reshape(lonss,(nlat*nlon))
 b_obs_m=np.reshape(b_obs_m,(nlat*nlon))
 b_err_m=np.reshape(b_err_m,(nlat*nlon))
 b_fgd_m=np.reshape(b_fgd_m,(nlat*nlon))
 b_mod_m=np.reshape(b_mod_m,(nlat*nlon))
 
 b_fgd_lp_m=np.reshape(b_fgd_lp_m,(nlat*nlon))
 b_obs_lp_m=np.reshape(b_obs_lp_m,(nlat*nlon))
 b_mod_lp_m=np.reshape(b_mod_lp_m,(nlat*nlon))
 
 latss=latss[count>0]
 lonss=lonss[count>0]

 b_obs_m=b_obs_m[count>0]
 b_err_m=b_err_m[count>0]
 b_fgd_m=b_fgd_m[count>0]
 b_mod_m=b_mod_m[count>0]
 
 b_fgd_lp_m=b_fgd_lp_m[count>0]
 b_obs_lp_m=b_obs_lp_m[count>0]
 b_mod_lp_m=b_mod_lp_m[count>0]
 
 count=count[count>0]
 
 #output the full dataset, filtered and unfiltered
 np.savez(outfile,lat=latss,lon=lonss,count=count,
           obs_m=b_obs_m, err_m=b_err_m, 
           fgd_m=b_fgd_m,mod_m=b_mod_m, 
           fgd_lp_m=b_fgd_lp_m,
           obs_lp_m=b_obs_lp_m, 
           mod_lp_m=b_mod_lp_m) 

 odb().clean_odb(win_files)


exit()
