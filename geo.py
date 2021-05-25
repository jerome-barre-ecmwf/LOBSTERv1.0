#!/usr/bin/env python3

'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

Geometry functions

https://acp.copernicus.org/articles/21/5117/2021/
'''

import sys
import os
import numpy as np
from mpl_toolkits.basemap import Basemap
#warning basemap is now deprecated

class geo(object):
 def base_region(self,area):
 #defines bounding boxes and returns a projections
  if area=='global':
   malo=180.
   milo=-180.
   mala=90.
   mila=-60

  if area=='europe':
   malo=45.
   milo=-11.
   mala=72.
   mila=36

  if area=='mideast':
   malo=85.
   milo=35.
   mala=45.
   mila=20.

  if area=='northam':
   malo=-60.
   milo=-127.
   mala=55.
   mila=25.

  #basemap is now deprecated this should be changed for geopandas
  m = Basemap(projection='cyl',llcrnrlat=mila,urcrnrlat=mala,\
            llcrnrlon=milo,urcrnrlon=malo,resolution='l')

  return m,milo,malo,mila,mala

 def cut_fields(self,lon,lat,var,milo,malo,mila,mala):
    #cut your 2D field given bounding coordinates

    min_lon=(np.where((lon>=milo) & (lon<=malo))[0])[0]
    max_lon=(np.where((lon>=milo) & (lon<=malo))[0])[-1]

    min_lat=(np.where((lat>=mila) & (lat<=mala))[0])[0]
    max_lat=(np.where((lat>=mila) & (lat<=mala))[0])[-1]

    var=var[min_lat:max_lat,min_lon:max_lon]

    return var

 def cut_geo_list(self,lon,lat,var,milo,malo,mila,mala):
    #cut your list of points given bounding coordiantes
    var=var[(lon>=milo) & (lon<=malo) & (lat>=mila) & (lat<=mala)]

    return var

 def cut_geo_multi_list(self,cnt,lon,lat,obs,err,mod,fgd_lp,obs_lp,mod_lp,milo,malo,mila,mala):

    new_cnt=self.cut_geo_list(lon,lat,cnt,milo,malo,mila,mala)
    new_lon=self.cut_geo_list(lon,lat,lon,milo,malo,mila,mala)
    new_lat=self.cut_geo_list(lon,lat,lat,milo,malo,mila,mala)

    new_obs=self.cut_geo_list(lon,lat,obs,milo,malo,mila,mala)
    new_err=self.cut_geo_list(lon,lat,err,milo,malo,mila,mala)
    new_mod=self.cut_geo_list(lon,lat,mod,milo,malo,mila,mala)

    new_fgd_lp=self.cut_geo_list(lon,lat,fgd_lp,milo,malo,mila,mala)
    new_obs_lp=self.cut_geo_list(lon,lat,obs_lp,milo,malo,mila,mala)
    new_mod_lp=self.cut_geo_list(lon,lat,mod_lp,milo,malo,mila,mala)

    return new_cnt,new_lon,new_lat,new_obs,new_err,new_mod,new_fgd_lp,new_obs_lp,new_mod_lp

