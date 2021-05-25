#!/usr/bin/env python3

'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

Stats, Maths and classification functions

https://acp.copernicus.org/articles/21/5117/2021/
'''


import sys
import os

import numpy as np
import scipy as sp
from scipy.interpolate import RegularGridInterpolator
#import scipy.ndimage
import scipy.stats as stats

from matplotlib import cm
import matplotlib.colors as mcolors


class clc(object):
 #binning
 def make_bin_stat(self,lat,lon,var,sbin,stat):

  malo=180.
  milo=-180.
  mala=90.
  mila=-90

  lats=np.arange(mila,mala+sbin,sbin)
  lons=np.arange(milo,malo+sbin,sbin)

  stat_var, xedges, yedges, binnumber = stats.binned_statistic_2d(
  lat, lon, values=var, statistic=stat,
  bins=[lats,lons])

  return stat_var, lons, lats

#pass filter
 def filter(self,var,sig):

  U=var

  V=U.copy()
  V[np.isnan(U)]=0
  VV=sp.ndimage.gaussian_filter(V,sigma=sig)

  W=0*U.copy()+1
  W[np.isnan(U)]=0
  WW=sp.ndimage.gaussian_filter(W,sigma=sig)

  Z=VV/WW

  return Z

 #pass filter
 def high_pass(self,lat,lon,data,sig,bin_size):

  data_bin,lons,lats=self.make_bin_stat(lat,lon,data,bin_size,'mean')
  plats=lats[0:len(lats)-1]+bin_size/2
  plons=lons[0:len(lons)-1]+bin_size/2
  yy, xx = np.meshgrid(plats,plons)
  b_lp=self.filter(data_bin,sig)

  fint = RegularGridInterpolator((plats,plons), b_lp, bounds_error=False, fill_value=None)
  coord = np.column_stack((lat,lon))
  data_lp=data-fint(coord)

  return data_lp

 #outlier filtering
 def get_filt_sig(self,var,sig):
    filt=np.ones((len(var)),int)
    filt[abs(var)>(np.mean(var)+sig*np.std(var))]*=-1
    return filt

 #threshold filtering
 def get_filt_ths(self,var,ths):
    filt=np.ones((len(var)),int)
    filt[abs(var)>ths]*=-1
    return filt

 #quadrant classification
 def get_class_quadrants(self,obs,mod):
    quad=np.zeros((len(mod)),int)
    quad[(obs>mod) & (obs>-mod)]+=1
    quad[(obs<mod) & (obs>-mod)]+=2
    quad[(obs<mod) & (obs<-mod)]+=3
    quad[(obs>mod) & (obs<-mod)]+=4
    return quad




